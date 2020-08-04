from helphours import app, password_reset
from helphours.forms import LoginForm, RequestResetForm, ResetPasswordForm
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user
from helphours.models.instructor import Instructor
from werkzeug.urls import url_parse


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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('join'))


@app.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    form = RequestResetForm()
    message = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            form_email = form.email.data
            user = Instructor.query.filter_by(email=form_email).first()
            if user is None:
                message = "Not a valid email address"
                return render_template('request_reset.html', form=form, message=message)
            else:
                # This is a valid user/email address
                password_reset.create_reset_request(user)
                return render_template('message_info.html', title="Reset Request Made",
                                       body=f"Instructions for resetting your password have been sent to {form_email}")
        else:
            message = "Enter a valid email"

    return render_template('reset.html', form=form, message=message)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    message = ''
    if 'token' in request.args:
        if request.method == 'POST':
            if form.validate_on_submit():
                if password_reset.update_password(request.args['token'], form.password.data):
                    return render_template('message_info.html', title="Password reset",
                                           body="Your password was successfully updated")
                else:
                    return render_template('message_error.html', title="Reset error",
                                           body="The reset link is no longer valid.")
            else:
                message = 'Both passwords must match'
        return render_template('reset_password.html', token=request.args['token'], form=form, message=message)
    else:
        return render_template('message_error.html', title="Reset error",
                               body="Malformed reset link. Token not present")
