from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length, DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#Create new event
class EventForm(FlaskForm):
  name = StringField('Country', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  currency = StringField('Currency', validators=[InputRequired()])
  submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired(message='Enter user name'), Length(min=3, max=64, message="Username must be between 3 and 64 characters")])
    password = PasswordField("Password", validators=[DataRequired(message='Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired(), Length(min=4, max=32, message="Username must be between 4 and 32 characters")])
    email_id = StringField("Email Address", validators=[DataRequired(), Email("Please enter a valid email"),Length(max=32, message="Email must be under 32 characters")])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long"), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    #submit button
    submit = SubmitField("Register")


#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')