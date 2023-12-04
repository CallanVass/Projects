from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from setup import db
from models.comment import CommentSchema, Comment
from auth import authorize


comments_bp = Blueprint("comments", __name__, url_prefix="/<int:card_id>/comments")


# # Get all comments
# @comments_bp.route("/")
# @jwt_required()
# def all_comments():
#     # Select * from comments;
#     stmt = db.select(Comment
#     )#.where(db.or_(Comment.status != "Done", Comment.id > 2)).order_by(Comment.title.desc())
#     comments = db.session.scalars(stmt).all()
#     # Excludes comments embedded in the use (for the exclude=["user.comments"])
#     return CommentSchema(many=True, exclude=["user.comments"]).dump(comments)


# @comments_bp.route("/")
# @jwt_required()
# def all_comments():
#     authorize()
#     # Select * from comments;
#     stmt = db.select(Comment)#.where(db.or_(Comment.status != "Done", Comment.id > 2)).order_by(Comment.title.desc())
#     comments = db.session.scalars(stmt).all()
#     return CommentSchema(many=True).dump(comments)
#     # dump() will convert a Python object into a JSON object,
#     # dumps() encodes a Python object into JSON string,
#     # which makes it more readily readable to more frameworks/languages.


# Get one comment
# @comments_bp.route("/<int:id>")
# @jwt_required()
# def one_comment(id):
#     stmt = db.select(Comment).filter_by(id=id) # .where(Comment.id == id)
#     comment = db.session.scalar(stmt)
#     if comment:
#         # Prints user to terminal
#         print(comment.user)
#         # Returns CommentSchema
#         return CommentSchema().dump(comment)
#     else:
#         return {"error": "comment not found"}, 404


# Create a new comment
# POST /comments
# POST /cards/<card_id>/comments
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(card_id):
    comment_info = CommentSchema(only=["message"]).load(request.json)
    comment = Comment(
        message=comment_info["message"], user_id=get_jwt_identity(), card_id=card_id
    )
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201


# Update a comment
# PUT /cards/<card_id>/comments/<comment_id>
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_comment(card_id, comment_id):
    comment_info = CommentSchema(only=["message"]).load(request.json)
    stmt = db.select(Comment).filter_by(id=comment_id)  # .where(Comment.id == id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        comment.message = comment_info.get("message", comment.message)
        db.session.commit()
        return CommentSchema().dump(comment)
    else:
        return {"error": "Comment not found"}, 404


# Delete a comment
# Delete /cards/<card_id>/comments/<comment_id>
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(card_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)  # .where(Comment.id == id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        db.session.delete(comment)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "Comment not found"}, 404
