from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Classes

class User(db.Model):
  pass

class Listing(db.Model):
  pass

