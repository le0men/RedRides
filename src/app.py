from db import db
from flask import Flask, request
import json
from db import Ride, Request, User

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

# ---- USERS ----


# Get all users
@app.route("/api/users/")
def get_users():
    users = [u.serialize() for u in User.querty.all()]
    return success_response(users)


# Creates user
@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    try:
        new_user = User(
            password=body.get("password"),
            name=body.get("name"),
            email=body.get("email"),
            phone=body.get("phone"),
            grad_year=body.get("grad_year"),
        )
    except:
        failure_response("Part of input is not complete or invalid", 400)

    if User.query.filter_by(email=body["email"]).first() is not None:
        return failure_response("A user with that email already exists", 400)

    if User.query.filter_by(phone=body["phone"]).first() is not None:
        return failure_response("A user with that phone number already exists", 400)

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


# Get User by ID
@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found")
    return success_response(user.serialize())


# Deletes a user from id
@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


# login user
@app.route("/api/users/login/", methods=["POST"])
def login_user():
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if (
        email is None
        or not isinstance(email, str)
        or password is None
        or not isinstance(password, str)
    ):
        failure_response("Part of input is not complete or invalid", 400)

    if User.query.filter_by(email=body["email"]).first() is None:
        return failure_response("Email not Found")

    user = User.query.filter_by(email=email).first()

    if user.password != password:
        return failure_response("Incorrect Password", 400)

    return success_response(user.serialize())


# ---- RIDES ----


# Get all rides
@app.route("/api/rides/")
def get_rides():
    rides = [u.serialize() for u in Ride.querty.all()]
    return success_response(rides)


# Creates ride
@app.route("/api/rides/", methods=["POST"])
def create_ride():
    body = json.loads(request.data)
    try:
        new_ride = Ride(
            departure_city=body.get("departure_city"),
            arrival_city=body.get("arrival_city"),
            departure_time=body.get("departure_time"),
            arrival_time=body.get("arrival_time"),
            date=body.get("date"),
            available_seats=body.get("available_seats"),
            price=body.get("price"),
            driver_id=body.get("driver_id"),
        )
    except:
        failure_response("Part of input is not complete or invalid", 400)

    driver = get_user(body.get("driver_id"))
    # TODO: Check for conflicts, What is the format of the time passed in?
    # TODO: Need to add ride to driver's rides list.
    db.session.add(new_ride)
    db.session.commit()
    return success_response(new_ride.serialize(), 201)


# Get ride by ID
@app.route("/api/rides/<int:ride_id>/")
def get_ride(ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()
    if not ride:
        return failure_response("Ride not found")
    return success_response(ride.serialize())


# Deletes a ride from id
@app.route("/api/rides/<int:ride_id>/", methods=["DELETE"])
def delete_ride(ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()
    if not ride:
        return failure_response("Ride not found")
    db.session.delete(ride)
    db.session.commit()
    return success_response(ride.serialize())


# add user (passenger) to listing
@app.route("/api/rides/<int:listing_id>/<int:ride_id>/", methods=["POST"])
def add_user_to_ride(listing_id, ride_id):
    pass


# remove user (passenger) from listing
@app.route("/api/rides/<int:listing_id>/<int:ride_id>/", methods=["DELETE"])
def delete_user_from_ride(listing_id, ride_id):
    pass


# check if user is part of listing (either as driver or as passenger)
@app.route("/api/rides/<int:listing_id>/<int:ride_id>/", methods=["GET"])
def check_user_in_ride(listing_id, ride_id):
    pass


# ---- REQUESTS ----


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
