from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    events = db.relationship('Event', backref='user')
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    # realation to call user.orders and order.placed_by
    orders = db.relationship("Order", backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    genre = db.Column(db.String(40))
    location = db.Column(db.String(200))
    # possibly make this a date time format
    date = db.Column(db.DateTime)
    image = db.Column(db.String(400))
    quantity = db.Column(db.Integer)
    quantitySold = db.Column(db.Integer)
    price = db.Column(db.Float)
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
    # relation to call event.orders and order.event
    orders = db.relationship('Order', backref = 'event')

	# string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"
    
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer)
    booked_at = db.Column(db.DateTime, default = datetime.now())
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))

    def __repr__(self):
        return f"Order: {self.order_id}"