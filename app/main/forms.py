from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, \
     SelectField
from wtforms.validators import Required, Length, Email, Regexp
from flask.ext.pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField('What is your name?',
                       validators=[Required()])


class PostForm(Form):
    body = PageDownField("what's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class ProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('Submit')


class AdminEditProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('User name', validators=[Required(),
                                                      Length(1, 64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                             0,
                                                             'user name must has only letters')])
    
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', vlidators=[Required(), Length(1, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('about_me', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(AdminEditProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, filed):
        if field.data != self.user.email and \
           User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already in use!')

    def validate_username(self, field):
        if field.data != self.user.username and \
           User.query.filter_by(username = field.data).first():
            raise ValidationError('User name already in use!')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')
