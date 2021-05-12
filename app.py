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
    prcp_dict = {}

    for index, row in precipitation_df.iterrows():
        prcp_dict[row['date']] = row['prcp']

    return jsonify(prcp_dict)
    

#create stations route
@app.route('/api/v1.0/stations')
def stations():
    stations = []

    for index, row in stations_df.iterrows():
        stations.append(row['name'])

    return jsonify(stations)


#create tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    one_year_ago = pd.to_datetime(dt.date(2017, 8, 23) - dt.timedelta(days=365))
    
    tobs_df = merged_df[['date', 'tobs', 'name']]
    last_12_months_tobs_df = tobs_df.loc[(pd.to_datetime(tobs_df['date'], format='%Y-%m-%d')) > one_year_ago]
    waihee_12mo_tobs_df = last_12_months_tobs_df.groupby('name').get_group('WAIHEE 837.5, HI US')
    
    waihee_data = {}
    
    for index, row in waihee_12mo_tobs_df.iterrows():
        waihee_data[row['date']] = row['tobs']
        
    return jsonify(waihee_data)

#create start route
#@app.route('/api/v1.0/<start>')


#create start/end route
#@app.route('/api/v1.0/<start>/<end>')



if __name__ == '__main__':
    app.run(debug=True)