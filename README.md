# Ubuntu Server Dashboard

A modern, comprehensive web-based dashboard for monitoring and managing Ubuntu server resources, built with Flask and a modular architecture. This professional-grade dashboard offers real-time system monitoring, advanced user management, service control, integrated terminal access, chat functionality, and comprehensive file management capabilities.

**🚀 Completely rewritten with modern Flask architecture, SQLAlchemy database integration, and professional security features!**

## Features

### 🔐 Advanced Authentication & User Management
- **Secure Login System**: Flask-Login with Werkzeug password hashing
- **Role-Based Access Control**: Administrator and User roles with different permissions
- **User Registration**: Admin can create new user accounts
- **Profile Management**: Users can update their information, email, and profile pictures
- **Session Management**: Secure session handling with logout functionality

### 📊 Real-Time System Monitoring
- **Live System Metrics**: CPU, Memory, Disk usage with color-coded indicators
- **Network Information**: Public/Private IP addresses, hostname display
- **System Uptime**: Server uptime tracking and display
- **Historical Data**: System metrics stored in database for trend analysis
- **Auto-Refresh Dashboard**: Real-time updates without page reload

### ⚙️ Advanced Service Management
- **Service Control Panel**: Start, stop, restart system services (Admin only)
- **Service Status Monitoring**: Real-time status of critical services
- **Common Services**: Pre-configured list of Ubuntu services
- **Command Logging**: All service actions logged in audit trail

### 💻 Integrated Web Terminal
- **Secure Command Execution**: Execute shell commands via web interface (Admin only)
- **Command History**: Track all executed commands
- **Security Controls**: Dangerous command blocking and timeout protection
- **Interactive Interface**: Terminal-like experience in browser

### 💬 Team Communication System
- **Live Chat**: Real-time messaging between users
- **Message History**: Persistent chat storage in database
- **User Attribution**: Messages linked to user accounts
- **Auto-Scroll**: Automatic scrolling to latest messages

### 📁 SMB File Management
- **File Browser**: Navigate SMB shares through web interface
- **File Download**: Direct download of files from SMB shares
- **Directory Navigation**: Browse folders and view file information
- **File Information**: Display file sizes, modification dates

### 👥 Administrative Features
- **User Management**: Add, edit, delete user accounts (Admin only)
- **Audit Logging**: Complete audit trail of all system actions
- **System Settings**: Configure application settings
- **Security Monitoring**: Track login attempts and user activities

## 🛠️ Technologies Used

### Backend Framework
- **Flask 2.3.3**: Modern Python web framework with blueprint architecture
- **SQLAlchemy 3.0.5**: Advanced ORM for database management
- **Flask-Login 0.6.2**: User session management and authentication
- **Flask-WTF 1.1.1**: Form handling with CSRF protection
- **Werkzeug 2.3.7**: Password hashing and security utilities

### Database & Storage
- **SQLite**: Lightweight, serverless database for production use
- **Database Models**: User, ChatMessage, AuditLog, SystemMetrics, ServiceStatus

### Security Features
- **Password Hashing**: Werkzeug secure password storage
- **CSRF Protection**: Flask-WTF token-based protection
- **Session Management**: Secure user sessions with Flask-Login
- **Audit Logging**: Complete action tracking and logging
- **Input Validation**: WTForms validation and sanitization

### System Integration
- **psutil 5.9.5**: Advanced system monitoring and resource statistics
- **subprocess**: Secure command execution with timeout protection
- **socket & requests**: Network information and HTTP requests

### Frontend Technologies
- **HTML5/CSS3**: Modern responsive web design
- **JavaScript**: Interactive dashboard features and real-time updates
- **Font Awesome**: Professional icon library
- **Ubuntu Color Scheme**: Authentic Ubuntu-themed interface

## 🚀 Installation and Setup

### Prerequisites
- **Python 3.8+**: Modern Python version required
- **pip**: Python package manager
- **Git**: Version control system
- **Ubuntu/Linux**: Optimized for Ubuntu server environments

### Quick Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ZentoxDeveloper/ubuntu-linux-dashboard.git
   cd ubuntu-server-dashboard
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```

4. **Access the Dashboard**:
   - Local: `http://localhost:5000`
   - Remote: `http://<server-ip>:5000`

### First Time Setup

1. **Default Admin Account**:
   - Username: `admin`
   - Password: `admin123`
   - **⚠️ Change this password immediately after first login!**

2. **Database Initialization**:
   - SQLite database is created automatically on first run
   - Default admin user is created if no users exist

