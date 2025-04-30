from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Classes


# id, email, and phone numbers must be unique, phone number and grad year don't have to be
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    grad_year = db.Column(db.Int, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "grad_year": self.grad_year,
        }


class Listing(db.Model):
    __tablename__ = "listing"
    ride_id = db.Column(db.Integer, primary_key=True)

    # TODO: make this reference an the id of an existing passenger
    passenger_id = db.Column(db.String, nullable=False)

    # must be either "yes", "no", or "pending"
    status = db.Column(db.String, nullable=False)

    # must be the name of an existing passenger
    # TODO (maybe): make this reference the name of an existing user
    passenger_name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "ride_id": self.ride_id,
            "passenger_id": self.passenger_id,
            "status": self.status,
            "passenger_name": self.passenger_name,
        }
