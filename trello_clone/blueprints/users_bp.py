from flask import Blueprint, request
from models.user import User, UserSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from auth import authorize

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/register", methods=["POST"])
@jwt_required()
def register():
    authorize() # Admin only
    try:
        # Parse incoming POST body through the schema (excludes id and is_admin to ensure users can't make themselves admin)
        user_info = UserSchema(exclude=["id", "is_admin"]).load(request.json)
        # Create a new user with the parsed data
        user = User(
            email=user_info["email"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode(
                "utf8"
            ),
            name=user_info.get("name", ""),
        )
        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()
        print(user.__dict__)
        # Return the new user (exludes password)
        return UserSchema(exclude=["password"]).dump(user), 201
    except IntegrityError:
        return {"error": "Email address already in use"}, 409


@users_bp.route("/login", methods=["POST"])
def login():
    # 1 Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id", "name", "is_admin"]).load(request.json)
    # 2 Select user with email that matches the one in the POST body
    # 3 Check the password hash matches
    stmt = db.select(User).where(User.email == user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        # 4 Create a JWT token
        token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=2)
        )  # ,additional_claims=["email": user.email])
        # 5 Return token to the client
        return {
            "token": token,
            "user": UserSchema(exclude=["password", "cards"]).dump(user),
        }  # Can also use only=[""] to keep the columns listed
    else:
        return {"error": "Invalid email or password"}, 401


# Get all users
@users_bp.route("/")
@jwt_required()
def all_users():
    authorize()
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password"]).dump(users)
