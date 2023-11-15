from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create instance of the app
app = Flask(__name__)

# Connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://trello_dev:callan@127.0.0.1:5432/trello"

# Import (must be after config but before routes/error handlers)
db = SQLAlchemy(app)

# Declaring a model to create a table in the database (postgresql) (entity)
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    date_created = db.Column(db.Date())

@app.route("/")
def index():
    return "Hello World!"

