from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Order
from . import db
from flask_login import login_required, current_user
from datetime import datetime

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    events = db.session.scalars(
        db.select(Event).order_by(Event.id.desc()).limit(24)).all()
    upcoming_events = db.session.scalars(
        db.select(Event).order_by(Event.date.desc()).limit(4)).all()
    popular_events = db.session.scalars(
        db.select(Event).order_by(Event.quantitySold.desc()).limit(4)).all()
    for event in events:
        if event.status != 'Inactive' and event.date < datetime.now():
            event.status = "Inactive"
            db.session.commit()
        elif event.status == 'Inactive' and event.date > datetime.now():
            if event.quantity > event.quantitySold:
                event.status = "Open"
                db.session.commit()
            else:
                event.status = "Sold Out"
                db.session.commit()
        elif event.status != 'Sold Out' and event.status != 'Cancelled' and event.quantity <= event.quantitySold:
            event.status = "Sold Out"
            db.session.commit()
        elif event.status == 'Sold Out' and event.quantity > event.quantitySold:
            event.status = "Open"
            db.session.commit()
    return render_template('index.html', events=events, num_events=len(events), upcoming_events=upcoming_events, popular_events=popular_events,
                           genres=genres, selected_genre='Select', selected_location='', selected_date='',
                           searching=False)


@mainbp.route('/tickets')
@login_required
def tickets():
    tickets = db.session.scalars(
        db.select(Order).where(Order.user == current_user)).all()
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    return render_template('tickets.html', tickets=tickets, num_tickets=len(tickets), genres=genres, selected_genre='Select')


@mainbp.route('/search')
def search():
    genres = db.session.scalars(
        db.select(Event.genre.distinct()).where(Event.genre.is_not(request.args["genre"])))
    events = db.session.scalars(
        db.select(Event).order_by(Event.id.desc()).limit(24)).all()
    upcoming_events = db.session.scalars(
        db.select(Event).order_by(Event.date.desc()).limit(4)).all()
    popular_events = db.session.scalars(
        db.select(Event).order_by(Event.quantitySold.desc()).limit(4)).all()
    try:
        date_time = datetime.strptime(request.args['date'], '%d/%m/%y')
        date = "%" + date_time.strftime("%Y-%m-%d") + "%"
        print(date)
    except:
        date = "%" + request.args['date'] + "%"

    genre = request.args['genre']
    location = "%" + request.args['location'] + "%"

    if request.args['genre'] == "Select" and location == "%%" and date == "%%":
        return redirect(url_for('main.index'))
    else:
        if request.args['genre'] == "All" or request.args['genre'] == "Select":
            search_events = db.session.scalars(
                db.select(Event).where(Event.location.like(location)).where(Event.date.like(date)).limit(12)).all()
        else:
            search_events = db.session.scalars(
                db.select(Event).where(Event.genre.is_(genre)).where(Event.location.ilike(location)).where(Event.date.ilike(date)).limit(12)).all()
        return render_template('index.html', events=events, num_events=len(events), search_events=search_events, num_search_events=len(search_events),
                               upcoming_events=upcoming_events, popular_events=popular_events,
                               genres=genres, selected_genre=request.args['genre'], selected_location=request.args['location'], selected_date=request.args['date'],
                               searching=True)
