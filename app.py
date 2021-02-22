# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Add the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask dependencies
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a varaible for each reference to save them to a table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session link from Python to our database. 
session = Session(engine)

# Define Flask app 
app = Flask(__name__)

# Define welcome route
@app.route("/")

# Add routing info for each of the other routes
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tabs
        /api/v1.0/temp/start/end
        ''')

# Create route for the precipitation data for the last year 
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create the stations route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create the tabs route
@app.route("/api/v1.0/tabs")

# Create temp_month function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create route for starting end date

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)