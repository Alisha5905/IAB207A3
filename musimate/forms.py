from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DecimalField, DateTimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length, DataRequired, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new event
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    genre = StringField('Genre', validators=[InputRequired()])
    date = DateTimeField("Date", validators=[InputRequired(
    )], format='%d/%m/%Y %I:%M %p', description="Use format: dd/mm/yyyy hh:mm am/pm")
    image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(
        ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    quantity = IntegerField('Quantity of Tickets Available', validators=[InputRequired(
    ), NumberRange(min=10, max=99999999999, message="please enter a quantity greater than 10")])
    price = DecimalField('Ticket Price ($)', validators=[
                         InputRequired()], render_kw={"placeholder": "00.00"})
    submit = SubmitField("Create")

# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired(message='Enter user name'), Length(
        min=3, max=64, message="Username must be between 3 and 64 characters")])
    password = PasswordField("Password", validators=[
                             DataRequired(message='Enter user password')])
    submit = SubmitField("Login")

# User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired(), Length(
        min=4, max=32, message="Username must be between 4 and 32 characters")])
    email_id = StringField("Email Address", validators=[DataRequired(), Email(
        "Please enter a valid email"), Length(max=32, message="Email must be under 32 characters")])
    contact_number = StringField("Contact Number", validators=[DataRequired(), Length(
        min=7, max=15, message="Contact number must be between 7 and 15 digits")])
    address = TextAreaField("Address", validators=[DataRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[DataRequired(), Length(
        min=4, message="Password must be at least 6 characters long"), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    # submit button
    submit = SubmitField("Register")


# User comment
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Post Comment')


# User order
class OrderForm(FlaskForm):
    quantity = IntegerField("Order", [InputRequired(), NumberRange(
        min=1, max=10, message="please entre a quantity between 1 and 10")])
    submit = SubmitField("Place Order")
