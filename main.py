from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask('__name__')

def get_temperature(station_id, observation_date):
    station_filename = 'TG_STAID'+str(station_id).zfill(6)+'.txt'
    df = pd.read_csv('data_small/' + station_filename, skiprows=20, parse_dates=['    DATE'])
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0']/10
    return df.loc[df['    DATE']==observation_date]['TG'].squeeze()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/v1/<station>/<date>')
def about(station, date):
    temperature = get_temperature(station, date)
    return {
"station": station,
"date": date,
"temperature": temperature
    }

# @app.route('/api/v1/<keyword>')
# def api(keyword):
#     return {
# "definition": keyword.toupper(),
# "keyword": keyword
#     }

if __name__ == '__main__':
    app.run(debug=True, port=5001)