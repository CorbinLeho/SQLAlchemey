import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Declare a Base using `automap_base()`
Base = automap_base()

# Reflect Database into ORM classes
Base.prepare(engine, reflect=True)

# Save a reference to the measurement table as 'Measurement'
Measurement = Base.classes.measurement

# Save a reference to the station table as 'Station'
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
    return (
        "Hawaii Weather Data<br/><br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "/api/v1.0/stations<br/><br/>"
    )
 
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_entry = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_from_last = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_from_last).order_by(Measurement.date).all()
    precip = []
    for p in results:
        prcp_data = {}
        prcp_data["Date"] = p.date
        prcp_data["Precipitation"] = p.prcp
        precip.append(prcp_data)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
	results = session.query(Station).all()
	all = []
	for station in results:
		station_data = {}
		station_data["station"] = station.station
		station_data["station name"] = station.name
		station_data["latitude"] = station.latitude
		station_data["longitude"] = station.longitude
		station_data["elevation"] = station.elevation
		all.append(station_data)
		
	return jsonify(all)

if __name__ == '__main__':
    app.run(debug=True)
