from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import bp
from app.models import ChatMessage, SystemMetrics, ServiceStatus, User
from app import db
from datetime import datetime, timedelta

try:
    from app.utils.system_info import get_system_info, get_service_status
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

@bp.route('/system_info')
@login_required
def system_info():
    """Get current system information"""
    info = get_system_info()
    
    # Store metrics in database
    metrics = SystemMetrics(
        cpu_percent=info['cpu_percent'],
        memory_percent=info['memory_percent'],
        disk_percent=info['disk_percent'],
        network_bytes_sent=info.get('network_bytes_sent', 0),
        network_bytes_recv=info.get('network_bytes_recv', 0),
        load_average=info.get('load_average', '')
    )
    db.session.add(metrics)
    db.session.commit()
    
    return jsonify(info)

@bp.route('/chat_messages')
@login_required
def chat_messages():
    """Get recent chat messages"""
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).limit(20).all()
    return jsonify([msg.to_dict() for msg in reversed(messages)])

@bp.route('/service_status/<service_name>')
@login_required
def service_status(service_name):
    """Get status of a specific service"""
    status = get_service_status(service_name)
    
    # Update database
    service = ServiceStatus.query.filter_by(service_name=service_name).first()
    if not service:
        service = ServiceStatus(service_name=service_name)
        db.session.add(service)
    
    service.status = status
    service.last_checked = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'service': service_name,
        'status': status,
        'last_checked': service.last_checked.isoformat()
    })

@bp.route('/metrics/history')
@login_required
def metrics_history():
    """Get historical system metrics"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    hours = request.args.get('hours', 24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    metrics = SystemMetrics.query.filter(
        SystemMetrics.timestamp >= since
    ).order_by(SystemMetrics.timestamp.asc()).all()
    
    return jsonify([metric.to_dict() for metric in metrics])

@bp.route('/user_activity')
@login_required
def user_activity():
    """Get current user activity statistics"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    from app.models import User, AuditLog
    
    # Count active users (logged in within last 24 hours)
    since = datetime.utcnow() - timedelta(hours=24)
    active_users = User.query.filter(User.last_login >= since).count()
    total_users = User.query.count()
    
    # Recent audit logs
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    
    return jsonify({
        'active_users': active_users,
        'total_users': total_users,
        'recent_activity': [log.to_dict() for log in recent_logs]
    })

@bp.route('/dashboard_stats')
@login_required
def dashboard_stats():
    """Get dashboard statistics"""
    stats = {
        'system_info': get_system_info(),
        'openvpn_status': get_service_status('openvpn'),
        'squid_status': get_service_status('squid'),
        'chat_message_count': ChatMessage.query.count(),
        'user_count': User.query.count() if current_user.is_admin() else None
    }
    
    return jsonify(stats)
