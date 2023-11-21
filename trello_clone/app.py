from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

# Create instance of the app
app = Flask(__name__)

# Connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://trello_dev:callan@127.0.0.1:5432/trello"

# Import (must be after config but before routes/error handlers)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

# Declaring a model to create a table in the database (postgresql) (entity)
class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

   
class CardSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "status", "date_created")

# Create user instance
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin")

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

@app.route("/users/register", methods=["POST"])
def register():
    # Parse incoming POST body through the schema (excludes id)
    user_info = UserSchema(exclude=["id"]).load(request.json)
    # Create a new user with the parsed data
    user = User(
        email=user_info["email"],
        password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
        name=user_info.get("name", "")
    )
    # Add and commit the new user to the database
    db.session.add(user)
    db.session.commit()
    print(user.__dict__)
    # Return the new user (exludes password)
    return UserSchema(exclude=["password"]).dump(user), 201



@app.cli.command("all_cards")
def all_cards():
    # Select different orders from cards;
    stmt = db.select(Card).where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    # Select * from cards;
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    # print(list(cards)) FOR DEBUGGING
    for card in cards:
        print(card.__dict__)
    # Could also use __repr__ for a string representation of an object

@app.route("/cards")
def all_cards():
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

