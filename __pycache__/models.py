from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)
db = SQLAlchemy(app)
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    talent_hunt = db.Column(db.Boolean())
    description = db.Column(db.String(120))
    shows = db.relationship("Shows",backref = 'venue',lazy=True)
    date = db.Column(db.DateTime, default = db.func.now())


