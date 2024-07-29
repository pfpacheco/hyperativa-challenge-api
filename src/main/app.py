import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from routes.credit_card.credit_card_route import route as credit_card_route
from routes.authentication.user.user_route import route as user_route


load_dotenv()
app = Flask(__name__)
app.register_blueprint(user_route)

app.register_blueprint(credit_card_route)

app.config['DEBUG'] = os.getenv('DEBUG')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['ALLOWED_EXTENSIONS'] = os.getenv('ALLOWED_EXTENSIONS')

jwt = JWTManager(app)
