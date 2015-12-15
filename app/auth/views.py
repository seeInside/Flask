from flask import render_template, redirect, request, url_for, flash, request
from flask.ext.login import login_user, login_required, logout_user, current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from ..models import User
from .forms import LoginForm, RegistrationForm
from . import auth
from app import db

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can Login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        #if request.endpoint[:5] != 'auth.':
            #redirect(url_for('auth.login'))
    else:
        pass
    
        

