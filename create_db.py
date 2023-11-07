from musimate import db, create_app
from musimate.models import User, Event, Comment, Order
from flask_bcrypt import generate_password_hash
from datetime import datetime

# Recreate database
app = create_app()
ctx = app.app_context()
ctx.push()
db.drop_all()
db.create_all()

# Populate the database with sample data
user1_name = 'test'
user1_password = generate_password_hash('1234')
user1_email = 'test@test.com'
user1_contact_number = '1234567890'
user1_address = '1234 Main Street'
user_1 = User(name=user1_name, password_hash=user1_password, email=user1_email, contact_number=user1_contact_number, address=user1_address)
db.session.add(user_1)
db.session.commit()

user2_name = 'person'
user2_password = generate_password_hash('abcd')
user2_email = 'person@email.com'
user2_contact_number = '6789012345'
user2_address = '89 Side Rd'
user_2 = User(name=user2_name, password_hash=user2_password, email=user2_email, contact_number=user2_contact_number, address=user2_address)
db.session.add(user_2)
db.session.commit()

event1_name = 'Omatone Concert'
event1_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event1_genre = 'Pop'
event1_location = 'Brisbane'
event1_string_date = '28/11/2023 5:00 PM'
event1_date = datetime.strptime(event1_string_date, '%d/%m/%Y %I:%M %p')
event1_image = '/static/image/otamatone.jpg'
event1_quantity = 20
event1_price = 15
event1_user_id = user_1.id
event_1 = Event(name=event1_name, description=event1_description, genre=event1_genre, location=event1_location, date=event1_date, image=event1_image, quantity=event1_quantity, price=event1_price, user_id=event1_user_id)
db.session.add(event_1)
db.session.commit()

event2_name = 'Classical Concert'
event2_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event2_genre = 'Classical'
event2_location = 'Gold Coast'
event2_string_date = '24/11/2023 11:00 AM'
event2_date = datetime.strptime(event2_string_date, '%d/%m/%Y %I:%M %p')
event2_image = '/static/image/event2.jpg'
event2_quantity = 5
event2_price = 19.99
event2_user_id = user_1.id
event_2 = Event(name=event2_name, description=event2_description, genre=event2_genre, location=event2_location, date=event2_date, image=event2_image, quantity=event2_quantity, price=event2_price, user_id=event2_user_id)
db.session.add(event_2)
db.session.commit()

event3_name = 'Heavy Metal Concert'
event3_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event3_genre = 'Metal'
event3_location = 'Brisbane'
event3_string_date = '3/11/2023 8:00 PM'
event3_date = datetime.strptime(event3_string_date, '%d/%m/%Y %I:%M %p')
event3_image = '/static/image/event3.jpg'
event3_quantity = 200
event3_price = 10.5
event3_user_id = user_1.id
event_3 = Event(name=event3_name, description=event3_description, genre=event3_genre, location=event3_location, date=event3_date, image=event3_image, quantity=event3_quantity, price=event3_price, user_id=event3_user_id)
db.session.add(event_3)
db.session.commit()

event4_name = 'Rap Concert'
event4_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event4_genre = 'Rap'
event4_location = 'Townsville'
event4_string_date = '1/12/2023 2:00 PM'
event4_date = datetime.strptime(event4_string_date, '%d/%m/%Y %I:%M %p')
event4_image = '/static/image/event6.jpg'
event4_quantity = 100
event4_price = 4.99
event4_user_id = user_2.id
event_4 = Event(name=event4_name, description=event4_description, genre=event4_genre, location=event4_location, date=event4_date, image=event4_image, quantity=event4_quantity, price=event4_price, user_id=event4_user_id)
event_4.status = 'Cancelled'
db.session.add(event_4)
db.session.commit()

comment1_text = 'Looking forward to this event!'
comment1_user_id = user_1.id
comment1_event_id = event_1.id
comment_1 = Comment(text=comment1_text, user_id=comment1_user_id, event_id=comment1_event_id)
db.session.add(comment_1)
db.session.commit()

comment2_text = 'I love listening to classical music. It is so relaxing.'
comment2_user_id = user_1.id
comment2_event_id = event_2.id
comment_2 = Comment(text=comment2_text, user_id=comment2_user_id, event_id=comment2_event_id)
db.session.add(comment_2)
db.session.commit()

comment3_text = 'ARE YOU READY TO ROCK?!?!'
comment3_user_id = user_1.id
comment3_event_id = event_3.id
comment_3 = Comment(text=comment3_text, user_id=comment3_user_id, event_id=comment3_event_id)
db.session.add(comment_3)
db.session.commit()

order1_quantity = 5
order1_user_id = user_1.id
order1_event_id = event_1.id
order_1 = Order(quantity=order1_quantity, user_id=order1_user_id, event_id=order1_event_id)
event_1.quantitySold += order1_quantity
db.session.add(order_1)
db.session.commit()

order2_quantity = 5
order2_user_id = user_1.id
order2_event_id = event_2.id
order_2 = Order(quantity=order2_quantity, user_id=order2_user_id, event_id=order2_event_id)
event_2.quantitySold += order2_quantity
db.session.add(order_2)
db.session.commit()

order3_quantity = 2
order3_user_id = user_2.id
order3_event_id = event_1.id
order_3 = Order(quantity=order3_quantity, user_id=order3_user_id, event_id=order3_event_id)
event_1.quantitySold += order3_quantity
db.session.add(order_3)
db.session.commit()

quit()


