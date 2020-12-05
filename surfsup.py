# Import Dependencies

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Column, Integer, String, Float, Date

from flask import Flask, jsonify

# Create and connect Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Stations = Base.classes.station

# connect session with engine
session = Session(engine)


app = Flask(__name__)

# Homepage
@app.route("/")
def main():
    # Gives the user the options of where they can go
    return (
        f"Please copy and paste one of the follwing to the end of the above URL:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"or<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creates a query that looks for the most recent date stripped from the year, month, day
    most_recent_date = session.query(
        func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()

    # Transforms SQl query into a string
    string_version = most_recent_date[0][0]
    end_date = dt.datetime.strptime(string_version, "%Y-%m-%d")

    # Subtracts one year from the most recent data row
    start_date = end_date - dt.timedelta(365)

    # Creates a query taht retrieves the data and percipitation from anything greater than
    # or equal to the start date, filtered by the date
    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).all()

    # Creates a dictionary and put the resutls in said dictionary
    results = {}
    for result in precip_data:
        results[result[0]] = result[1]

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():

    # query stations list
    stations_ = session.query(Stations).all()

    # create a list of dictionaries
    stations_list = []
    for station in stations_:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)


# @app.route("/api/v1.0/<start>")
# @api.route("/api/v1.0/<start>/<end>")
