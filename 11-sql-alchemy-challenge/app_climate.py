import numpy as np

import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
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
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/station<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"/api/v1.0/date1/<start_date><br/>"
        f"/api/v1.0/date1/<start_date>/<end_date>"
    )

# Appending the dates and precipitation
@app.route("/api/v1.0/precipitation3/")
def precipitation():

    results = session.query(Measurement).filter(Measurement.prcp != None)
    all_data = {}
    
    for test in results:
        all_data[test.date] = test.prcp

    return jsonify(all_data)

# Getting all the stations ID
@app.route("/api/v1.0/stations1")
def stations():

    results = session.query(Station)
    station_list = []
    for station in results:

        station_dict={}
        station_dict["Station ID"] = station.station
        station_dict["Location"] = station.name
        station_list.append(station_dict)

    return jsonify(station_list)

# Reformat the tobs
@app.route("/api/v1.0/tobs")
def tobs():

    results = session.query(Measurement).filter(Measurement.date >= "2016-08-23")
    tobs_list = []
    for temperature in results:

        tobs_dict={}
        tobs_dict["Date"] = temperature.date
        tobs_dict["TOBS"] = temperature.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


# Finding values with start date
@app.route("/api/v1.0/date2/<start_date>")
def calc_temps(start_date):
    
    measure = session.query(Measurement).filter(Measurement.station >= start_date).all()
    
    all_dict = {}
    temps = []
    for test in measure:
        temps.append(test.tobs)
        
    all_dict = {
        "Mix Temp": min(temps),
        "Max Temp": max(temps),
        "Avg Temp": sum(temps)/len(temps)
        
    }

    return jsonify(all_dict)

@app.route("/api/v1.0/date/<start_date>/<end_date>")
def calc_total(start_date, end_date):
    
    measure = session.query(Measurement).filter(Measurement.station >= start_date).filter(Measurement.station <= end_date).all()
    
    total_dict = {}
    temps_total = []
    for test in measure:
        temps_total.append(test.tobs)
        
    total_dict = {
        "Mix Temp": min(temps_total),
        "Max Temp": max(temps_total),
        "Avg Temp": sum(temps_total)/len(temps_total)
        
    }

    return jsonify(total_dict)

if __name__ == '__main__':
    app.run(debug=True)

