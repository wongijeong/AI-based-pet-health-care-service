from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import * 
from ..database_model import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verity_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startwith('/'):
				next = url_for('main.index')
			return redirect(next)
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)
