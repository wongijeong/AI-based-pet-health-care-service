import os
from flask import render_template, url_for, flash
from flask_wtf import FlaskForm
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import wtforms
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from __init__ import login_manager
import __init__

DB_USER = os.environ.get("DB_USER")
DB_PW = os.environ.get("DB_PW")
# Personal Setting***************************************************
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1234@127.0.0.1:3306/users")
# *********************************************************

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

Base = sqlalchemy.orm.declarative_base()

class User(UserMixin, Base):
	__tablename__ = 'info'
	id = sqlalchemy.Column(sqlalchemy.String(length=100), primary_key=True)
	email = sqlalchemy.Column(sqlalchemy.String(64), unique=True, index=True)
	password = sqlalchemy.Column(sqlalchemy.String(length=100))
	password_hash = sqlalchemy.Column(sqlalchemy.String(128))
	profile_pic = sqlalchemy.Column(sqlalchemy.String(128))
	name = sqlalchemy.Column(sqlalchemy.String(64))
#	role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'))

	def __init__(self, id, name, email, profile_pic, password):
		self.id=id
		self.name=name
		self.email=email
		self.profile_pic = profile_pic
		self.password = password

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')	

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	# 패스워드 확인
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

Base.metadata.create_all(engine)

class RegisterForm(FlaskForm):
	id = StringField(validators=[InputRequired(), Length(
				min=4, max=20)], render_kw={"placeholder": "User ID"})
	name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "User name"})
	password = PasswordField(validators=[InputRequired(), Length(
				min=4, max=30),  EqualTo('pwd_confirm', message=											'패스워드가 일치하지 않습니다.')],
				render_kw={"placeholder": "Password"})
	pwd_confirm = PasswordField(validators=[InputRequired(), Length(
				min=4, max=30)], render_kw={"placeholder": "Confirm Password"													})
	email = StringField(validators=[InputRequired(), Length(min=4, max=40)],
				render_kw={"placeholder": "E-mail"}) 
	submit = SubmitField("가입하기")

	def validate_email(self, field):
		existing_email = session.query(User).filter_by(
						email=field.data).first()
		if existing_email:
			flash('이메일이 이미 존재합니다.')
			raise ValidationError(
			"E-mail alreay exists. Try another one.") 

	def validate_id(self, field):
		existing_id = session.query(User).filter_by(
						id=field.data).first()
		if existing_id:
			flash('ID가 이미 존재합니다.')
			raise ValidationError(
				"ID already exists. Try another one.")

class LoginForm(FlaskForm):
	id = StringField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={"placeholder": "User ID"})
	password = PasswordField(validators=[InputRequired(), Length(
                min=4, max=20)], render_kw={"placeholder": "Password"})
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField("Login")

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def addUser(id, password):
	newUser = User(id = id, password = password)
	session.add(newUser)
	session.commit()

def deleteUser(id):
	session.query(User).filter(User.id == id).delete()
	session.commit()

def load_shopping(): # 상품 테이블 전체 튜플 반환
	return session.query(item).filter_by()

def load_recommend_hit(): # 상품 테이블의 조회수 높은 순서대로 모든 튜플 반환 
	return session.query(item).filter_by().order_by(item.hit.desc())

# def load_recommend_hit_genus(): # 상품 테이블의 조회수가 높은 순서 + 유저의 펫의 종류가 같은 모든 튜플 반환 
# 	return session.query(item).filter_by(item.Genus == session.query(pet.type).filter_by(User.id == pet.owner_id)).order_by(item.hit.desc())

# This function is not working ... !
def updateUserPassword(id, password):
	user = session.query(User).filter(User.id == id)
	user.password = password
	session.add(user) 
	session.commit()

def selectAll():
   users = session.query(User).all()
   for user in users:
       print(" - " + user.id + ' ' + user.password)

       
class cart(Base): # 테이블 생성
	__tablename__ = 'cart'
	id = sqlalchemy.Column(sqlalchemy.String(length=100), primary_key=True)
	item_num = sqlalchemy.Column(sqlalchemy.Integer())
Base.metadata.create_all(engine)

class purchase(Base): # 테이블 생성
	__tablename__ = 'purchase'
	purchase_id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
	id = sqlalchemy.Column(sqlalchemy.String(length=100))
	item_num = sqlalchemy.Column(sqlalchemy.Integer())
Base.metadata.create_all(engine)

class pet(Base): # 테이블 생성
	__tablename__ = 'pet'
	pet_id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True, autoincrement=True) # 고유번호
	owner_id = sqlalchemy.Column(sqlalchemy.String(length=100))  #2023-05-24 추가함
	image = sqlalchemy.Column(sqlalchemy.String(length=200)) #저장할 이미지 이름, 이미지 파일 자체는 static/uploads에 저장함
	name = sqlalchemy.Column(sqlalchemy.String(length=50))
	type = sqlalchemy.Column(sqlalchemy.String(length=50)) #펫 종류
	gender = sqlalchemy.Column(sqlalchemy.String(length=50))
	age_years = sqlalchemy.Column(sqlalchemy.Integer())
	age_months = sqlalchemy.Column(sqlalchemy.Integer())
	weight = sqlalchemy.Column(sqlalchemy.Float())
	neuter = sqlalchemy.Column(sqlalchemy.CHAR()) #중성화 여부
Base.metadata.create_all(engine)
	
class item(Base): # 테이블 생성
	__tablename__ = 'item'
	item_num = sqlalchemy.Column(sqlalchemy.BigInteger(), primary_key=True)
	item_name = sqlalchemy.Column(sqlalchemy.String(length=1000)) # 상품 이름
	price = sqlalchemy.Column(sqlalchemy.String(length=1000)) # 상품 가격
	Genus = sqlalchemy.Column(sqlalchemy.String(length=1000)) #속 전용 용품 분류
	description = sqlalchemy.Column(sqlalchemy.String(length=1000)) # 상품 설명
	hit = sqlalchemy.Column(sqlalchemy.Integer()) #조회수
	site_link = sqlalchemy.Column(sqlalchemy.String(length=1000)) # 상품 하이퍼링크 주소
Base.metadata.create_all(engine)


#addUser("user1", "user1234")
#deleteUser("user1")
#updateUserPassword("user1", "user3456")
