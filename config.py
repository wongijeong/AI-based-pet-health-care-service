import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	DB_USER = os.environ.get('DB_USER')
	DB_PW = os.environ.get('DB_PW')
	GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
	GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
	GOOGLE_DISCOVERY_URL = (
		"https://accounts.google.com/.well-known/openid-configuration"
)

	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

config = {
	'development' : DevelopmentConfig,

	'default' : DevelopmentConfig
}
