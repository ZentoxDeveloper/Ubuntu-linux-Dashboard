from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.models import User, AuditLog
from app.forms import LoginForm
from app import db
from datetime import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data) and user.is_active:
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log the login
            audit_log = AuditLog(
                action='LOGIN',
                description=f'User {user.username} logged in',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                user_id=user.id
            )
            db.session.add(audit_log)
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page)
        else:
            # Log failed login attempt
            audit_log = AuditLog(
                action='LOGIN_FAILED',
                description=f'Failed login attempt for username: {form.username.data}',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(audit_log)
            db.session.commit()
            
            flash('Invalid username, password, or account is disabled.', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Log the logout
        audit_log = AuditLog(
            action='LOGOUT',
            description=f'User {current_user.username} logged out',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            user_id=current_user.id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('You have been logged out.', 'info')
    
    logout_user()
    return redirect(url_for('auth.login'))
