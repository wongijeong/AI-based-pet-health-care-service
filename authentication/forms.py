from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..forest_animal import database_model 

class LoginForm(FlaskForm):
    id = StringField(validators=[InputRequired(), Length(
                min=4, max=20)], render_kw={"placeholder": "User ID"})
    password = PasswordField(validators=[InputRequired(), Length(
                min=4, max=20)], render_kw={"placeholder": "Password"})
    #remember_me = BooleanField('Keep me logged in')
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
	email = StringField('Email', validator=[DataRequired(), Length(1, 64),
							Email()])
	username = StringField('Username', validators=[DataRequired(),
							Length(1, 64),
		Regexp('^[A-Za-z[A-Za-z0-9_.]*$', 0,
			'Usernames must have only letters, numbers, dots or '
			'underscores')])
password = PAsswordField('Password', validators=[
			DataRequired(), EqualTo('password2', message='Passwords must math.')])
password2 = PasswordField('Confirm password', validators=[DataRequired()])
submit = SubmitField('Register')

def validate_email(self, field):
	if User.query.filter_by(email=field.data).first():
		raise ValidationError('Email already registered.')

def validate_username(self, field):
	if User.query.filter_by(username=field.data).frist():
		raise ValidationError('Username already in use.')
