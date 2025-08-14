from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(1, 64),
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(),
        Length(1, 120)
    ])
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(1, 100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(8, 128)
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[
        ('User', 'User'),
        ('Administrator', 'Administrator')
    ], default='User')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different email.')

class EditProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(1, 100)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 120)
    ])
    profile_image_url = StringField('Profile Image URL', validators=[
        Length(0, 255)
    ])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[
        Length(0, 128)
    ])
    new_password2 = PasswordField('Repeat New Password', validators=[
        EqualTo('new_password', message='Passwords must match')
    ])
    
    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please choose a different email.')

class ChatMessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(1, 500)
    ])

class CommandForm(FlaskForm):
    command = StringField('Command', validators=[
        DataRequired(),
        Length(1, 255)
    ])

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 120)
    ])
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(1, 100)
    ])
    role = SelectField('Role', choices=[
        ('User', 'User'),
        ('Administrator', 'Administrator')
    ])
    is_active = BooleanField('Active')
    reset_password = BooleanField('Reset Password')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please choose a different email.')

class ServiceControlForm(FlaskForm):
    action = SelectField('Action', choices=[
        ('start', 'Start'),
        ('stop', 'Stop'),
        ('restart', 'Restart'),
        ('enable', 'Enable'),
        ('disable', 'Disable')
    ], validators=[DataRequired()])
    service = StringField('Service', validators=[DataRequired()])
