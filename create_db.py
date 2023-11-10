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
user1_name = 'Rick Astley'
user1_password = generate_password_hash('1234')
user1_email = 'rick@astely.com'
user1_contact_number = '424141'
user1_address = 'Rick Roll Street'
user_1 = User(name=user1_name, password_hash=user1_password, email=user1_email, contact_number=user1_contact_number, address=user1_address)
db.session.add(user_1)
db.session.commit()

user2_name = 'Bladee'
user2_password = generate_password_hash('abcd')
user2_email = 'Bladee@email.com'
user2_contact_number = '6789012345'
user2_address = '89 Side Rd'
user_2 = User(name=user2_name, password_hash=user2_password, email=user2_email, contact_number=user2_contact_number, address=user2_address)
db.session.add(user_2)
db.session.commit()

user3_name = 'Jesus Piece Band'
user3_password = generate_password_hash('78910')
user3_email = 'jp@band.com'
user3_contact_number = '457949763'
user3_address = '59 Wrong Road'
user_3 = User(name=user3_name, password_hash=user3_password, email=user3_email, contact_number=user3_contact_number, address=user3_address)
db.session.add(user_3)
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
event2_description = 'Fun classical vibes for you to come and enjoy.'
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

event5_name = 'Jesus Piece'
event5_description = "Philadelphia’s Jesus Piece gallantly broke onto the scene, turning heads for their feral live shows and grandiose, melodic songwriting which has since cemented them as standard stirrers and boundary-breakers. On their latest album ‘...So Unknown’, listeners ascend to the apex of metal and hardcore– where a mix of complex instrumentation is led by a manic, shaman-like vocal delivery from frontman Aaron Heard. It’s a cluster bomb of ten anthems, bursting at the seams with memorable riffs and pulsing with fresh ideas. Drummer Luis Aponte (LU2K) promises, “This is as close to a Jesus Piece experience as you’re going to get without standing in front of us.” Joined by guitarists David Updike and John Distefano, Jesus Piece has created an effort that never fails to impress, gets to the point and never gets in its own way. Heard uses a livewire vocal delivery, ala Busta Rhymes, to orchestrate the crowd’s kinetic energy— pushing further toward utter mayhem and culminating in a show that stands tall among their genre peers and live music writ large."
event5_genre = 'HardCore'
event5_location = 'Sydney'
event5_string_date = '5/12/2023 8:00 PM'
event5_date = datetime.strptime(event5_string_date, '%d/%m/%Y %I:%M %p')
event5_image = '/static/image/jp.png'
event5_quantity = 150
event5_price = 35.30
event5_user_id = user_3.id
event_5= Event(name=event5_name, description=event5_description, genre=event5_genre, location=event5_location, date=event5_date, image=event5_image, quantity=event5_quantity, price=event5_price, user_id=event5_user_id)
db.session.add(event_5)
db.session.commit()

event6_name = 'Bladee Tour'
event6_description = "The Iconic internation underground rap icon Bladee starts his tour off with a bang in Melbourne. With special appearences from 'Drain Gang' the rap group dominating the underground rap scene. Starting out in early 2000s from Stockholm, this collective along with Bladee revolutionalised the rap game with the unique sound."
event6_genre = 'Rap'
event6_location = 'Melbourne'
event6_string_date = '7/12/2023 10:00 PM'
event6_date = datetime.strptime(event5_string_date, '%d/%m/%Y %I:%M %p')
event6_image = '/static/image/bladee.jpg'
event6_quantity = 125
event6_price = 54.20
event6_user_id = user_2.id
event_6= Event(name=event6_name, description=event6_description , genre=event6_genre, location=event6_location, date=event6_date, image=event6_image, quantity=event6_quantity, price=event6_price, user_id=event6_user_id)
db.session.add(event_6)
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