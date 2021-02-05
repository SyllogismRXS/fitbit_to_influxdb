import os
import json
from influxdb import InfluxDBClient

from fitbit_to_influxdb.line_protocols import write_intraday_activities

file_type_map = {'activities-heart.json': write_intraday_activities,
                 'activities-distance.json': write_intraday_activities,
                 'activities-steps.json': write_intraday_activities,
                 'activities-minutesSedentary.json': write_intraday_activities,
                 'activities-minutesLightlyActive.json': write_intraday_activities,
                 'activities-minutesVeryActive.json': write_intraday_activities,
                 'activities-calories.json': write_intraday_activities,
                 'activities-minutesFairlyActive.json': write_intraday_activities}

def write_to_influxdb(profile_path, date_paths):
    # Create the database connection
    client = InfluxDBClient(host='localhost', port=8086)
    db_name = 'fitbit'
    client.create_database(db_name)
    client.switch_database(db_name)

    # Load in the profile
    with open(profile_path) as f:
        profile = json.load(f)

    for date_path in date_paths:
        for f in os.listdir(date_path['path']):
            try:
                file_type_map[f](f, client, profile, os.path.join(date_path['path'], f))
            except KeyError:
                print('Ignoring: %s' % f)
