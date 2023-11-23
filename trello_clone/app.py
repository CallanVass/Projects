from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from setup import *
from models.card import Card, CardSchema
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from sqlalchemy.exc import IntegrityError


# ENSURE YOU UNTRACK .FLASKENV

def admin_required():
    # Checking for user in header (decoded with jwt-get-identity) (Get email address)
    user_email = get_jwt_identity()
    # Check user email against the databasse
    stmt = db.select(User).where(User.email == user_email)
    # Get an instance of the model (stmt user model)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

# Handling the 401 error (This will pick up every 401 error)
@app.errorhandler(401)
def unauthorised(err):
    return {"error": "You are not authorised to access this resource"}

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)


# @app.cli.command("all_cards")
# def all_cards():
#     # Select different orders from cards;
#     stmt = db.select(Card).where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
#     # Select * from cards;
#     stmt = db.select(Card)
#     cards = db.session.scalars(stmt).all()
#     # print(list(cards)) FOR DEBUGGING
#     for card in cards:
#         print(card.__dict__)
#     # Could also use __repr__ for a string representation of an object

@app.route("/cards")
@jwt_required()
def all_cards():
    admin_required()
    # Select * from cards;
    stmt = db.select(Card)#.where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
    # dump() will convert a Python object into a JSON object, 
    # dumps() encodes a Python object into JSON string, 
    # which makes it more readily readable to more frameworks/languages.


# Declaring a route
@app.route("/")
def index():
    return "Hello World!"

# Handles error generally if route doesn't have try/except
@app.errorhandler(IntegrityError)
def handler(error):
    return {"error": str(error)}, 409

