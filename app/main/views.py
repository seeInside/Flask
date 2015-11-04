from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main
from .forms import NameForm
from ..import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    
    name = None
    user = None
    form = NameForm()
    if form.validate_on_submit():
        new_name = form.name.data
        user = User.query.filter_by(username =
                                    form.name.data).first
        
        old_name = session.get('name')
        
        if user is None:
            user = User(username = new_name)
            session['user'] = user
            db.session.add(user)
            db.session.commit()
            session['know'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],
                           'NEW_USER',
                           'mail/new_user',
                           user = user)
        else:
            session['know'] = True
            if new_name != old_name:
                flash('looks like you change your name')
        
        session['name'] = new_name
        #this is a important code restore the data that in User class
        form.name.data = ''
        
        return redirect(url_for('main.index'))  #function()
        
    return render_template('index.html',
                           current_time = datetime.utcnow(),
                           form = form,
                           name = session.get('name'),
                           know = session.get('know', False),
                           user =session.get('user'))

@main.route('/re')
def relocation():
    return redirect('http://wwww.baidu.com')
