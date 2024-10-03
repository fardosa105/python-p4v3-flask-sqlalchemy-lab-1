# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        response = make_response(
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year,
            },
            200,
        )
    else:
        response = make_response({"message": f"Earthquake {id} not found."}, 404)
    return response


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_minimum_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquakes_length = len(earthquakes)
    quakes = []
    for earthquake in earthquakes:
        quakes.append(
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year,
            }
        )
    if earthquakes_length > 0:
        response = make_response({"count": earthquakes_length, "quakes": quakes}, 200)
    else:
        response = make_response({"count": 0, "quakes": []}, 200)
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
