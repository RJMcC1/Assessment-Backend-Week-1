"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)

@app.route('/between', methods=['POST'])
def between_dates():
    add_to_history(request)
    body = request.json

    if not body or 'first' not in body or 'last' not in body:
        return {'error': 'Missing required data.'}, 400

    try:
        first = convert_to_datetime(body['first'])
        last = convert_to_datetime(body['last'])
    except Exception:
        return {'error': 'Unable to convert value to datetime.'}, 400

    days_between = get_days_between(first, last)
    return jsonify({"days": days_between})


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })

@app.route('/history', methods=['GET', 'DELETE'])
def history():
    """Returns the last n requests."""
    if request.method == 'GET':
        add_to_history(request)
        raw = request.args.get('number')

        if raw is None:
            number = 5  
        else:
            number = request.args.get('number', type=int)
            if number is None or number < 1 or number > 20:
                return {'error': 'Number must be an integer between 1 and 20.'}, 400
        return jsonify(app_history[-number:])
    if request.method == 'DELETE':
        app_history.clear()
        return jsonify({'status': 'History cleared'}), 200
    
    

def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.route('/weekday' , methods =['POST'])
def getting_weekdays():
    add_to_history(request)
    body = request.json

    if not body or 'date' not in body :
        return {'error': 'Missing required data.'}, 400
    try:
        date = convert_to_datetime(body['date'])
    except Exception:
        return {'error': 'Unable to convert value to datetime.'}, 400


    weekday = get_day_of_week_on(date)
    return jsonify({"weekday": weekday})



@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
