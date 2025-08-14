# Ubuntu Server Dashboard - Quick Start Guide

Een geavanceerd web-gebaseerd dashboard voor Ubuntu Server management.

## 🚀 Snelle Start

### 1. Dependencies installeren
```bash
pip install -r requirements.txt
```

### 2. Applicatie starten
```bash
python start.py
```

**Of gebruik het originele script:**
```bash
python app.py
```

### 3. Open in browser
- **URL**: http://localhost:5000
- **Username**: admin  
- **Password**: admin123

⚠️ **Belangrijk**: Wijzig het standaard wachtwoord na de eerste login!

## ✨ Functies

- **🔐 Gebruikersbeheer**: Veilige authenticatie met rol-gebaseerde toegang
- **📊 Systeemmonitoring**: Real-time CPU, geheugen, schijf en netwerkstatistieken  
- **⚙️ Servicebeheer**: Beheer van systemd services (OpenVPN, Squid, etc.)
- **💬 Live Chat**: Real-time communicatie tussen gebruikers
- **📁 SMB Share Browser**: Bekijk en download bestanden van SMB shares
- **📝 Audit Logging**: Volledige logging van gebruikersacties
- **💻 Command Line Interface**: Veilige commandoregel voor administrators
- **🔌 API Endpoints**: RESTful API voor externe integratie

## 🛠️ Troubleshooting

### Import Errors
```bash
pip install email-validator psutil requests flask-sqlalchemy flask-login flask-wtf
```

### Database Issues
```bash
# Reset database
rm instance/dashboard.db  # Linux/Mac
del instance\dashboard.db  # Windows
python app.py  # Will recreate
```

### Test Dependencies
```bash
python test_imports.py
```

## 📁 Project Structuur

```
app/
├── __init__.py              # Flask app factory
├── models.py                # Database modellen  
├── forms.py                 # WTF formulieren
├── auth/                    # Authenticatie module
├── main/                    # Hoofddashboard
├── admin/                   # Admin interface  
├── api/                     # REST API
├── utils/                   # Utility functies
└── templates/               # HTML templates
```

## 🔧 Configuratie

Environment variabelen in `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///dashboard.db
SMB_PATH=/mnt/smb
```

## 🚀 Productie Deployment

```bash
# Met Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Met systemd (Linux)
sudo cp ubuntu-dashboard.service /etc/systemd/system/
sudo systemctl enable ubuntu-dashboard
sudo systemctl start ubuntu-dashboard
```

## 🆘 Support

Voor problemen:
1. Controleer dat alle dependencies geïnstalleerd zijn
2. Controleer de `.env` configuratie  
3. Test met `python test_imports.py`
4. Gebruik `python start.py` voor uitgebreide error handling
