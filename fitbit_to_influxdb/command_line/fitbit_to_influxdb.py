import os
import sys
import argparse
import yaml
from pathlib import Path
from datetime import datetime

from fitbit_to_influxdb.gather_keys_oauth2 import authorize
from fitbit_to_influxdb.fitbit_client import FitbitClient

def re_authorize_and_save(settings, ephemeral_path):
    token = authorize(settings['client_id'], settings['client_secret'])

    with open(ephemeral_path, 'w') as outfile:
        yaml.dump(token, outfile)

    return token

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', default='settings.yaml', help='Path to persistent settings file.')
    parser.add_argument('--save_dir', default='data', help='Directory to save fitbit data.')
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

    client = FitbitClient(settings, ephemeral, os.path.abspath(args.save_dir))

if __name__ == "__main__":
    sys.exit(main())
