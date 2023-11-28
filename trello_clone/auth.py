from flask_jwt_extended import  get_jwt_identity
from flask import abort
from models.user import User
from setup import db

def admin_required():
    # Checking for user in header (decoded with jwt-get-identity) (Get email address)
    user_email = get_jwt_identity()
    # Check user email against the databasse
    stmt = db.select(User).where(User.email == user_email)
    # Get an instance of the model (stmt user model)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)
