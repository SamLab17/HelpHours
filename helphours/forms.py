from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError, NoneOf
from helphours.models.zoom_link import ZoomLink
from helphours.student import Student
from helphours import app
import validators


class JoinQueueForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=32, message="Please limit name entry to 2-32 characters.")
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

    default_opt = ('', 'Choose Format')
    remote_opt = (Student.REMOTE, 'Remote')
    in_person_opt = (Student.IN_PERSON, 'In Person')

    # If dual modality is not enabled, use 'remote'
    modality_default = None if app.config['DUAL_MODALITY'] else Student.REMOTE
    modality = SelectField('Format', choices=[default_opt, remote_opt, in_person_opt], 
                           default=modality_default, validators=[
        DataRequired(),
        NoneOf(default_opt)
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
        (-1, '---'),
        (0, 'Other'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    ])
    submit = SubmitField('Add Link')


class RemoveZoomLinkForm(FlaskForm):
    links = SelectField('Entry', validate_choice=False)
    submit = SubmitField('Remove Link')

    def set_choices(self):
        days = ["Other", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.links.choices = [(-1, "---")] + [(link.id, str(link.description + ", " + days[int(link.day)]))
                                              for link in ZoomLink.query.order_by(ZoomLink.day).all()]