### Advanced Configuration

#### Environment Variables
Create a `.env` file in the project root:
```bash
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
BASE_SMB_PATH=/path/to/smb/shares
```

#### Service Configuration
For service management functionality, configure sudo permissions:
```bash
# Add to /etc/sudoers.d/dashboard
www-data ALL=(ALL) NOPASSWD: /bin/systemctl start *, /bin/systemctl stop *, /bin/systemctl restart *, /bin/systemctl status *
```

#### Production Deployment
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 🔒 Security Features

### Authentication & Authorization
- **Secure Password Storage**: Werkzeug PBKDF2 password hashing with salt
- **Session Management**: Flask-Login secure session handling
- **Role-Based Access**: Admin and User roles with permission enforcement
- **Login Protection**: Session timeout and secure logout functionality

### Input Validation & Protection
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Input Sanitization**: WTForms validation and sanitization
- **Command Injection Prevention**: Whitelist-based command filtering
- **SQL Injection Protection**: SQLAlchemy ORM parameter binding

### Audit & Monitoring
- **Complete Audit Trail**: All user actions logged with timestamps
- **IP Address Tracking**: Login and action tracking by IP
- **User Agent Logging**: Device and browser information capture
- **Failed Login Monitoring**: Track and log authentication failures

### Production Security
- **Secret Key Management**: Environment variable configuration
- **Debug Mode Control**: Production-safe debug settings
- **Timeout Protection**: Command execution and request timeouts
- **Error Handling**: Secure error messages without information disclosure

## 🏗️ Project Architecture

### Modular Structure
```
📁 app/
├── 📁 admin/          # Administrative functionality
│   ├── __init__.py    # Blueprint initialization
│   └── routes.py      # User management, audit logs
├── 📁 auth/           # Authentication system
│   ├── __init__.py    # Blueprint initialization
│   └── routes.py      # Login, logout, registration
├── 📁 main/           # Core dashboard features
│   ├── __init__.py    # Blueprint initialization
│   └── routes.py      # Dashboard, chat, terminal, services
├── 📁 api/            # REST API endpoints
│   ├── __init__.py    # Blueprint initialization
│   └── routes.py      # JSON API for real-time data
├── 📁 utils/          # Utility modules
│   ├── __init__.py    # Package initialization
│   ├── system_info.py # System monitoring functions
│   └── file_manager.py # SMB file management
├── 📁 templates/      # Jinja2 HTML templates
│   ├── base.html      # Main layout template
│   ├── 📁 auth/       # Authentication templates
│   ├── 📁 main/       # Dashboard templates
│   └── 📁 admin/      # Administrative templates
├── __init__.py        # Application factory
├── models.py          # SQLAlchemy database models
└── forms.py           # WTForms form definitions

📁 Root Files:
├── run.py             # Application entry point
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
└── app.db            # SQLite database (created on first run)
```

### Database Schema
- **Users**: Authentication and profile information
- **ChatMessages**: Team communication history
- **AuditLog**: Complete action tracking
- **SystemMetrics**: Historical performance data
- **ServiceStatus**: Service monitoring data

## 🤝 Contributing

We welcome contributions to improve the Ubuntu Server Dashboard! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Create a Pull Request

### Contribution Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation for any changes
- Ensure security best practices
- Test on Ubuntu/Linux environments

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

**Free to use, modify, and distribute for personal and commercial projects.**

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/ZentoxDeveloper/ubuntu-linux-dashboard/issues)
- **Discussions**: [Community support and questions](https://github.com/ZentoxDeveloper/ubuntu-linux-dashboard/discussions)
- **Security Issues**: Please report security vulnerabilities privately

## 🚀 What's New in v2.0

### Major Updates (August 2025)
✅ **Complete Architecture Rewrite**: Modern Flask blueprint structure
✅ **Database Integration**: SQLAlchemy ORM with persistent storage
✅ **Enhanced Security**: CSRF protection, password hashing, audit logging
✅ **Advanced UI**: Professional Ubuntu-themed responsive interface
✅ **Real-time Features**: Live chat, auto-refreshing metrics
✅ **Production Ready**: Gunicorn support, environment configuration

### Previous Features Maintained
✅ **System Monitoring**: Enhanced with historical data storage
✅ **Service Management**: Improved with better error handling
✅ **File Management**: Enhanced SMB integration
✅ **User Management**: Complete admin interface overhaul

---

**🎉 Thank you for using Ubuntu Server Dashboard! Star ⭐ this repository if you find it useful!** 
