from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, AuditLog, ServiceStatus
from app.forms import RegistrationForm, UserEditForm, ServiceControlForm
from app import db
import secrets
import string

try:
    from app.utils.system_info import control_service
except ImportError:
    def control_service(service, action):
        return {'success': False, 'error': 'Service control not available'}

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Log user creation
        audit_log = AuditLog(
            action='USER_CREATED',
            description=f'Admin {current_user.username} created user {user.username}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'User {user.username} has been created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/add_user.html', form=form)

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(user.username, user.email)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        
        if form.reset_password.data:
            # Generate random password
            new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.set_password(new_password)
            flash(f'Password reset. New password: {new_password}', 'info')
        
        db.session.commit()
        
        # Log user modification
        audit_log = AuditLog(
            action='USER_MODIFIED',
            description=f'Admin {current_user.username} modified user {user.username}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'User {user.username} has been updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.name.data = user.name
        form.role.data = user.role
        form.is_active.data = user.is_active
    
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    if user.username == 'admin':
        flash('The admin account cannot be deleted.', 'error')
        return redirect(url_for('admin.users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    # Log user deletion
    audit_log = AuditLog(
        action='USER_DELETED',
        description=f'Admin {current_user.username} deleted user {username}',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        user_id=current_user.id
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'User {username} has been deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/services')
@login_required
@admin_required
def services():
    services = ServiceStatus.query.all()
    return render_template('admin/services.html', services=services)

@bp.route('/control_service', methods=['POST'])
@login_required
@admin_required
def control_service_route():
    form = ServiceControlForm()
    if form.validate_on_submit():
        service_name = form.service.data
        action = form.action.data
        
        try:
            result = control_service(service_name, action)
            
            # Log service control
            audit_log = AuditLog(
                action='SERVICE_CONTROL',
                description=f'Admin {current_user.username} performed {action} on {service_name}',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                user_id=current_user.id
            )
            db.session.add(audit_log)
            db.session.commit()
            
            if result['success']:
                flash(f'Service {service_name} {action} completed successfully.', 'success')
            else:
                flash(f'Failed to {action} service {service_name}: {result["error"]}', 'error')
                
        except Exception as e:
            flash(f'Error controlling service: {str(e)}', 'error')
    
    return redirect(url_for('admin.services'))

@bp.route('/audit_logs')
@login_required
@admin_required
def audit_logs():
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False)
    return render_template('admin/audit_logs.html', logs=logs)

@bp.route('/system_settings')
@login_required
@admin_required
def system_settings():
    return render_template('admin/system_settings.html')
