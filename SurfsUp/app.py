# Import the dependencies.
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
Base.prepare(autoload_with=engine)

# Save references to each table
stations_db = Base.classes.station
measurements = Base.classes.measurement


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
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start(YYYY-MM-DD)<br/>"
        f"/api/v1.0/start(YYYY-MM-DD)/end(YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        all_percip = []
        my_query = session.query(measurements.date, measurements.prcp).filter(measurements.date <= "2017-08-23" , measurements.date >= "2016-08-23").all()
        for date, prcp in my_query:
            percip_dict = {}
            percip_dict["date"] = date
            percip_dict["prcp"] = prcp
            all_percip.append(percip_dict)
        
        return jsonify(all_percip) 
    

@app.route("/api/v1.0/stations")
def stations():
        all_stations = []
        my_query = session.query(stations_db.station, stations_db.name, stations_db.latitude, stations_db.longitude, stations_db.elevation).all()
        for station,name,latitude,longitude,elevation in my_query:
             station_dict = {}
             station_dict["station"] = station
             station_dict["name"] = name
             station_dict["latitude"] = latitude
             station_dict["longitude"] = longitude
             station_dict["elevation"] = elevation
             all_stations.append(station_dict)

        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
        all_tobs = []
        my_query = session.query(measurements.date, measurements.tobs).filter(measurements.station == 'USC00519281', measurements.date <= "2017-08-23" , measurements.date >= "2016-08-23").all()
        for date, tobs in my_query:
            percip_dict = {}
            percip_dict["date"] = date
            percip_dict["tobs"] = tobs
            all_tobs.append(percip_dict)
        
        return jsonify(all_tobs) 

@app.route("/api/v1.0/<start>")
def start_date(start):
    all_temps = []
    my_query = session.query(func.min(measurements.tobs) , func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= start).all()
    for tmin, tmax, tavg in my_query:
        temps_dict = {}
        temps_dict["tmin"] = tmin
        temps_dict["tavg"] = tavg
        temps_dict["tmax"] = tmax
        all_temps.append(temps_dict)

    return jsonify(all_temps)

         

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    all_temps = []
    my_query = session.query(func.min(measurements.tobs) , func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date <= end, measurements.date >= start).all()
    for tmin, tmax, tavg in my_query:
        temps_dict = {}
        temps_dict["tmin"] = tmin
        temps_dict["tavg"] = tavg
        temps_dict["tmax"] = tmax
        all_temps.append(temps_dict)

    return jsonify(all_temps)

if __name__ == "__main__":
    app.run(debug=True)