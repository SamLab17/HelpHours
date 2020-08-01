from flask import Flask
from helphours.notifications import Notifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.jinja_env.auto_reload = True

from helphours import routes