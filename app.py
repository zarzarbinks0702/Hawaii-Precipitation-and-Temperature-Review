#import flask dependencies
from flask import Flask, jsonify
import csv

#flask setup
app = Flask(__name__)

#create homepage route
@app.route('/')
def home():
    return (
        f'Welcome to the Hawaii Rainfall and Temperature API!<br/>'
        f'Available Routes:<br/>'
        f'To see pairs of dates and precipitation measurements in inches for various stations in Hawaii: /api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'//api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

#create precipitaion route
@app.route('/api/v1.0/precipitation')
def precipitation():
    with open('Resources/hawaii_measurements.csv') as csv_file_1:
        precipitation_csv = csv.reader(csv_file_1, delimiter=',')

        prcp_dict = {}

        for row in precipitation_csv:
            prcp_dict[row[1]] = row[2]

        return jsonify(prcp_dict)
    

#create stations route
@app.route('/api/v1.0/stations')
def stations():
    with open('Resources/hawaii_stations.csv') as csv_file_2:
        stations_csv = csv.reader(csv_file_2, delimiter=',')
        stations = []

        for row in stations_csv:
            stations.append(row[1])

        return jsonify(stations)


#create tobs route
#@app.route('/api/v1.0/tobs')


#create start route
#@app.route('/api/v1.0/<start>')


#create start/end route
#@app.route('/api/v1.0/<start>/<end>')



if __name__ == '__main__':
    app.run(debug=True)