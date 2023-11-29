from setup import db, ma
from marshmallow import fields


# Create user instance
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    cards = db.relationship("Card", back_populates="user")
    # backpopulates links the relationships

class UserSchema(ma.Schema):
    # Pass the list as a parameter t
    cards = fields.Nested("CardSchema", exclude=["user"], many=True) # Can also use fields.List()

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "cards")