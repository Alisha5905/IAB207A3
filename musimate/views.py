from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    return render_template('index.html', events=events, genres=genres, selected_genre='Select', selected_location='', selected_date='')


@mainbp.route('/search')
def search():
    genre = request.args['genre']
    location = "%" + request.args['location'] + "%"
    date = "%" + request.args['date'] + "%"

    if request.args['genre'] == "Select" and location == "%%" and date == "%%":
        print("None")
        return redirect(url_for('main.index'))
    else:
        print(genre, location, date)
        genres = db.session.scalars(
            db.select(Event.genre.distinct()).where(Event.genre.is_not(request.args["genre"])))
        if request.args['genre'] == "All" or request.args['genre'] == "Select":
            selected_genre = "Select"
            events = db.session.scalars(
                db.select(Event).where(Event.location.like(location)).where(Event.date.like(date)))
        else:
            selected_genre = request.args['genre']
            events = db.session.scalars(
                db.select(Event).where(Event.genre.is_(genre)).where(Event.location.ilike(location)).where(Event.date.ilike(date)))
        return render_template('index.html', events=events, genres=genres, selected_genre=selected_genre, selected_location=request.args['location'], selected_date=request.args['date'])
