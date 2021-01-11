from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from helphours.models.zoom_link import ZoomLink
import validators


class JoinQueueForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=32, message="Please limit name entry to 32 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    eid = StringField('EID', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z0-9]+$', message="Please only enter alphanumeric characters for EID field")
    ])
    desc = StringField('Short Problem Description', validators=[
        DataRequired()
    ])
    submit = SubmitField('Join the Queue!')


class RemoveSelfForm(FlaskForm):
    eid = StringField('EID', validators=[
        DataRequired()
    ])
    submit = SubmitField('Remove self')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Sign In')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Send Reset Instructions')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[
        DataRequired(),
        EqualTo('confirm', message='The two passwords must match')
    ])
    confirm = PasswordField('Confirm new password')
    submit = SubmitField('Reset Password')


class InstructorForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired()
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    is_active = BooleanField('Active')
    is_admin = BooleanField('Admin')
    submit = SubmitField('Update')


class AddZoomLinkForm(FlaskForm):
    def check_valid_url(form, field):
        if not validators.url(form.url.data):
            raise ValidationError(f'Invalid url: {form.url.data}')

    description = StringField('Description', validators=[
        DataRequired()
    ])
    url = StringField('Zoom Link', validators=[
        DataRequired(),
        check_valid_url
    ])
    day = SelectField('Day', choices=[
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (0, 'Other')
    ])
    submit = SubmitField('Add Link')


class RemoveZoomLinkForm(FlaskForm):
    links = SelectField('Entry', choices=[(-1, "---")]+[(link.id, str(link.description + ", " + str(link.day))) for link in ZoomLink.query.all()])
    submit = SubmitField('Remove Link')