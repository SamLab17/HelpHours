from helphours import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class Instructor(UserMixin, db.Model):
    """
        Database model to represent an Instructor
        in the "instructors" table. This class is
        also used as the "User" class for flask_login
        authentication
    """
    __tablename__ = "instructors"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    is_active = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)
    last_login = db.Column(db.DateTime)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """ Allows the login manager to load the
        correct user from the database based
        on their ID
    """
    return Instructor.query.get(int(id))


# I don't like the idea of being able to completely delete an Instructor
# from the table because the visits store an instructor id and removing
# an entry could cause problems.
# We could fake deleting an instructor by having a "is_visible" column
# which would hide the instructor from the admin panel, prevent them from logging in
# but preserve the links with any entries they may have attributed to them in the
# visits table.
