from flask import Blueprint
from setup import db, bcrypt
from models.card import Card
from models.user import User
from models.comment import Comment
from datetime import date

# Declaring the blueprint (Dunders are variables or functions that have a special meaning)
db_commands = Blueprint("db", __name__)

# Declaring a cli command
@db_commands.cli.command("create")
def db_create():
    # Drop table
    db.drop_all()
    # Create table
    db.create_all()
    print("Created tables")

@db_commands.cli.command("seed")
def db_seed():
    users = [
        User(
            email="admin@spam.com",
            password=bcrypt.generate_password_hash("spam").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="John",
            email="john@spam.com",
            password=bcrypt.generate_password_hash("tisbutascratch").decode("utf-8"),
            is_admin=False
        )

    ]
    # These could all move to the bottom, however if we create the users first, we
    # can dynamically reference them.
    db.session.add_all(users)
    db.session.commit()
    cards = [
    Card(
        title = "Start the project",
        description = "Stage 1 = Create ERD",
        status = "Done",
        date_created = date.today(),
        user_id = 1
    ),
    Card(
        title = "ORM Queries",
        description = "Stage 2 = Implement CRUD queries",
        status = "In Progress",
        date_created = date.today(),
        # Another way to get the user dynamically after it's been commited
        user_id = users[0].id
    ),
    Card(
        title = "Marshmallow",
        description = "Stage 3 = Implement JSONify of models",
        status = "In Progress",
        date_created = date.today(),
        user_id = 2
    ),
    ]
    
    
    # Adding transaction to queue
    db.session.add_all(cards)
    # Commiting transaction
    db.session.commit()

    comments = [
        Comment(
            message = "comment 1",
            user_id = users[0].id,
            card_id=cards[2].id
        ),
        Comment(
            message = "comment 2",
            user_id = users[1].id,
            card_id=cards[2].id
        ),
        Comment(
            message = "comment 3",
            user_id = users[1].id,
            card_id=cards[0].id
        ),
    ]
    db.session.add_all(comments)
    db.session.commit()
    print("Database Seeded")