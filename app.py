#import flask dependencies
from flask import Flask, jsonify
import csv
import datetime as dt
import pandas as pd

#create the precipitation df
precipitation_csv = 'Resources/hawaii_measurements.csv'
precipitation_df = pd.read_csv(precipitation_csv, encoding='ISO-8859-1')

#create the stations df
stations_csv = 'Resources/hawaii_stations.csv'
stations_df = pd.read_csv(stations_csv, encoding='ISO-8859-1')

#create the merged df
merged_df = pd.merge(precipitation_df, stations_df, on='station', how='outer')

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
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

#create precipitaion route
@app.route('/api/v1.0/precipitation')
def precipitation():
    #create dictionary for the precipitation data
    prcp_dict = {}

    #pull precipitation data into the dictionary
    for index, row in precipitation_df.iterrows():
        prcp_dict[row['date']] = row['prcp']

    #jsonify and return
    return jsonify(prcp_dict)
    

#create stations route
@app.route('/api/v1.0/stations')
def stations():
    #create list for the station names
    stations = []

    #pull station names into the list
    for index, row in stations_df.iterrows():
        stations.append(row['name'])

    #jsonify and return
    return jsonify(stations)


#create tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    #get the date one year ago
    one_year_ago = pd.to_datetime(dt.date(2017, 8, 23) - dt.timedelta(days=365))
    
    #create a separate tobs df
    tobs_df = merged_df[['date', 'tobs', 'name']]
    #pull the last 12 months of data from the tobs df
    last_12_months_tobs_df = tobs_df.loc[(pd.to_datetime(tobs_df['date'], format='%Y-%m-%d')) > one_year_ago]
    #pull just the waihee station data from the last 12 months of tobs data
    waihee_12mo_tobs_df = last_12_months_tobs_df.groupby('name').get_group('WAIHEE 837.5, HI US')
    
    #create dictionary for the tobs data
    tobs_data = {}
    
    #pull tobs data into the dictionary
    for index, row in waihee_12mo_tobs_df.iterrows():
        tobs_data[row['date']] = row['tobs']
       
    #jsonify and return
    return jsonify(tobs_data)

#create start route
#@app.route('/api/v1.0/<start>')


#create start/end route
#@app.route('/api/v1.0/<start>/<end>')



if __name__ == '__main__':
    app.run(debug=True)