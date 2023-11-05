from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    num_events = len(events)
    return render_template('index.html', events=events, num_events=num_events, genres=genres, selected_genre='Select', selected_location='', selected_date='')


@mainbp.route('/search')
def search():
    genre = request.args['genre']
    location = "%" + request.args['location'] + "%"
    date = "%" + request.args['date'] + "%"

    if request.args['genre'] == "Select" and location == "%%" and date == "%%":
        return redirect(url_for('main.index'))
    else:
        genres = db.session.scalars(
            db.select(Event.genre.distinct()).where(Event.genre.is_not(request.args["genre"])))
        if request.args['genre'] == "All" or request.args['genre'] == "Select":
            events = db.session.scalars(
                db.select(Event).where(Event.location.like(location)).where(Event.date.like(date))).all()
        else:
            events = db.session.scalars(
                db.select(Event).where(Event.genre.is_(genre)).where(Event.location.ilike(location)).where(Event.date.ilike(date))).all()
        num_events = len(events)
        return render_template('index.html', events=events, num_events=num_events, genres=genres, selected_genre=request.args['genre'], selected_location=request.args['location'], selected_date=request.args['date'])
