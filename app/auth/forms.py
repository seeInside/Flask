from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class LoginForm(Form):
    email = StringField('Email', validators = [Required(), Length(1, 64),
                                               Email()])
    password = PasswordField('Password', validators=[Required()])
    rember_me = BooleanField('Keep me Logged in')
    submit = SubmitField('Log')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64),
                                             Email()])
    username = StringField('UserName', validators = [Required(),
                                                     Length(1, 64),
                                                     Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                            0, 'username must have only letters')])
    password = PasswordField('Password', validators = [Required(),
                                                       EqualTo('password2',
                                                               message = 'Password must match')])
    password2 = PasswordField('Confirm password', validators = [Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already register')
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use')

