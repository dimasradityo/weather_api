from flask import Flask, render_template
import pandas as pd
import numpy as np
import datetime as dt

app = Flask('__name__')

stations_reference = pd.read_csv('data_small/stations.txt', skiprows=17)

def clean_data(station_id):
    station_filename = 'TG_STAID'+str(station_id).zfill(6)+'.txt'
    df = pd.read_csv('data_small/' + station_filename, skiprows=20, parse_dates=['    DATE'])
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0']/10
    return df


# Homepage 
@app.route('/')
def home():
    return render_template('home.html', data=stations_reference.to_html())

# GET temperature data for station and date
@app.route('/api/v1/<station>/<date>')
def about(station, date):
    df = clean_data(station)
    temperature = df.loc[df['    DATE']==date]['TG'].squeeze()
    return {
"station": station,
"date": date,
"temperature": temperature
    }

# GET all temperature data for a station
@app.route('/api/v1/<station>')
def get_all_temperature_for_station(station):
    df = clean_data(station)
    result = df[['    DATE','TG']].to_dict(orient='records')
    return result

# GET all temperature data for a station only for specified year
@app.route('/api/v1/yearly/<station>/<year>')
def get_all_temperature_for_station_year(station, year):
    df = clean_data(station)
    yearly_data = df[df['    DATE'].dt.year == int(year)]
    result = yearly_data[['    DATE','TG']].to_dict(orient='records')
    return result

if __name__ == '__main__':
    app.run(debug=True)