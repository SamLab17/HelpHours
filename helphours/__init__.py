from flask import Flask
from helphours.notifications import Notifier
from helphours.logger import Logger
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.jinja_env.auto_reload = True

db = SQLAlchemy(app)

login = LoginManager(app)

# Creates an empty database
# from helphours.models.instructor import Instructor
# from helphours.models.visit import Visit
# from helphours.models.zoom_link import ZoomLink
# db.create_all()
# db.session.commit()

notifier = Notifier(app.config['EMAIL_ACCOUNT'],
                    app.config['EMAIL_PASSWORD'],
                    app.config['EMAIL_SERVER'],
                    app.config['EMAIL_SERVER_PORT'],
                    app.config['SEND_EMAILS'])

log = Logger(email_notifier=notifier,
             admin_emails=app.config['ADMIN_EMAILS'],
             log_file=app.config['LOG_FILE'],
             log_level=Logger.LEVEL_DEBUG)

log.info('Help Hours application starting...')

notifier.set_log(log)

from helphours import routes    # noqa: F401
