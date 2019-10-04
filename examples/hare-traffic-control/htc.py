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
global replay_timestamp

# Time at which the application was started 
global start_timestamp

# TODO: Replay speed

def get_time_in_replay_window(current_datetime):
    return int(current_datetime.timestamp()) - start_timestamp + replay_timestamp

def getTimestampParam_2(name, defaultSecondsAgo):
    replay_moment = get_time_in_replay_window(datetime.now())
    t = int(replay_moment - defaultSecondsAgo)
    if t > replay_moment * 100:   # in case it was millis
        t = int(t/1000)
    return t

def getTimestampParam(name, defaultSecondsAgo):
    replay_moment = get_time_in_replay_window(datetime.now())
    t = int(request.args.get(name, replay_moment - defaultSecondsAgo))
    if t > replay_moment * 100:   # in case it was millis
        t = int(t/1000)
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
    until = getTimestampParam('until', defaultSecondsAgo=-60*60)
    now = get_time_in_replay_window(datetime.now())

    segments = [
        s for s in allSegments if s['departure_timestamp'] <= until and s['arrival_timestamp'] >= now
    ]
    return jsonify(segments)

@app.route('/api/v1/timestamps')
def get_timestamps():
    return {"replay":replay_timestamp, "start":start_timestamp}

@app.route('/')
def index():

    data = {'replay_timestamp': replay_timestamp,
    'start_timestamp': start_timestamp}
    return render_template("index.html", data=data)

if __name__ == '__main__':
    datetime_arg = sys.argv[1] #Grab a date in format yyyy-mm-dd*[HH[MM[SS]]]
    start_time = datetime.fromisoformat(datetime_arg)

    #Start of the time period we are replaying
    replay_timestamp = int(start_time.timestamp())

    #Time at which we started the replay
    start_timestamp = int(datetime.now().timestamp())

    print(f'replay timestamp = {replay_timestamp}, start_timestamp = {start_timestamp}')

    app.config['replay_timestamp'] = replay_timestamp
    app.config['start_timestamp'] = start_timestamp

    #segments_df =  databuild_gcp.query_gcp_flight_segments(replay_timestamp)
    #segments_df.to_json('segments_production.json', orient='records')

    readSegments()

    until = getTimestampParam_2('until', defaultSecondsAgo=-60*60)
    now = get_time_in_replay_window(datetime.now())

    print(f'until: {until}, now: {now}')

    print(f'until: {datetime.fromtimestamp(until)}, now: {datetime.fromtimestamp(now)}')
    print(f"{min([s['departure_timestamp'] for s in allSegments if s['departure_timestamp'] <= until and s['arrival_timestamp'] >= now])}")
    
    app.run('0.0.0.0', port=11156, debug=True)

