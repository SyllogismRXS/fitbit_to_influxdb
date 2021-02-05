import os
import sys
import argparse
import yaml
from pathlib import Path
from datetime import datetime, timedelta

from fitbit_to_influxdb.gather_keys_oauth2 import authorize
from fitbit_to_influxdb.download_fitbit_data import download_fitbit_data
from fitbit_to_influxdb.utils import get_date_from_string

def re_authorize_and_save(settings, ephemeral_path):
    token = authorize(settings['client_id'], settings['client_secret'])

    with open(ephemeral_path, 'w') as outfile:
        yaml.dump(token, outfile)

    return token

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings', default='settings.yaml', help='Path to persistent settings file.')
    parser.add_argument('-o', '--save_dir', default='data', help='Directory to save fitbit data.')
    parser.add_argument('-d', '--date', default=None, help='The date to download in the format: 2020-05-25')
    parser.add_argument('-e', '--end_date', default=None, help='The end date to download in the format: 2020-05-25')
    args = parser.parse_args()

    # Load the persistent settings file
    with open(args.settings) as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)

    # Get the the full path to the ephemeral settings yaml file relative to the
    # settings.yaml file and store it:
    ephemeral_path = os.path.join(Path(os.path.abspath(args.settings)).parent, settings['ephemeral_settings_path'])

    try:
        with open(ephemeral_path) as f:
            ephemeral = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        ephemeral = re_authorize_and_save(settings, ephemeral_path)

    # if the token is expired, re-authorize
    if datetime.now() > datetime.fromtimestamp(ephemeral['expires_at']):
        ephemeral = re_authorize_and_save(settings, ephemeral_path)

    if args.date is None:
        date = datetime.today()
    else:
        date = get_date_from_string(args.date)

    if args.end_date is None:
        end_date = date
    else:
        end_date = get_date_from_string(args.end_date)

    # Increment by one day until we have reached the end date
    while date <= end_date:
        print('Downloading data for...')
        print(date)

        # Download the data
        download_fitbit_data(settings, ephemeral, date, os.path.abspath(args.save_dir))

        # Increment by one day
        date = date + timedelta(days=1)

if __name__ == "__main__":
    sys.exit(main())
