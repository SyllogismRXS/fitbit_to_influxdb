import os
import fitbit
from pathlib import Path
from datetime import datetime
import json

from fitbit_to_influxdb.utils import get_date_string

class FitbitClient:
    def __init__(self, settings, ephemeral, save_dir):
        self._authd_client = fitbit.Fitbit(
            settings['client_id'],
            settings['client_secret'],
            access_token=ephemeral['access_token'],
            refresh_token=ephemeral['refresh_token'],
            expires_at=ephemeral['expires_at'])

        self._profile = self._authd_client.user_profile_get()
        self._user = self._profile['user']['fullName']
        self._time_zone = self._profile['user']['timezone']

        date = datetime.today()

        # Make the save_dir if it doesn't exist
        output_dir = os.path.join(save_dir, get_date_string(date))
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for item in settings['intraday_time_series']:
            self.save_intraday_time_series(item['name'], date, item['detail_level'], output_dir)


    def save_intraday_time_series(self, name, date, detail_level, output_dir):
        data = self._authd_client.intraday_time_series(name, date, detail_level=detail_level)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(output_dir, name.replace('/','-') + '.json'), 'w') as fp:
            json.dump(data, fp)
