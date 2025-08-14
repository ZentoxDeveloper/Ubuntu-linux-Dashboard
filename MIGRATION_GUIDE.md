# Ubuntu Server Dashboard - Nieuwe Architectuur

## Wat er veranderd is

Je originele `app.py` bestand is volledig herstructureerd naar een professionele, modulaire Flask applicatie. Hier zijn de belangrijkste verbeteringen:

## ✨ Nieuwe Features

### 🏗️ Modulaire Architectuur
- **Blueprints**: Code is opgesplitst in logische modules (auth, main, admin, api)
- **Database**: SQLAlchemy ORM in plaats van in-memory dictionaries
- **Configuration**: Environment-based configuratie
- **Security**: Flask-Login, CSRF protection, input validation

### 🛡️ Beveiliging
- **Wachtwoord hashing**: Werkzeug password hashing
- **Session management**: Flask-Login voor gebruikerssessies
- **CSRF bescherming**: Flask-WTF CSRF tokens
- **Input validatie**: WTForms voor formuliervalidatie
- **Audit logging**: Volledige logging van gebruikersacties

### 💾 Database Integratie
- **SQLite database**: Vervang van in-memory dictionaries
- **Models**: User, ChatMessage, AuditLog, SystemMetrics, ServiceStatus
- **Migraties**: Automatische database schema management

### 🎨 Modern UI
- **Responsive design**: Mobile-friendly interface
- **Ubuntu theming**: Officiële Ubuntu kleuren en stijl
- **Real-time updates**: AJAX voor live data
- **Font Awesome icons**: Professionele iconografie

### 📊 Geavanceerde Monitoring
- **Historische data**: Opslag van systeemmetrieken over tijd
- **Service monitoring**: Automatische service status tracking
- **Performance charts**: Mogelijkheid voor grafieken en trends

## 📁 Nieuwe Bestands Structuur

```
Ubuntu-linux-Dashboard-main/
├── app/                     # Hoofdapplicatie
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # Database modellen
│   ├── forms.py            # WTForms formulieren
│   ├── auth/               # Authenticatie module
│   ├── main/               # Hoofddashboard
│   ├── admin/              # Administrator interface
│   ├── api/                # REST API endpoints
│   ├── utils/              # Utility functies
│   └── templates/          # Jinja2 templates
├── config.py               # Configuratieklassen
├── app.py                  # Applicatie entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variabelen
├── install.sh             # Installatiescript
└── ubuntu-dashboard.service # Systemd service file
```

## 🚀 Hoe te gebruiken

### 1. Installeer dependencies
```bash
pip install -r requirements.txt
```

### 2. Configureer environment
```bash
cp .env.example .env
# Bewerk .env met je instellingen
```

### 3. Start de applicatie
```bash
python app.py
```

### 4. Login
- **URL**: http://localhost:5000
- **Username**: admin
- **Password**: admin123

## 🔧 Configuratie Opties

### Environment Variabelen (.env)
```env
FLASK_ENV=development        # development/production
SECRET_KEY=your-secret-key   # Wijzig dit!
DATABASE_URL=sqlite:///dashboard.db
SMB_PATH=/mnt/smb
MAIN_LOGO_URL=https://your-logo.com/logo.png
```

## 📡 API Endpoints

### Systeem Informatie
- `GET /api/system_info` - Huidige systeemstatus
- `GET /api/metrics/history` - Historische data
- `GET /api/dashboard_stats` - Dashboard overzicht

### Services
- `GET /api/service_status/<service>` - Service status
- `POST /admin/control_service` - Service beheer

### Chat & Gebruikers
- `GET /api/chat_messages` - Chat berichten
- `POST /main/send_message` - Verstuur bericht
- `GET /api/user_activity` - Gebruikersactiviteit

## 🛠️ Development

### Database Migraties
De database wordt automatisch aangemaakt bij de eerste start. Voor wijzigingen:

```python
# In Python shell
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

### Custom Configuratie
Maak een nieuwe configuratieklasse in `config.py`:

```python
class MyConfig(Config):
    # Je custom instellingen
    pass
```

### Nieuwe Features Toevoegen
1. Maak een nieuwe blueprint in `app/`
2. Definieer routes in `routes.py`
3. Registreer in `app/__init__.py`

## 🔒 Productie Deployment

### Met Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Met Systemd
```bash
sudo cp ubuntu-dashboard.service /etc/systemd/system/
sudo systemctl enable ubuntu-dashboard
sudo systemctl start ubuntu-dashboard
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm instance/dashboard.db
python app.py  # Will recreate
```

### Permission Issues
```bash
# Zorg voor juiste permissies
sudo chown -R $USER:$USER .
chmod +x app.py install.sh
```

### Service Control Issues
```bash
# Zorg dat gebruiker sudo rechten heeft voor systemctl
sudo usermod -aG sudo $USER
```

## 🔄 Migratie van Oude Code

Je oude code werkt niet meer omdat:
1. Geen Flask app object beschikbaar
2. Geen imports van Flask modules
3. Templates zijn verplaatst naar modulaire structuur
4. Database structuur is veranderd

Om oude functionaliteit te behouden, bekijk de nieuwe routes in:
- `app/main/routes.py` - Dashboard functionaliteit
- `app/admin/routes.py` - Administratie functies
- `app/api/routes.py` - API endpoints

## 📚 Verder Leren

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)

## 🤝 Bijdragen

De nieuwe architectuur maakt het veel eenvoudiger om nieuwe features toe te voegen. Volg de modulaire structuur en maak gebruik van de bestaande patterns.
