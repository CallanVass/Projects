from flask import Blueprint
from setup import db, bcrypt
from models.card import Card
from models.user import User
from datetime import date

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

    cards = [
    Card(
        title = "Start the project",
        description = "Stage 1 = Create ERD",
        status = "Done",
        date_created = date.today(),
    ),
    Card(
        title = "ORM Queries",
        description = "Stage 2 = Implement CRUD queries",
        status = "In Progress",
        date_created = date.today()
    ),
    Card(
        title = "Marshmallow",
        description = "Stage 3 = Implement JSONify of models",
        status = "In Progress",
        date_created = date.today()
    ),
    ]
    # Adding transaction to queue
    db.session.add_all(cards)
    db.session.add_all(users)
    # Commiting transaction
    db.session.commit()

    print("Database Seeded")