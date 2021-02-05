import os
import fitbit
from pathlib import Path
from datetime import datetime
import json

from fitbit_to_influxdb.utils import get_date_string

def save_intraday_time_series(client, name, date, detail_level, output_dir):
    data = client.intraday_time_series(name, date, detail_level=detail_level)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(output_dir, 'intra-' + name.replace('/','-') + '.json'), 'w') as fp:
        json.dump(data, fp)

def save_time_series(client, name, date, period, output_dir):
    data = client.time_series(name, user_id=None, base_date=date, period='1d', end_date=None)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(output_dir, name.replace('/','-') + '.json'), 'w') as fp:
        json.dump(data, fp)


def download_fitbit_data(settings, ephemeral, date, save_dir):
    authd_client = fitbit.Fitbit(
        settings['client_id'],
        settings['client_secret'],
        access_token=ephemeral['access_token'],
        refresh_token=ephemeral['refresh_token'],
        expires_at=ephemeral['expires_at'])

    # Make the save_dir if it doesn't exist
    output_dir = os.path.join(save_dir, get_date_string(date))
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save the profile:
    profile = authd_client.user_profile_get()
    with open(os.path.join(save_dir, 'profile.json'), 'w') as fp:
        json.dump(profile, fp)

    if 'intraday_time_series' in settings:
        for item in settings['intraday_time_series']:
            save_intraday_time_series(authd_client, item['name'], date, item['detail_level'], output_dir)

    if 'time_series' in settings:
        for item in settings['time_series']:
            save_time_series(authd_client, item, date, '1d', output_dir)
