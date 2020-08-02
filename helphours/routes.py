from helphours import app
from flask import render_template, flash, url_for, redirect, request, g
# from helphours.forms import EnterLineForm, LoginForm, RequestResetForm, ResetPasswordForm, InstructorForm
from helphours.forms import JoinQueueForm
# from helphours.student import Student
from flask_login import current_user, login_user, logout_user, login_required
# from helphours.models.instructor import Instructor
# from helphours.models.visit import Visit
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
import validators
import json
import secrets

# Would likely need to be stored in a databse if we want multiple instances of this
# running
queue_is_open = False

@app.context_processor
def course_info():
    return dict(COURSE_NAME=app.config['COURSE_NAME'], COURSE_DESCRIPTION=app.config['COURSE_DESCRIPTION'])

@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/join", methods=['GET', 'POST'])
def join():
    form = JoinQueueForm()
    message = ""
    if not queue_is_open and request.method == 'POST':
        message = "Sorry, the queue was closed."
    else: 
        # go to the page that shows the people in the queue if you've submitted
        # a valid form
        if form.validate_on_submit():
            pass
            # visit = Visit(eid=form.eid.data, time_entered=datetime.utcnow(), time_left=None, was_helped=0, instructor_id=None)
            # db.session.add(visit)
            # db.session.commit()
            # s = Student(form.name.data, form.email.data, form.eid.data, visit.id)
            # place = queue_handler.enqueue(s)
            # flash(f'{form.name.data} has been added to the queue!', 'success')
            # try:
            #     notifier.send_message(form.email.data, "Notification from 314 Lab Hours Queue", 
            #     render_template("added_to_queue_email.html", place_str=routes_helper.get_place_str(place), 
            #     student_name=form.name.data, remove_code=form.eid.data), 'html')
            # except Exception as e:
            #     print(f"Failed to send email to {form.email.data}\n{e}")
            # return redirect(url_for('view_line'))
        else:
            if len(form.errors) > 0:
                message = next(iter(form.errors.values()))[0]
    # render the template for submitting otherwise
    return render_template('join.html', form=form, queue_is_open=queue_is_open, message=message)


@app.route("/zoom", methods=['GET'])
def zoom_redirect():
    return redirect("https://www.zoom.us")

@app.route("/schedule", methods=['GET'])
def schedule_redirect():
    return redirect(app.config['SCHEDULE_LINK'])

from helphours import error_routes