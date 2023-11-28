from flask import abort
from flask_jwt_extended import  get_jwt_identity
from models.user import User
from setup import app
# Importing the blueprints
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.cards_bp import cards_bp

# ENSURE YOU UNTRACK .FLASKENV

# Registering the blueprints (which allow us to modularise clicommands and routes)
app.register_blueprint(db_commands)

app.register_blueprint(users_bp)

app.register_blueprint(cards_bp)


