from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class JoinQueueForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
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
