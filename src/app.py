from db import db
from flask import Flask, request
import json
from db import Listing, User

app = Flask(__name__)
db_filename = "rr.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# Routes

# Get all users
@app.route("/api/users/")
def get_users():
    pass

# Creates user
@app.route("/api/users/", methods=["POST"])
def create_user():
    pass

# Get User by ID
@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    pass

# Deletes a user from id
@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(course_id):
    pass

# Get all listings
@app.route("/api/listings/")
def get_listings():
    pass

# Creates listing
@app.route("/api/listings/", methods=["POST"])
def create_listing():
    pass

# Get listing by ID
@app.route("/api/users/<int:listing_id>/")
def get_listing(listing_id):
    pass

# Deletes a user from id
@app.route("/api/users/<int:listing_id>/", methods=["DELETE"])
def delete_listing(listing_id):
    pass

# add user to listing
@app.route("/api/listings/<int:listing_id>/add/", methods=["POST"])
def add_user(listing_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)