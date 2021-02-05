import json

from fitbit_to_influxdb.utils import make_influx_safe, get_date_from_string_with_zone
from fitbit_to_influxdb.utils import get_unix_time_seconds

def heart_rate_line_2(user, heart_rate, timestamp):
    return f"heart_rate_fine,user={user} heart_rate={heart_rate}i {timestamp}"

def heart_rate_line(date, time_24, user, heart_rate):
    return heart_rate_line_2(user, heart_rate, get_unix_time_seconds(date, time_24))

def write_activities_heart(db_client, profile, file_path):
    with open(file_path) as f:
        heart = json.load(f)

    header = heart['activities-heart']
    heart_rate_data = heart['activities-heart-intraday']['dataset']

    time_zone_string = profile['user']['timezone']
    date_string = header[0]['dateTime']
    user = make_influx_safe(profile['user']['timezone'])

    date = get_date_from_string_with_zone(time_zone_string, date_string)

    data = [ heart_rate_line(date, data_point['time'], user, data_point['value'])
             for data_point in heart_rate_data ]

    if not db_client.write_points(data, time_precision='s', batch_size=10000, protocol='line'):
        print('Failed to write to database.')
