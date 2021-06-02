# Hawaii Precipitation and Temperature Review

SQLAlchemy project with Flask for class - Uses Python, Pandas, Jupyter Notebook, SQLAlchemy, Flask, and DateTime. 05/15/2021

-----------------------------------------------------------------------------------------------------------------------

Used given sqlite file to create an engine in jupyter notebook.
Used SQLAlchemy to query both tables within the sqlite file to find the most recent date in the dataset and used that date to find the date one year prior to said date and pull the last 12 months of data.
Pulled date and precipitation columns into a dataframe and plotted the results.
Queried the sqlite document for the number of stations studied.
Found the most active station for the dataset and performed calculations of the temperature data.
Plotted results from this station in a histogram.

Created a flask app with routes to show precipitaion data, station names, temperature data, and the minimum, maximum, and average temperatures for each station in a given time frame.

-----------------------------------------------------------------------------------------------------------------------

Ran extra analysis to see if there was a meaningful difference between the temperature in June and December for Hawaii.
Ran an analysis on rainfall and temperatures in August for an August vacation.
Plotted temperature on a bar chart.
Plotted daily normals for the trip range in an area plot.

-----------------------------------------------------------------------------------------------------------------------

Runs in jupyter notebook and on a localhost server where Flask is installed.
