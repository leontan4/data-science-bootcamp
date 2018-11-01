import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Surfing Page!!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return a list of percipitation"""

    measure = session.query(Measurement).all()
    all_data = []
    for data in measure:
        measurement_dict = {
            "Date": data["date"],
            "Precipitation": data["prcp"]
        }

        all_data.append(measurement_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations

    measure = session.query(Measurement).all()
    station_data = []
    for station in measure:
        station_dict = {

            "Stations": station.station,
            "Precipitation": station.prcp,
            "Tobs": station.tobs
        }

        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs"""
    # Query all tobs

    measure = session.query(Measurement).all()
    tobs_data = []
    for tobs in measure:
        tobs_dict = {
            "Date": tobs.date,
            "TOBS": tobs.tobs
        }

        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start_date):
    """Return a list from start date"""
    # Query all columns from start date

    measure = session.query(Measurement).all()
    start_dates = []
    for date in measure:
        start_dict = {
            "Date": date.date
        }

        start_dates.append(start_dict)

    return jsonify(start_dates)
if __name__ == '__main__':
    app.run(debug=True)
