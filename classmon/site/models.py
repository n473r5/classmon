from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import app, db

class User(UserMixin, db.Model):
	__tablename__ = "users"
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(64))
	data_sources = db.Column(db.String(1024))

	def check_password(self, string):
		return check_password_hash(self.password_hash, string)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	@property
	def is_admin(self):
		return self.username in app.config["ADMINISTRATORS"]

	def __repr__(self):
		return "<user \"{}\" id {}>".format(self.username, self.id)