from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Order
from . import db
from flask_login import login_required, current_user
from datetime import datetime

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():

    events = db.session.scalars(db.select(Event)).all()
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    num_events = len(events)
    for event in events: 
        currentStatus = None
        # if event.status = "Cancelled":
        #   currentStatus = "Cancelled"
        if event.date < datetime.now():
            event.currentStatus = "Inactive"
        elif event.quantity <= event.quantitySold:
            event.currentStatus = "Sold-Out"
        else:
            event.currentStatus = "Open"
    return render_template('index.html', events=events, num_events=num_events, genres=genres, selected_genre='Select', selected_location='', selected_date='')

# def eventStatus(id):
#     currentStatus = None
#     event = db.session.scalar(db.select(Event)).where
#     # if event.status = "Cancelled":
#     #   currentStatus = "Cancelled"
#     if event.date < datetime.datetime.now():
#       return "Inactive"
#     elif event.quantity <= event.quantitySold:
#       return "Sold-Out"
#     else:
#       return "Open"

@mainbp.route('/tickets')
@login_required
def tickets():
    # tickets = db.session.scalars(db.select(Order)).all()
    tickets = db.session.scalars(
                db.select(Order).where(Order.user == current_user)).all()
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    return render_template('tickets.html', tickets=tickets, num_tickets=len(tickets), genres=genres, selected_genre='Select')


@mainbp.route('/search')
def search():
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
        genres = db.session.scalars(
            db.select(Event.genre.distinct()).where(Event.genre.is_not(request.args["genre"])))
        if request.args['genre'] == "All" or request.args['genre'] == "Select":
            events = db.session.scalars(
                db.select(Event).where(Event.location.like(location)).where(Event.date.like(date))).all()
        else:
            events = db.session.scalars(
                db.select(Event).where(Event.genre.is_(genre)).where(Event.location.ilike(location)).where(Event.date.ilike(date))).all()
        return render_template('index.html', events=events, num_events=len(events), genres=genres, selected_genre=request.args['genre'], selected_location=request.args['location'], selected_date=request.args['date'])