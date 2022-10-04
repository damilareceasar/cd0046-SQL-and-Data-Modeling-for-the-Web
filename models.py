from flask_sqlalchemy import SQLAlchemy
from flask import Flask


#instantiation of the flask api and sqalAlchemy api
app = Flask(__name__)
db = SQLAlchemy(app)
#creation of the Venue Models
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


#creation of the Artist model
class Artist(db.Model):
        __tablename__ = 'artist'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        city = db.Column(db.String(120))
        state = db.Column(db.String(120))
        phone = db.Column(db.String(120))
        genres = db.Column(db.String(120))
        seek_venue = db.Column(db.Boolean, nullable=False, default=False)
        image_link = db.Column(db.String(500))
        facebook_link = db.Column(db.String(120))
        website_link = db.Column(db.String(120))
        seek_description= db.Column(db.String(120))
        date = db.Column(db.DateTime, default = db.func.now())
        shows = db.relationship('Shows', backref='artist', lazy=True)

#creation of the shows Model
class Shows(db.Model):
      __Tablename__ = 'shows'
      id = db.Column(db.Integer,primary_key = True)
      artist_id = db.Column(db.Integer)
      time = db.Column(db.String())
      show_id = db.Column(db.Integer,db.ForeignKey('artist.id'))
      venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)