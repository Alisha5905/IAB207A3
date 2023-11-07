from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm
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
        return redirect(url_for('event.create'))
    return render_template('events/create.html', form=form, genres=genres, selected_genre='Select')


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
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    allocatedTix = db.session.scalar(
        db.select(Event.quantity).where(Event.id == id))
    quantitySold = db.session.scalar(
        db.select(Event.quantitySold).where(Event.id == id))
    availableTix = allocatedTix - quantitySold
    if availableTix <= 0:
        flash("Event is sold out!!", 'error')
        return redirect(url_for('event.show', id=id))

    elif form.validate_on_submit():
        orderQuant = form.quantity.data

        if orderQuant > availableTix:
            flash("Not enough tickets available", 'error')
            return redirect(url_for('event.show', id=id))

        elif orderQuant <= availableTix:
            order = Order(quantity=form.quantity.data, event=event,
                          user=current_user)
            db.session.add(order)
            event.quantitySold += orderQuant
            db.session.commit()
            flash('Your order has been placed.\n' +
                  f'Order Number: {order.order_id}E{event.id}Q{orderQuant}#{datetime.now().toordinal()}', 'success')
            return redirect(url_for('event.show', id=id))

    else:
        return redirect(url_for('event.show', id=id))
