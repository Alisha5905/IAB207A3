from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    #we use this utility module to display forms quickly
    Bootstrap5(app)

    #this is a much safer way to store passwords
    Bcrypt(app)

    #a secret key for the session object
    # created using: python3 -c 'import secrets; print(secrets.token_hex())'
    app.secret_key = 'bfa5fe7e3d0d18ed9d3285679bfb8c167a1cdc8427ea7760d7a84e583501244c'

    #Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musimate.sqlite'
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    #initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.eventbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)
    
    @app.errorhandler(500)
    def internal_server_error(e):
    # note that we set the 500 status explicitly
      return render_template('500.html', error=e)

    #this creates a dictionary of variables that are available
    #to all html templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    return app
