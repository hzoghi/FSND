#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
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
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
#Done
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  error = False
  data = []
  try:
    venue_records = db.session.query(Venue).all()
    locations = [(record.city, record.state) for record in venue_records]
    unique_locations = set(locations)  
    for location in unique_locations:
      location_data = {}
      location_data["city"] = location[0]
      location_data["state"] = location[1]
      location_data["venues"]=[]
      data.append(location_data)
    
    for record in venue_records:
      for dictionary in data:
        if dictionary["city"] == record.city and dictionary["state"] == record.state:
          upcoming_shows = Show.query.filter_by(venue_id = record.id).filter(Show.start_time > datetime.now()).count()
          dictionary["venues"].append({"id": record.id, "name": record.name, 
          "num_upcoming_shows": upcoming_shows}) 
  
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return render_template('pages/venues.html', areas=data)

#Done
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%"+search+"%")).all()
  data = []
  for venue in venues:
    upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(
        Show.start_time > datetime.now()).count()
    data.append({"id": venue.id, "name": venue.name,
                 "num_upcoming_shows": upcoming_shows})

  response = {"count": len(data), "data": data}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time < datetime.now()
  ).all()

  past_shows_list = [{
    'artist_id': artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.image_link,
    "start_time": show.start_time.strftime('%m/%d/%Y')
  } for artist, show in past_shows]

  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
      Show.venue_id == venue_id,
      Show.artist_id == Artist.id,
      Show.start_time > datetime.now()
  ).all()

  upcoming_shows_list = [{
      'artist_id': artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime('%m/%d/%Y')
  } for artist, show in upcoming_shows]
  
  
  
  venue_record = Venue.query.get(venue_id)
  data = {
    "id": venue_id,
    "name": venue_record.name,
    "genres": venue_record.genres,
    "address": venue_record.address,
    "city": venue_record.city,
    "state": venue_record.state,
    "phone": venue_record.phone,
    "website": venue_record.website,
    "facebook_link":venue_record.facebook_link,
    "seeking_talent": venue_record.seeking_talent,
    "seeking_description": venue_record.seeking_description,
    "image_link": venue_record.image_link,
    "past_shows": past_shows_list,
    "upcoming_shows": upcoming_shows_list,
    "past_shows_count": len(past_shows_list),
    "upcoming_shows_count": len(upcoming_shows_list)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#Done
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  data = VenueForm(request.form)
  try:
    if 'seeking_talent' not in request.form:
      seeking = False
      description = ''
    else:
      seeking = True
      description = data.seeking_description
    
    new_venue = Venue(
      name = data.name.data,
      city = data.city.data,
      state = data.state.data,
      address = data.address.data,
      image_link = data.image_link.data,
      genres = data.genres.data,
      facebook_link = data.facebook_link.data,
      website = data.website.data,
      phone = data.phone.data,
      seeking_talent = seeking,
      seeking_description = description
    )
    db.session.add(new_venue)
    db.session.commit()
    
  except:
    error = True 
    db.session.rollback()
    print(sys.exc_info())

  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + data.name.data + ' could not be listed.')
  else:
    flash('Venue ' + data.name.data + ' was successfully listed!')

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

#Done
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.get(venue_id).delete()
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()
    flash('Something went wrong when trying to delete the venue')
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
#Done
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists_query = db.session.query(Artist.id, Artist.name).all()
  data = [q._asdict() for q in artists_query]
  return render_template('pages/artists.html', artists=data)

#Done
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  term = request.form.get('search_term', '')
  search = '%{}%'.format(term)
  artists = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike(search)).all()
  _data = [artist._asdict() for artist in artists]
  data = []
  for _d in _data:
    _d["num_upcoming_shows"] = db.session.query(Show).join(Artist).filter(Artist.id == _d['id'],Show.artist_id == Artist.id,
    Show.start_time > datetime.now()).count()
    data.append(_d)
  response ={"count": len(data), "data": data}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
#Done
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  past_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id, 
    Show.start_time < datetime.now()
  ).all()

  past_shows_list = [{
    'venue_id': artist_id,
    'venue_name': venue.name,
    'venue_image_link': venue.image_link,
    'start_time': show.start_time.strftime('%m/%d/%Y')
  } for venue, show in past_shows]
  
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id,
    Show.start_time > datetime.now()
  ).all()
  
  upcoming_shows_list = [{
    'venue_id': artist_id,
    'venue_name': venue.name,
    'venue_image_link': venue.image_link,
    'start_time': show.start_time.strftime('%m/%d/%Y')
  } for venue, show in upcoming_shows]

  artist_record = Artist.query.get(artist_id)
  data = {
    "id": artist_record.id,
    "name": artist_record.name,
    "genres": artist_record.genres,
    "city": artist_record.city,
    "state": artist_record.state,
    "phone": artist_record.phone,
    "website": artist_record.website,
    "facebook_link": artist_record.facebook_link,
    "seeking_venue": artist_record.seeking_venue,
    "seeking_description": artist_record.seeking_description,
    "image_link": artist_record.image_link,
    "past_shows" : past_shows_list,
    "upcoming_shows" : upcoming_shows_list,
    "past_shows_count" : len(past_shows_list),
    "upcoming_shows_count" : len(past_shows_list)
  } 

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
#Done
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  form = ArtistForm(obj = artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#Done
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  form = ArtistForm(request.form)
  error = False

  try:
    artist = Artist.query.first_or_404(artist_id)
    form.populate_obj(artist)    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash("Something went wrong while trying to edit the record")  
  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  form = VenueForm(obj=venue)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#Done
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  

  try:
    venue = Venue.query.first_or_404(venue_id)
    form.populate_obj(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash("Something went wrong while trying to edit the record")
  finally:
    db.session.close()
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

#Done
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)
  error = False
  
  try:
    new_artist = Artist()
    form.populate_obj(new_artist)
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    print(sys.exc_info())
    flash('An error occured. Artist ' + request.form['name'] + ' was not created!')
    db.session.rollback()
  
  finally:
    db.session.close()

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

#Done
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  shows = db.session.query(Show).all()
  data = [{
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name":show.artist.name,
    "artist_image_link":show.artist.image_link,
    "start_time": show.start_time.strftime("%Y%m%d")
  }for show in shows]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False

  try:
    new_show = Show()
    form.populate_obj(new_show)
    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
