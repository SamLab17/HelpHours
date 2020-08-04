import secrets
from helphours import app, db, notifier, queue_handler, routes_helper, password_reset, stats
from flask import render_template, url_for, redirect, request, g
from helphours.forms import JoinQueueForm, RemoveSelfForm, InstructorForm
from helphours.student import Student
from flask_login import current_user, login_required
from helphours.models.instructor import Instructor
from helphours.models.visit import Visit
from datetime import datetime
from werkzeug.security import generate_password_hash

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
            visit = Visit(eid=form.eid.data, time_entered=datetime.utcnow(), time_left=None,
                          was_helped=0, instructor_id=None)
            db.session.add(visit)
            db.session.commit()
            s = Student(form.name.data, form.email.data,
                        form.eid.data, visit.id)
            place = queue_handler.enqueue(s)
            notifier.send_message(form.email.data,
                                  f"Notification from {app.config['COURSE_NAME']} Lab Hours Queue",
                                  render_template("email/added_to_queue_email.html",
                                                  place_str=routes_helper.get_place_str(place),
                                                  student_name=form.name.data, remove_code=form.eid.data),
                                  'html')
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
    return render_template('view.html', queue=queue, queue_is_open=queue_is_open)


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


@app.route("/zoom", methods=['GET'])
def zoom_redirect():
    return redirect(app.config['DEFAULT_ZOOM_LINK'])


@app.route("/schedule", methods=['GET'])
def schedule_redirect():
    return redirect(app.config['SCHEDULE_LINK'])


@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.is_admin:
        return render_template('admin_panel.html', instructors=Instructor.query.all())
    else:
        return render_template('message_error.html', title="Admin Panel", body="Not authenticated, must be admin")


@app.route('/edit_instructor', methods=['GET', 'POST'])
@login_required
def edit_instructor():
    if current_user.is_admin:
        if 'id' not in request.args:
            return render_template('message_error.html', title="Error", body="Missing instructor id")
        instr = Instructor.query.filter_by(id=request.args['id']).first()
        if request.method == 'GET':
            if instr is None:
                return render_template('message_error.html', title="Error", body="Invalid instructor id")
            form = InstructorForm(first_name=instr.first_name, last_name=instr.last_name, email=instr.email, is_active=(
                instr.is_active != 0), is_admin=(instr.is_admin != 0))
            return render_template('edit_instructor.html',
                                   title="Edit Instructor",
                                   form=form, message='', id=instr.id)
        else:
            form = InstructorForm()
            if form.validate_on_submit():
                instr.first_name = form.first_name.data
                instr.last_name = form.last_name.data
                instr.email = form.email.data
                instr.is_active = 1 if form.is_active.data else 0
                instr.is_admin = 1 if form.is_admin.data else 0
                db.session.commit()
                return redirect('admin_panel')
            else:
                message = 'Enter a valid email address'
                return render_template('edit_instructor.html',
                                       title="Edit Instructor",
                                       form=form,
                                       message=message)
    else:
        return render_template('reset_message.html', title="Edit user", body="Not authenticated")


@app.route('/add_instructor', methods=['GET', 'POST'])
@login_required
def add_instructor():
    if current_user.is_admin:
        message = ''
        if request.method == 'GET':
            form = InstructorForm(is_active=True)
            return render_template('edit_instructor.html',
                                   title="Create Instructor", form=form,
                                   message=message)
        else:
            form = InstructorForm()
            if form.validate_on_submit():
                instr = Instructor()
                instr.first_name = form.first_name.data
                instr.last_name = form.last_name.data
                instr.email = form.email.data
                instr.is_active = 1 if form.is_active.data else 0
                instr.is_admin = 1 if form.is_admin.data else 0
                instr.password_hash = generate_password_hash(
                    secrets.token_urlsafe(20))
                db.session.add(instr)
                db.session.commit()
                password_reset.new_user(instr)
                return redirect('admin_panel')
            else:
                message = 'Enter a valid email address'
    else:
        return render_template('reset_message.html', title="Edit user",
                               body="Not authenticated")


@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats_page():
    if 'range' not in request.args:
        range = "all"
    else:
        range = request.args['range']
    return stats.get_graphs(range)


# noqa: F401 == Ignore rule about unused imports
from helphours import automated_routes  # noqa: F401
from helphours import error_routes  # noqa: F401
from helphours import account_routes    # noqa: F401
