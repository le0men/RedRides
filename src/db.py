from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Classes

# many-many table
association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("ride_id", db.Integer, db.ForeignKey("ride.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)


# id, email, and phone numbers must be unique, phone number and grad year don't have to be
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)
    requests = db.relationship("Request")
    rides = db.relationship(
        "User", secondary=association_table, back_populates="passengers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "grad_year": self.grad_year,
            "requests": [s.serialize() for s in self.requests],
            "rides": [s.simple_serialize() for s in self.rides],
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "grad_year": self.grad_year,
        }


class Ride(db.Model):
    __tablename__ = "ride"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure_city = db.Column(db.String, nullable=False)
    arrival_city = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    driverId = db.Column(db.Integer, nullable=False)
    requests = db.relationship("Request", cascade="delete")
    passengers = db.relationship(
        "User", secondary=association_table, back_populates="rides"
    )

    def serialize(self):
        return {
            "id": self.id,
            "departure_city": self.departure_city,
            "arrival_city": self.arrival_city,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "data": self.date,
            "available_seats": self.available_seats,
            "price": self.price,
            "driverId": self.driverId,
            "requests": [s.serialize() for s in self.requests],
            "passengers": [s.simple_serialize() for s in self.passengers],
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "departure_city": self.departure_city,
            "arrival_city": self.arrival_city,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "data": self.date,
            "available_seats": self.available_seats,
            "price": self.price,
            "driverId": self.driverId,
        }


class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ride_id = db.Column(
        db.Integer, db.ForeignKey("ride.id"), primary_key=True, autoincrement=True
    )

    # TODO: make this reference an the id of an existing passenger
    passenger_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, autoincrement=True
    )

    # must be either "yes", "no", or "pending"
    status = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "ride_id": self.ride_id,
            "passenger_id": self.passenger_id,
            "status": self.status,
            "passenger_name": User.query.filter_by(id=self.passenger_id).first(),
        }
