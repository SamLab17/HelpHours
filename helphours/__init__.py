from flask import Flask
from helphours.notifications import Notifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.jinja_env.auto_reload = True

db = SQLAlchemy(app)
login = LoginManager(app)

notifier = Notifier(app.config['EMAIL_ACCOUNT'],
                    app.config['EMAIL_PASSWORD'],
                    app.config['EMAIL_SERVER'],
                    app.config['EMAIL_SERVER_PORT'],
                    app.config['SEND_EMAILS'])

from helphours import routes    # noqa: F401
