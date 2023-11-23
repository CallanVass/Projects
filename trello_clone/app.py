from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from os import environ


# ENSURE YOU UNTRACK .FLASKENV

# ACL = Access Control List
# Create instance of the app
app = Flask(__name__)


# Connection string
# This could be generated at random every now and then (coded, obviously)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://trello_dev:callan@127.0.0.1:5432/trello"

# Import (must be after config but before routes/error handlers)
# Pass instances of flask app to the modules
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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
    try:
        # Parse incoming POST body through the schema (excludes id and is_admin to ensure users can't make themselves admin)
        user_info = UserSchema(exclude=["id", "is_admin"]).load(request.json)
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
    except IntegrityError:
        return {"error": "Email address already in use"}, 409


@app.route("/users/login", methods=["POST"])
def login():
    # 1 Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id", "name", "is_admin"]).load(request.json)
    # 2 Select user with email that matches the one in the POST body
    # 3 Check the password hash matches
    stmt = db.select(User).where(User.email == user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        # 4 Create a JWT token
        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=2)) # ,additional_claims=["email": user.email])
        # 5 Return token to the client
        return {"token": token, "user": UserSchema(exclude=["password"]).dump(user)}
    else:
        return {"error": "Invalid email or password"}, 401



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

