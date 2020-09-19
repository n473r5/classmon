from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_json("./config/site.json")

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)

from .api import api

app.register_blueprint(api, url_prefix="/api")

from .views import *
from .models import User

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))