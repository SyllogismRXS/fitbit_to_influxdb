import re
import json

from fitbit_to_influxdb.utils import make_influx_safe, get_date_from_string_with_zone
from fitbit_to_influxdb.utils import get_unix_time_seconds

def line_protocol_activity_intraday(name, user, value, date, time_24):
    unix_time = get_unix_time_seconds(date, time_24)
    return f"{name}_intra,user={user} {name}={value} {unix_time}"

def line_protocol_activity(name, user, value, date):
    unix_time = get_unix_time_seconds(date, '00:00:00')
    return f"{name},user={user} {name}={value} {unix_time}"

def write_intraday_activities(file_name, db_client, profile, file_path):
    with open(file_path) as f:
        json_data = json.load(f)

    # Get the name of the activity from the json file
    name = re.search(r'intra-activities-(.*).json', file_name).group(1)

    header = json_data['activities-%s' % name]
    data = json_data['activities-%s-intraday' % name]['dataset']

    time_zone_string = profile['user']['timezone']
    date_string = header[0]['dateTime']
    user = make_influx_safe(profile['user']['timezone'])

    date = get_date_from_string_with_zone(time_zone_string, date_string)

    lines = [ line_protocol_activity_intraday(name, user, data_point['value'], date, data_point['time'])
              for data_point in data ]

    if not db_client.write_points(lines, time_precision='s', batch_size=10000, protocol='line'):
        print('Failed to write to database.')

def write_activities(file_name, db_client, profile, file_path):
    with open(file_path) as f:
        json_data = json.load(f)

    # Get the name of the activity from the json file
    name = re.search(r'activities-(.*).json', file_name).group(1)

    header = json_data['activities-%s' % name]

    time_zone_string = profile['user']['timezone']
    date_string = header[0]['dateTime']
    user = make_influx_safe(profile['user']['timezone'])
    value = header[0]['value']

    date = get_date_from_string_with_zone(time_zone_string, date_string)

    lines = [line_protocol_activity(name, user, value, date)]
    #lines = [ line_protocol_activity(name, user, data_point['value'], date, data_point['time'])
    #          for data_point in data ]

    if not db_client.write_points(lines, time_precision='s', batch_size=10000, protocol='line'):
        print('Failed to write to database.')
