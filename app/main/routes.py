from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, ChatMessage, AuditLog, SystemMetrics
from app.forms import EditProfileForm, ChatMessageForm, CommandForm, ServiceControlForm
from app import db
import subprocess
import os

try:
    from app.utils.system_info import get_system_info, get_service_status
    from app.utils.file_manager import get_smb_files, download_smb_file
except ImportError:
    # Fallback functions if utils are not available
    def get_system_info():
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'uptime': 'Unknown',
            'public_ip': 'Unknown',
            'private_ip': 'Unknown',
            'hostname': 'Unknown'
        }
    
    def get_service_status(service):
        return 'unknown'
    
    def get_smb_files(path):
        return []
    
    def download_smb_file(base_path, filename):
        flash('SMB functionality not available.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Get recent chat messages
    chat_messages = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).limit(20).all()
    chat_messages.reverse()  # Show oldest first
    
    # Get system info
    system_info = get_system_info()
    
    # Get service statuses
    openvpn_status = get_service_status('openvpn')
    squid_status = get_service_status('squid')
    
    # Get SMB files
    smb_files = get_smb_files(current_app.config['BASE_SMB_PATH'])
    
    return render_template('main/dashboard.html',
                         chat_messages=chat_messages,
                         system_info=system_info,
                         openvpn_status=openvpn_status,
                         squid_status=squid_status,
                         smb_files=smb_files)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(current_user.email)
    
    if form.validate_on_submit():
        # Check current password if new password is provided
        if form.new_password.data:
            if not form.current_password.data or not current_user.check_password(form.current_password.data):
                flash('Current password is incorrect.', 'error')
                return render_template('main/profile.html', form=form)
            current_user.set_password(form.new_password.data)
        
        # Update profile
        current_user.name = form.name.data
        current_user.email = form.email.data
        if form.profile_image_url.data:
            current_user.profile_image_url = form.profile_image_url.data
        
        db.session.commit()
        
        # Log the profile update
        audit_log = AuditLog(
            action='PROFILE_UPDATE',
            description=f'User {current_user.username} updated their profile',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.profile_image_url.data = current_user.profile_image_url
    
    return render_template('main/profile.html', form=form)

@bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    form = ChatMessageForm()
    if form.validate_on_submit():
        message = ChatMessage(
            content=form.message.data,
            user_id=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')
    else:
        flash('Message could not be sent.', 'error')
    
    return redirect(url_for('main.index'))

@bp.route('/execute_command', methods=['POST'])
@login_required
def execute_command():
    if not current_user.is_admin():
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    form = CommandForm()
    if form.validate_on_submit():
        command = form.command.data
        
        # Log the command execution
        audit_log = AuditLog(
            action='COMMAND_EXECUTION',
            description=f'User {current_user.username} executed command: {command}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        try:
            # Security: Only allow specific commands or use a whitelist
            if any(dangerous in command.lower() for dangerous in ['rm -rf', 'mkfs', 'dd if=', 'format', '> /dev/']):
                flash('Command blocked for security reasons.', 'error')
                return redirect(url_for('main.index'))
            
            output = subprocess.check_output(
                command, 
                shell=True, 
                stderr=subprocess.STDOUT,
                timeout=30  # 30 second timeout
            ).decode('utf-8')
            
            flash(f'Command executed successfully. Output: {output[:500]}...', 'success')
            
        except subprocess.TimeoutExpired:
            flash('Command timed out after 30 seconds.', 'error')
        except subprocess.CalledProcessError as e:
            flash(f'Command failed: {e.output.decode("utf-8")[:500]}...', 'error')
        except Exception as e:
            flash(f'Error executing command: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@bp.route('/browse_smb')
@login_required
def browse_smb():
    path = request.args.get('path', '')
    smb_files = get_smb_files(os.path.join(current_app.config['BASE_SMB_PATH'], path))
    return render_template('main/smb_browser.html', smb_files=smb_files, current_path=path)

@bp.route('/download_smb')
@login_required
def download_smb():
    filename = request.args.get('filename')
    if not filename:
        flash('No filename specified.', 'error')
        return redirect(url_for('main.browse_smb'))
    
    return download_smb_file(current_app.config['BASE_SMB_PATH'], filename)

@bp.route('/metrics')
@login_required
def metrics():
    if not current_user.is_admin():
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    # Get recent system metrics
    metrics = SystemMetrics.query.order_by(SystemMetrics.timestamp.desc()).limit(100).all()
    return render_template('main/metrics.html', metrics=metrics)

@bp.route('/service_control', methods=['GET', 'POST'])
@login_required
def service_control():
    if not current_user.is_admin():
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    from app.forms import ServiceControlForm
    form = ServiceControlForm()
    result = None
    
    if form.validate_on_submit():
        service_name = form.service.data
        action = request.form.get('action')
        
        # Log the service control action
        audit_log = AuditLog(
            action='SERVICE_CONTROL',
            description=f'User {current_user.username} executed {action} on service {service_name}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        try:
            if action == 'status':
                result = subprocess.check_output(['systemctl', 'status', service_name], 
                                               stderr=subprocess.STDOUT, timeout=10).decode('utf-8')
            elif action == 'start':
                result = subprocess.check_output(['sudo', 'systemctl', 'start', service_name], 
                                               stderr=subprocess.STDOUT, timeout=30).decode('utf-8')
                result = f"Service {service_name} started successfully"
            elif action == 'stop':
                result = subprocess.check_output(['sudo', 'systemctl', 'stop', service_name], 
                                               stderr=subprocess.STDOUT, timeout=30).decode('utf-8')
                result = f"Service {service_name} stopped successfully"
            elif action == 'restart':
                result = subprocess.check_output(['sudo', 'systemctl', 'restart', service_name], 
                                               stderr=subprocess.STDOUT, timeout=30).decode('utf-8')
                result = f"Service {service_name} restarted successfully"
            
            flash(f'Command executed successfully', 'success')
        except subprocess.TimeoutExpired:
            result = f'Command timed out after 30 seconds'
            flash('Command timed out', 'error')
        except subprocess.CalledProcessError as e:
            result = e.output.decode('utf-8')
            flash(f'Command failed', 'error')
        except Exception as e:
            result = f'Error: {str(e)}'
            flash(f'Error executing command: {str(e)}', 'error')
    
    # Common services list
    common_services = [
        {'name': 'apache2', 'description': 'Apache Web Server'},
        {'name': 'nginx', 'description': 'Nginx Web Server'},
        {'name': 'mysql', 'description': 'MySQL Database Server'},
        {'name': 'postgresql', 'description': 'PostgreSQL Database Server'},
        {'name': 'ssh', 'description': 'SSH Server'},
        {'name': 'smbd', 'description': 'Samba File Server'},
        {'name': 'nmbd', 'description': 'NetBIOS Name Server'},
        {'name': 'cron', 'description': 'Cron Job Scheduler'},
        {'name': 'docker', 'description': 'Docker Engine'},
        {'name': 'fail2ban', 'description': 'Intrusion Prevention System'}
    ]
    
    return render_template('main/service_control.html', form=form, result=result, common_services=common_services)

@bp.route('/terminal', methods=['GET', 'POST'])
@login_required
def terminal():
    if not current_user.is_admin():
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    form = CommandForm()
    output = None
    
    if form.validate_on_submit():
        command = form.command.data
        
        # Log the terminal command
        audit_log = AuditLog(
            action='TERMINAL_COMMAND',
            description=f'User {current_user.username} executed terminal command: {command}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        try:
            # Security: Block dangerous commands
            dangerous_commands = ['rm -rf', 'mkfs', 'dd if=', 'format', '> /dev/', 'sudo rm', 'rm -f']
            if any(dangerous in command.lower() for dangerous in dangerous_commands):
                flash('Command blocked for security reasons.', 'error')
                output = 'ERROR: Command blocked for security reasons'
            else:
                output = subprocess.check_output(
                    command, 
                    shell=True, 
                    stderr=subprocess.STDOUT,
                    timeout=30,
                    cwd=os.path.expanduser('~')
                ).decode('utf-8')
                flash('Command executed successfully', 'success')
        except subprocess.TimeoutExpired:
            output = 'ERROR: Command timed out after 30 seconds'
            flash('Command timed out', 'error')
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            flash('Command execution failed', 'error')
        except Exception as e:
            output = f'ERROR: {str(e)}'
            flash(f'Error executing command: {str(e)}', 'error')
    
    return render_template('main/terminal.html', form=form, output=output)

@bp.route('/chat', methods=['GET', 'POST'])
@login_required  
def chat():
    form = ChatMessageForm()
    
    if form.validate_on_submit():
        message = ChatMessage(
            content=form.message.data,
            user_id=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('main.chat'))
    
    # Get all chat messages
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
    
    return render_template('main/chat.html', form=form, messages=messages)
