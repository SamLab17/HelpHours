from helphours import app, db, notifier, queue_handler, routes_helper
from flask import render_template, flash, url_for, redirect, request, g
from helphours.forms import JoinQueueForm, RemoveSelfForm, ResetPasswordForm, RequestResetForm, InstructorForm, LoginForm
from helphours.student import Student
from flask_login import current_user, login_user, logout_user, login_required
from helphours.models.instructor import Instructor
from helphours.models.visit import Visit
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
import validators
import json
import secrets

# Would likely need to be stored in a databse if we want multiple instances of this
# running
queue_is_open = False

@app.before_request
def load_user():
    g.user = current_user

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
            visit = Visit(eid=form.eid.data, time_entered=datetime.utcnow(), time_left=None, was_helped=0, instructor_id=None)
            db.session.add(visit)
            db.session.commit()
            s = Student(form.name.data, form.email.data, form.eid.data, visit.id)
            place = queue_handler.enqueue(s)
            notifier.send_message(form.email.data, "Notification from 314 Lab Hours Queue", 
            render_template("email/added_to_queue_email.html", place_str=routes_helper.get_place_str(place), 
            student_name=form.name.data, remove_code=form.eid.data), 'html')
            return redirect(url_for('view'))
        else:
            if len(form.errors) > 0:
                message = next(iter(form.errors.values()))[0]
    # render the template for submitting otherwise
    return render_template('join.html', form=form, queue_is_open=queue_is_open, message=message)

@app.route("/view", methods=['GET', 'POST'])
def view():
    global queue_is_open
    if request.method == "POST" and current_user.is_authenticated:
        queue_is_open = routes_helper.handle_line_form(request, queue_is_open)
    queue = queue_handler.get_students()
    s1 = Student("John Doe", "example@example.com", "jd1234", 42)
    s2 = Student("Jane Doe", "example@example.com", "jd1234", 42)
    s3 = Student("A longer name", "example@example.com", "jd1234", 42)
    return render_template('view.html', queue=[s1, s2, s3], queue_is_open=queue_is_open)

@app.route("/remove", methods=['GET', 'POST'])
def remove():
    form = RemoveSelfForm()
    message = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            # remove em
            s = queue_handler.remove_eid(request.form['eid'])
            if s is None:
                v = Visit.query.filter_by(id=s.id).first()
                if v is not None:
                    v.time_left = datetime.utcnow()
                    v.was_helped = 0
                    db.session.commit()
                else:
                    # Log Error, Assertion failed
                    pass
                return redirect(url_for('view'))
            else:
                message = "EID not found in queue"
        else:
            message = "EID is required"
    return render_template('remove.html', form=form, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view'))
    form = LoginForm()
    message = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Instructor.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                message = "Incorrect email or password"
            elif not user.is_active:
                message = "This account is inactive"
            else:
                login_user(user, remember=False)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('view')
                return redirect(next_page)
        else:
            message = "Please enter a valid email"
    return render_template('login.html', form=form, message=message)


@app.route("/zoom", methods=['GET'])
def zoom_redirect():
    return redirect(app.config['DEFAULT_ZOOM_LINK'])

@app.route("/schedule", methods=['GET'])
def schedule_redirect():
    return redirect(app.config['SCHEDULE_LINK'])

from helphours import error_routes