from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, EditEventForm, CommentForm, OrderForm
from . import db
import os
from datetime import datetime
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')


@eventbp.route('/<id>')
def show(id):
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    # create the comment form
    comment_form = CommentForm()
    order_form = OrderForm()

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
    return render_template('events/show.html', event=event, genres=genres, selected_genre='Select', comment_form=comment_form, order_form=order_form)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data, description=form.description.data,
                      genre=form.genre.data, location=form.location.data, date=form.date.data,
                      image=db_file_path, quantity=form.quantity.data, price=form.price.data, user=current_user)
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Successfully created new event', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('main.index'))
    return render_template('events/create.html', form=form, genres=genres, selected_genre='Select', editing=False)


@eventbp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if (event.user != current_user):
        flash('You are not the owner of this event', 'error')
        return redirect(url_for('event.show', id=id))
    else:
        form = EditEventForm()
        if (request.method == 'GET'):
            # Prepare form with default values
            form.name.default = event.name
            form.description.default = event.description
            form.genre.default = event.genre
            form.location.default = event.location
            form.date.default = event.date
            form.quantity.default = event.quantity
            form.price.default = event.price
            form.process()

        if form.validate_on_submit():
            # call the function that checks and returns image
            if (form.image.data is not None):
                db_file_path = check_upload_file(form)
                event.image = db_file_path
            # update the event data
            event.name = form.name.data
            event.description = form.description.data
            event.genre = form.genre.data
            event.location = form.location.data
            event.date = form.date.data
            event.quantity = form.quantity.data
            event.price = form.price.data
            # add the object to the db session
            db.session.add(event)
            # commit to the database
            db.session.commit()
            flash('Successfully edited event', 'success')
            # Always end with redirect when form is valid
            return redirect(url_for('event.show', id=id))
    return render_template('events/create.html', form=form, event=event, genres=genres, selected_genre='Select', editing=True)


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@eventbp.route('/change_status/<id>/<status>')
@login_required
def change_status(id, status):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if (event.user != current_user):
        flash('You are not the owner of this event', 'error')
        return redirect(url_for('event.show', id=id))
    else:
        event.status = status
        db.session.commit()
        flash('Event status changed', 'success')
        return redirect(url_for('event.show', id=id))


@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    # get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data, event=event,
                          user=current_user)
        # here the back-referencing works - comment.event is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()
        # flashing a message which needs to be handled by the html
        flash('Your comment has been added', 'success')
        # print('Your comment has been added', 'success')
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))


@eventbp.route('/<id>/order', methods=['GET', 'POST'])
@login_required
def order(id):
    form = OrderForm()
    # get event object from DB associated with current order
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    # from event object isloate allocatedTix & quatitySold for that event
    allocatedTix = db.session.scalar(
        db.select(Event.quantity).where(Event.id == id))
    quantitySold = db.session.scalar(
        db.select(Event.quantitySold).where(Event.id == id))
    # calculate the number of tickets that can be purchased.
    availableTix = allocatedTix - quantitySold
    # if there are no tix left: can't purchase tickets
    if availableTix <= 0:
        flash("Event is sold out!!", 'error')
        return redirect(url_for('event.show', id=id))

    elif form.validate_on_submit():
        # read data from form
        orderQuant = form.quantity.data
        # if the order quantity more than available purchase will fail
        if orderQuant > availableTix:
            flash("Not enough tickets available", 'error')
            return redirect(url_for('event.show', id=id))
      # if order quantity is less than available tix proceed with placing the order
        elif orderQuant <= availableTix:
            order = Order(quantity=form.quantity.data, event=event,
                          user=current_user)
            #back referencing - order.event is set and link created
            db.session.add(order)
            # add the order to the DB
            event.quantitySold += orderQuant
            # update the quantitySold on the event 
            db.session.commit()
            #display message:
            flash('Your order has been placed.\n' +
                  f'Order Number: {order.order_id}E{event.id}Q{orderQuant}#{datetime.now().toordinal()}', 'success')
            
            return redirect(url_for('event.show', id=id))

    else:
        return redirect(url_for('event.show', id=id))
