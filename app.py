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


@app.route("/")
def hello():
    return "hello world"


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

    db.session.add(new_ride)
    driver.rides.append(new_ride)
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
@app.route("/api/rides/<int:user_id>/<int:ride_id>/", methods=["POST"])
def add_user_to_ride(user_id, ride_id):
    # TODO: Need to check if adding exceeding available spaces
    ride = Ride.query.filter_by(id=ride_id).first()
    if not ride:
        return failure_response("Ride not found")
    passenger = User.query.filter_by(id=user_id).first()
    if not passenger:
        return failure_response("User not found")

    if ride.available_seats == 0:
        return failure_response("Ride is full", 400)
    ride.available_seats -= 1
    ride.passengers.append(passenger)
    db.session.commit()
    return success_response(ride.serialize())


# ---- REQUESTS ----


# Get all requests
@app.route("/api/requests/")
def get_requests():
    requests = [u.serialize() for u in Request.query.all()]
    return success_response(requests)


# Creates request
@app.route("/api/requests/", methods=["POST"])
def create_request():
    body = json.loads(request.data)
    try:
        new_request = Request(
            ride_id=body.get("ride_id"),
            passenger_id=body.get("passenger_id"),
            status="pending",
        )
    except:
        failure_response("Part of input is not complete or invalid", 400)

    ride = Ride.query.filter_by(id=body["ride_id"]).first()
    if not ride:
        return failure_response("Ride not found")
    passenger = User.query.filter_by(id=body["passenger_id"]).first()
    if not passenger:
        return failure_response("User not found")

    db.session.add(new_request)
    db.session.commit()
    return success_response(new_request.serialize(), 201)


# Deletes a request from id
@app.route("/api/requests/<int:request_id>/", methods=["DELETE"])
def delete_request(request_id):
    request = Request.query.filter_by(id=request_id).first()
    if not request:
        return failure_response("Request not found")
    db.session.delete(request)
    db.session.commit()
    return success_response(request.serialize())


# Get request by ID
@app.route("/api/request/<int:request_id>/")
def get_request(request_id):
    request = Ride.query.filter_by(id=request_id).first()
    if not request:
        return failure_response("Request not found")
    return success_response(request.serialize())


# resolve a request
@app.route("/api/request/<int:request_id>/", methods=["POST"])
def resolve_request(request_id):
    body = json.loads(request.data)
    status = body.get("status")

    if status is None or (status != "yes" and status != "no"):
        failure_response("Part of input is not complete or invalid", 400)

    request = Request.query.filter_by(id=request_id).first()
    if not request:
        return failure_response("Request not found")

    request.status = status

    if status == "yes":
        add_user_to_ride(request.passenger_id, request.ride_id)
    db.session.commit()
    return success_response(request.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
