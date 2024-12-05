from flask import Flask, render_template

app = Flask('__name__')

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/api/v1/<station>/<date>')
# def about(station, date):
#     return {
# "station": station,
# "date": date
#     }

@app.route('/api/v1/<keyword>')
def api(keyword):
    return {
"definition": keyword.toupper(),
"keyword": keyword
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001)