#import dependencies
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#############################################

#setup database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#save reference to measurement class
Measurement = Base.classes.measurement

#save reference to station class
Station = Base.classes.station

#############################################

#flask setup
app = Flask(__name__)

#create homepage route
@app.route('/')
def home():
    return (
        f'Welcome to the Hawaii Rainfall and Temperature API!<br/><br/>'
        f'Available Routes:<br/><br/>'
        f'To see pairs of dates and precipitation measurements in inches for various stations in Hawaii:<br/>'
        f'/api/v1.0/precipitation<br/><br/>'
        f'To see a list of the stations used for measurements:<br/>'
        f'/api/v1.0/stations<br/><br/>'
        f'To see temperature observations in degrees F for the Waihee station:<br/>'
        f'/api/v1.0/tobs<br/><br/>'
        f'To see minimum, maximum, and average temperatures since a certain date (in year-month-date format) in degrees F for all stations:<br/>'
        f'/api/v1.0/start_date<br/>'
        f'To see minimum, maximum, and average temperatures in a certain date range (in year-month-date format) in degrees F for all stations:<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
    )

#create precipitaion route
@app.route('/api/v1.0/precipitation')
def precipitation():
    #create session for the precipitation data
    session=Session(engine)

    #pull precipitation data from session
    prcp_readings = session.query(Measurement.date, Measurement.prcp)
    session.close()
    
    #convert into a dictionary
    prcp_dict = dict(prcp_readings)
    
    #jsonify and return
    return jsonify(prcp_dict)
    

#create stations route
@app.route('/api/v1.0/stations')
def stations():
    #create session for the station data
    session=Session(engine)

    #pull station names from session
    station_names = session.query(Station.name)
    session.close()
    
    #convert to a list
    stations = list(station_names)
    
    #jsonify and return
    return jsonify(stations)


#create tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    #create session for the precipitation data
    session=Session(engine)
    
    #get the date for the last year
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #pull the dates and temp observations from the waihee (most active) station for the past year
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                select_from(Measurement).\
                join(Station, Measurement.station == Station.station).\
                filter(Station.id == 7).\
                filter(Measurement.date > one_year_ago).all()
    session.close()
       
    #jsonify and return
    return jsonify(tobs_data)

#create start route
@app.route('/api/v1.0/<start>')
def min_max_avg(start):
    #format the input
    formatted_start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    #create session for the precipitation data
    session=Session(engine)
    
    #calculating minimum temp since start date
    tmin = session.query(Station. name, func.min(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date >= formatted_start_date).all()
    
    #calculating maximum temp since start date
    tmax = session.query(Station. name, func.max(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date >= formatted_start_date).all()
    
    #calculating average temp since start date
    tavg = session.query(Station. name, func.avg(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date >= formatted_start_date).all()
    
    session.close()
    
    return f'For dates since {start}: <br/><br/> Min Temp: {tmin} <br/><br/> Max Temp: {tmax} <br/><br/> Average Temp: {tavg}'

#create start/end route
@app.route('/api/v1.0/<start>/<end>')
def min_max_avg_range(start, end):
    #format the inputs
    formatted_start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    formatted_end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    #create session for the precipitation data
    session=Session(engine)
    
    #calculating minimum temp since start date
    tmin = session.query(Station. name, func.min(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date <= formatted_end_date).\
        filter(Measurement.date >= formatted_start_date).all()
    
    #calculating maximum temp since start date
    tmax = session.query(Station. name, func.max(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date <= formatted_end_date).\
        filter(Measurement.date >= formatted_start_date).all()
    
    #calculating average temp since start date
    tavg = session.query(Station. name, func.avg(Measurement.tobs)).\
        select_from(Measurement).\
        join(Station, Measurement.station == Station.station).\
        group_by(Measurement.station).\
        filter(Measurement.date <= formatted_end_date).\
        filter(Measurement.date >= formatted_start_date).all()
    
    session.close()
    
    return f'For dates in the range of {start} to {end}: <br/><br/> Min Temp: {tmin} <br/><br/> Max Temp: {tmax} <br/><br/> Average Temp: {tavg}'


if __name__ == '__main__':
    app.run(debug=True)