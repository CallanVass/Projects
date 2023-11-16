from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Create instance of the app
app = Flask(__name__)

# Connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://trello_dev:callan@127.0.0.1:5432/trello"

# Import (must be after config but before routes/error handlers)
db = SQLAlchemy(app)

# Declaring a model to create a table in the database (postgresql) (entity)
class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    date_created = db.Column(db.Date())

# Declaring a cli command
@app.cli.command("db_create")
def db_create():
    # Drop table
    db.drop_all()
    # Create table
    db.create_all()
    print("Created tables")

@app.cli.command("db_seed")
def db_seed():
    cards = [
    Card(
        title = "Start the project",
        description = "Stage 1 = Create ERD",
        date_created = date.today()
    ),
    Card(
        title = "ORM Queries",
        description = "Stage 2 = Implement CRUD queries",
        date_created = date.today()
    ),
    Card(
        title = "Marshmallow",
        description = "Stage 3 = Implement JSONify of models",
        date_created = date.today()
    ),
    ]
    # Adding transaction to queue
    db.session.add_all(cards)
    # Commiting transaction
    db.session.commit()

    print("Database Seeded")


@app.cli.command("all_cards")
def all_cards():
    # Select * from cards;
    stmt = db.select(Card)
    print(stmt)




# Declaring a route
@app.route("/")
def index():
    return "Hello World!"

