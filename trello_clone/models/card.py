from setup import db, ma
from datetime import datetime
from marshmallow import fields

# Declaring a model to create a table in the database (postgresql) (entity)
class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    status = db.Column(db.String(30), default="To Do")
    date_created = db.Column(db.Date(), default=datetime.now().strftime("%Y-%m-%d"))
    # Establishes database relationship via foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # SQLAlchemy relationship: nests an instance of a related model in this one
    user = db.relationship("User", back_populates="cards")
    # backpopulates links the relationships
   
class CardSchema(ma.Schema):
    # References the UserSchema to produce nested result inside the card (of the user)
    # Tell Marshmallow to next a UserSchema instance when serializing
    user = fields.Nested("UserSchema", exclude=["password"])

    class Meta:
        fields = ("id", "title", "description", "status", "date_created", "user")