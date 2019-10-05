import json
from datetime import datetime, timedelta, date
from random import random
import sys
from flask import Flask, request, jsonify, render_template
import databuild_gcp

app = Flask(__name__)

allSegments = []
allStays = []

# The start of the replay window (which we are replaying)
global record_start

# Time at which the application was started 
global current_start

# TODO: Replay speed

def get_time_in_replay_window(current_datetime):
    return int(current_datetime.timestamp()) - current_start + record_start

def getTimestampParam(defaultSecondsAgo):
    replay_moment = get_time_in_replay_window(datetime.now())
    t = int(replay_moment - defaultSecondsAgo*replay_speed)

    return t

def readSegments():
    global allSegments
    allSegments = json.load(open('segments_production.json'))
    for s in allSegments:
        fuzz = int((random()-0.5)*300*1000)
        s['departure_timestamp'] += fuzz
        s['arrival_timestamp'] += fuzz

@app.route('/api/v1/segments')
def apisegments():
    until = getTimestampParam(defaultSecondsAgo=-60*60)
    now = get_time_in_replay_window(datetime.now())
    segments = [
        s for s in allSegments if s['departure_timestamp'] <= until and s['arrival_timestamp'] >= now
    ]
    return jsonify(segments)

@app.route('/api/v1/timestamps')
def get_timestamps():
    return {"replay":record_start, "start":current_start}

@app.route('/')
def index():

    data = {'record_start': record_start,
    'current_start': current_start,
    'replay_speed': replay_speed}
    return render_template("index.html", data=data)

if __name__ == '__main__':
    datetime_arg = sys.argv[1] #Grab a date in format yyyy-mm-dd*[HH[MM[SS]]]
    start_time = datetime.fromisoformat(datetime_arg)

    try:
        replay_speed = int(sys.argv[2]) # expect an integer
    except IndexError:
        replay_speed = 1

    #Start of the recorded period we are replaying
    record_start = int(start_time.timestamp())

    #Time at which we started to play the recording
    current_start = int(datetime.now().timestamp())

    time_delta = record_start - current_start

    segments_df =  databuild_gcp.query_gcp_flight_segments(record_start)
    segments_df.to_json('segments_production.json', orient='records')

    readSegments()

    until = getTimestampParam(defaultSecondsAgo=-60*60)
    now = get_time_in_replay_window(datetime.now())
    
    app.run('0.0.0.0', port=11156, debug=True)

