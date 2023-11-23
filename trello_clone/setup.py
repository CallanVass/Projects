from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ


#  ACL = Access Control List
# Create instance of the app
app = Flask(__name__)

# Connection string
# This could be generated at random every now and then (coded, obviously)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"
] = environ.get("CONNECTION_STRING")

# Import (must be after config but before routes/error handlers)
# Pass instances of flask app to the modules
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)