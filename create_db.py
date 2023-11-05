from musimate import db, create_app
from musimate.models import User, Event, Comment
from flask_bcrypt import generate_password_hash

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

event1_name = 'Omatone Concert'
event1_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event1_genre = 'Pop'
event1_location = 'Brisbane'
event1_date = '19/09/2023 5:00pm'
event1_image = '/static/image/otamatone.jpg'
event1_price = 15
event1_user_id = user_1.id
event_1 = Event(name=event1_name, description=event1_description, genre=event1_genre, location=event1_location, date=event1_date, image=event1_image, price=event1_price, user_id=event1_user_id)
db.session.add(event_1)
db.session.commit()

event2_name = 'Classical Concert'
event2_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event2_genre = 'Classical'
event2_location = 'Gold Coast'
event2_date = '20/09/2023 5:00pm'
event2_image = '/static/image/event2.jpg'
event2_price = 19.99
event2_user_id = user_1.id
event_2 = Event(name=event2_name, description=event2_description, genre=event2_genre, location=event2_location, date=event2_date, image=event2_image, price=event2_price, user_id=event2_user_id)
db.session.add(event_2)
db.session.commit()

event3_name = 'Heavy Metal Concert'
event3_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
event3_genre = 'Metal'
event3_location = 'Brisbane'
event3_date = '20/9/2023 5:00pm'
event3_image = '/static/image/event3.jpg'
event3_price = 10.5
event3_user_id = user_1.id
event_3 = Event(name=event3_name, description=event3_description, genre=event3_genre, location=event3_location, date=event3_date, image=event3_image, price=event3_price, user_id=event3_user_id)
db.session.add(event_3)
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

quit()


