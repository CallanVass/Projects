from flask import Blueprint
from flask_jwt_extended import jwt_required
from setup import db
from models.card import CardSchema, Card
from auth import admin_required


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("/")
@jwt_required()
def all_cards():
    # admin_required()
    # Select * from cards;
    stmt = db.select(Card)#.where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
    # dump() will convert a Python object into a JSON object, 
    # dumps() encodes a Python object into JSON string, 
    # which makes it more readily readable to more frameworks/languages.


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

# @cards_bp.route("/")
# @jwt_required()
# def all_cards():
#     admin_required()
#     # Select * from cards;
#     stmt = db.select(Card)#.where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
#     cards = db.session.scalars(stmt).all()
#     return CardSchema(many=True).dump(cards)
#     # dump() will convert a Python object into a JSON object, 
#     # dumps() encodes a Python object into JSON string, 
#     # which makes it more readily readable to more frameworks/languages.