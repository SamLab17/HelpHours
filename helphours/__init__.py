from flask import Flask
from helphours.notifications import Notifier
from helphours.logger import Logger
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.jinja_env.auto_reload = True

# Default DUAL_MODAILTY option to false.
if 'DUAL_MODALITY' not in app.config:
    app.config['DUAL_MODALITY'] = False

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

from helphours import queue_handler
from helphours import routes    # noqa: F401
import pickle

try:
    with open(app.config['QUEUE_FILE'], "rb") as openfile:
        load_data = pickle.load(openfile)
        routes.queue_is_open = load_data[0]
        student_queue = load_data[1]
        for student in student_queue:
            queue_handler.enqueue(student)
except:  # noqa: E722
    log.info('Error while loading last queue state')
    pass


def save_queue(sender, **args):
    try:
        with open(app.config['QUEUE_FILE'], "wb") as file:
            dump_data = (routes.queue_is_open, queue_handler.get_students())
            pickle.dump(dump_data, file)
    except:  # noqa: E722
        log.info('Error while writing last queue state')
        pass


from flask import appcontext_tearing_down
appcontext_tearing_down.connect(save_queue, app)
