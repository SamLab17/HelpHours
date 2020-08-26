from helphours import db, notifier, app, log
from flask import url_for, render_template
import secrets
import datetime as dt
from werkzeug.security import generate_password_hash
from helphours.models.instructor import Instructor

NUM_HOURS_EXPIRE = 24

reset_requests = {}


def create_reset_request(user):
    token = secrets.token_urlsafe(20)
    while token in reset_requests.keys():
        token = secrets.token_urlsafe(20)
    reset_link = app.config["WEBSITE_LINK"] + url_for('reset_password', token=token)
    notifier.send_message(user.email, app.config['COURSE_NAME'] + " Help Hours Password Reset",
                          render_template('email/reset_password_email.html', reset_link=reset_link),
                          'html')
    expire_time = dt.datetime.utcnow() + dt.timedelta(hours=NUM_HOURS_EXPIRE)
    reset_requests[token] = (expire_time, user.id)
    log.info(f'{user.first_name} {user.last_name} requested to reset their password.')


def new_user(user):
    token = secrets.token_urlsafe(20)
    while token in reset_requests.keys():
        token = secrets.token_urlsafe(20)
    reset_link = app.config["WEBSITE_LINK"] + url_for('reset_password', token=token)
    notifier.send_message(user.email, "New " + app.config['COURSE_NAME'] + " Help Hours Instructor Account",
                          render_template('email/new_user_email.html', reset_link=reset_link),
                          'html')
    expire_time = dt.datetime.utcnow() + dt.timedelta(hours=NUM_HOURS_EXPIRE)
    reset_requests[token] = (expire_time, user.id)


def update_password(token, new_password):
    if token in reset_requests.keys():
        (expire_time, userid) = reset_requests[token]
        del reset_requests[token]
        if expire_time > dt.datetime.utcnow():
            # Valid token, time not expired
            new_hash = generate_password_hash(new_password)
            user = Instructor.query.filter_by(id=userid).first()
            user.password_hash = new_hash
            log.info(f'{user.first_name} {user.last_name} reset their password.')
            db.session.commit()
            return True
        else:
            return False
    else:
        return False
