#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db,app,Venue,Artist,Shows
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:funmilayo@localhost:5432/fyurr'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
migrate = Migrate(app,db)



#creation of venue Model

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


#creation of Artist Model

    # TODO: implement any micssing fields, as a database migration using Flask-Migrate
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#Creation of shows Model

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
#Query request for Venues
@app.route('/')
def index():
  myvenue = Venue.query.order_by(Venue.date.desc()).limit(3).all()
  art = Artist.query.order_by(Artist.date.desc()).limit(3).all()

  venue = []
  for venues in myvenue:
    venue.append({
      "id": venues.id,
      "name": venues.name,
      "city": venues.city
    })
  artist = []
  for art in artist:
    artist.append({
      'id': art.id,
      'name': art.name,
      'city': art.city
    })
  
  return render_template('pages/home.html', venues=venue, artists=artist)
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
   
  venue_list = Venue.query.distinct(Venue.city, Venue.state).all()
  data = []
  for location in venue_list:
    result ={
      'state': location.state,
      'city': location.city
    }
    venue_name = Venue.query.filter_by(city=location.city, state=location.state).all()
    all_venue = []
    for venue in venue_name:
      all_venue.append({       
        'id': venue.id,
       'name':venue.name,       
      })

      result['venues'] = all_venue
      data.append(result)
     
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  query = request.form.get("search_term")
  #search = Artist.query.filter(Artist.name == text).all()
  search = Venue.query.filter(Venue.name.ilike(f'%{query}%')).all()
  result = {
    'count':len(search),
    'data': []
  }

  for mysearch in search:
    result['data'].append({
      'id':mysearch.id,
      'name':mysearch.name
    })
    db.session.close()
  return render_template('pages/search_venues.html', results=result, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
     myvenue = Venue.query.get('id')

     upcoming = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue_id).filter(Shows.time >= db.func.now())
     previous = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue_id).filter(Shows.time < db.func.now())
  
     
     list_upcoming = []
     list_previous = []

     for myshow in upcoming:
      list_upcoming.append({
        'start_time' : str(myshow.time.strftime('%Y-%m-%d %H:%M:%S')),
        'artist_id': myshow.artist.id,
        'artist_image_link': myshow.artist.image_link,
        'artist_name': myshow.artist.name,
      })
     
      for myshow in previous:
         list_previous.append({
        'start_time' : str(myshow.time.strftime('%Y-%m-%d %H:%M:%S')),
        'artist_image_link': myshow.artist.image_link,
        'artist_name': myshow.artist.name,
        'artist_id': myshow.artist.id

      })


      data = {

        'up_show':list_upcoming,
        'prev_show':list_previous,
        'up_count':len(list_upcoming),
        'prev_count':len(list_previous),
        
      }

     return render_template('pages/show_venue.html',venue=myvenue,data=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  try:
      form = VenueForm(request.form)
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      genres = form.genres.data
      img_link = form.phone.data
      fb_link = form.facebook_link.data
      wb_link = form.website_link.data
      sk_talent = form.seeking_talent.data
      description = form.seeking_description.data
 
      my_venue = Venue(name=name,city=city,state=state,address=address,
      phone=phone,genres=genres,image_link=img_link,facebook_link=fb_link,
      website_link=wb_link,talent_hunt=sk_talent,description=description)
      db.session.add(my_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
      db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')
  
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  art = db.session.query(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=art)
    
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artname = request.form.get("search_term")
  
  art_search = Artist.query.filter(Artist.name.ilike(f'%{artname}%')).all()
  
  result = {
    'data': [],
    'count':len(art_search)
    }

  for searching in art_search:
    result['data'].append({
      'id':searching.id,
      'name':searching.name
    })

  db.session.close()
  return render_template('pages/search_artists.html', results = result , search_term=request.form.get('search_term', ''))
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
#edit Artist form
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = ArtistForm(request.form)
  get_artist = Artist.query.get(artist_id)
  form.name.default = get_artist.name
  form.state.default =get_artist.state
  form.city.default = get_artist.city
  form.phone.default = get_artist.phone
  form.website_link.default = get_artist.website_link
  form.facebook_link.default = get_artist.facebook_link
  form.seeking_venue.default = get_artist.seek_venue
  form.seeking_description.default = get_artist.seek_description
  form.genres.default = get_artist.genres
  form.process()
  


  return render_template('forms/edit_artist.html', form=form, artist=get_artist)

  

def Request(req):
  if req == 'genres':
    return request.form.getlist(req)
  elif req == 'seeking_talent' or req == 'seek_venue' and request.form[req] == 'y':
    return True
  elif req == 'seeking_talent' or req == 'seek_venue' and request.form[req] != 'y':
    return False
  else:
    return request.form[req]
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  get_artist = Artist.query.get(artist_id)
  try:  
    get_artist.name = Request('name')
    get_artist.genres = Request('genres')
    get_artist.city = Request('city')
    get_artist.phone = Request('phone')
    get_artist.state = Request('state')
    get_artist.website_link = Request('website_link')
    get_artist.seeking_talent = Request('seeking_talent')
    get_artist.seek_description = Request('seeking_description')
    get_artist.facebook_link = Request('facebook_link')
    get_artist.image_link = Request('image_link')
    db.session.commit()
    flash( request.form['name'] + 'details has been succesfully updated!')
  except:
    flash('Error')
    db.session.rollback()

  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
   
  get_venue = Venue.query.get(venue_id)
  form.genres.default = get_venue.genres
  form.address.default = get_venue.address
  form.name.default = get_venue.name
  form.state.default = get_venue.state
  form.city.default = get_venue.city
  form.phone.default = get_venue.phone
  form.website_link.default = get_venue.website_link
  form.facebook_link.default = get_venue.facebook_link
  form.seeking_talent.default = get_venue.talent_hunt
  form.seeking_description.default = get_venue.description
  
  form.process()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=get_venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue_edit = Venue.query.get(venue_id)
  try:  
    venue_edit.name = Request('name')
    venue_edit.genres = Request('genres')
    venue_edit.city = Request('city')
    venue_edit.phone = Request('phone')
    venue_edit.state = Request('state')
    venue_edit.website_link = Request('website_link')
    venue_edit.talent_hunt = Request('seeking_talent')
    venue_edit.description = Request('seeking_description')
    venue_edit.facebook_link = Request('facebook_link')
    venue_edit.image_link = Request('image_link')
    venue_edit.address = Request('address')
    db.session.commit()
    flash(  request.form['name'] + 'details has been  updated!')
  except:
    flash(' try  again')
  
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)
#Artist submission to the database
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   
      form = ArtistForm(request.form)
    #this block validates users input form
  
      if form.validate():
         try:
             name = form.name.data
             city = form.city.data
             state = form.state.data
             phone = form.phone.data
             genres = form.genres.data
             fb_link = form.facebook_link.data
             website_link = form.website_link.data
             image_link = form.image_link.data
             seeking_venue = form.seeking_venue.data
             seeking_description = form.seeking_description.data
    
             new_artist = Artist(name = name, city=city, state=state, phone=phone, genres=genres, facebook_link= fb_link, website_link=website_link, image_link =image_link, seek_description= seeking_description, seek_venue=seeking_venue)
             db.session.add(new_artist)
             db.session.commit()
    
             flash('Artist ' + request.form['name'] + ' was successfully listed!')
         except:
              db.session.rollback()
              flash('Artist ' + request.form['name'] + ' was not listed')

         finally:     
            db.session.close()
            return render_template('pages/home.html')
    
      else: 
          flash('Form input invalid')
          for field, message in form.errors.items():
             flash(field + ' - ' + str(message))
             flash(str(message))
             return render_template('pages/home.html')
  


#  Shows
#  ----------------------------------------------------------------
#show query
@app.route('/shows')
def shows():
   
  # displays list of shows at /shows
  show = db.session.query(Shows).join(Artist).all()
  data = []
  for myshow in show:
    data.append({
      'venue_id': myshow.venue.id,
      'venue_name': myshow.venue.name,
      'artist_name': myshow.artist.name,
      'artist_id': myshow.artist_id,
      'artist_image_link': myshow.artist.image_link,
      'start_time': str(myshow.time.strftime('%Y -%m-%d %H:%M:S'))
    }) 
  return render_template('pages/shows.html', shows=data)
#show submission to the database
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    try:
       form = ShowForm(request.form)
       art_id = form.artist_id.data
       ven_id = form.venue_id.data
       time = form.start_time.data
       my_show = Shows(artist_id=art_id, venue_id=ven_id, time =time)
       db.session.add(my_show)
       db.session.commit()
       flash('Show added succesfully!')
    except:
       db.session.rollback()
       flash('Show Error')
       db.session.close()
    return render_template('pages/home.html')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
 # displays list of shows at /shows
  # TODO: replace with real venues data.
  # # 
'''
  
   show = db.session.query(Shows).join(Artist).all()
   data= []

   for myshow in show:
    data.append({
      'artist_id': myshow.artist_id,
      'artist_name': myshow.artist.name,
      'venue_id': myshow.venue.id,
      'venue_name': myshow.venue.name,
      'image_link': myshow.artist.image_link,
      'start_time': str(myshow.time.strftime('%Y -%m-%d %H:%M:S'))
    }) 

    return render_template('pages/shows.html', shows=data)
'''