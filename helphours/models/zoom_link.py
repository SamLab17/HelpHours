from helphours import db


class ZoomLink(db.Model):
    __tablename__ = "zoomlinks"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128))
    description = db.Column(db.String(512))
    day = db.Column(db.Integer)
