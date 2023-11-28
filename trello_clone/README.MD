# Overview

This project is a Trello Clone API (lacking any sort of front-end as of yet) that allows users to create new cards, delete them, login, and signup.

# Software and Dependencies

## Flask

- The main application runs on the Flask framework, which is a lightweight API framework that uses Python. In setup.py, you will see the creation of the application with the line:

app = Flask(__name__)

- This creases an instance of the application for us to work with in the future when we want to refer to the application itself.

## SQLAlchemy

- SQLAlchemy is an ORM (Object Relational Mapper) that allows us to translate between the data representations used by databases and those is our code. This means we can query the database (lookup something in the database) in a simplified manner, and also create Models (essentially classes). Setup.py also has a declaration of SQLAlchemy's instance:

db = SQLAlchemy(app)

## Marshmallow

- An integration with SQLAlchemy, marshmallow allows us to create Schemas for SQLAlchemy Models and deserialize incoming or outgoing information.


