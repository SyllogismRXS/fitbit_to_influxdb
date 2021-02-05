import sys
import os
import argparse

from fitbit_to_influxdb.write_to_influxdb import write_to_influxdb
from fitbit_to_influxdb.utils import is_valid_date_string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--save_dir', default='data', help='Directory that contains profile.json and saved data.')
    parser.add_argument('-d', '--date', default=None, help='The saved date to write to influxdb (format: 2020-05-25)')
    args = parser.parse_args()

    save_dir = os.path.abspath(args.save_dir)
    profile_path = os.path.join(save_dir, 'profile.json')

    if not os.path.exists(profile_path):
        raise Exception('The profile.json file does not exist at %s. Make sure you have already downloaded the Fitbit data.' % profile_path)

    if args.date is not None:
        # use the specified date
        date_dir = os.path.join(save_dir, args.date)
        if not os.path.exists(date_dir):
            raise Exception('The date directory does not exist: %s' % date_dir)
        dirs = [{'date': args.date,
                 'path': date_dir}]
    else:
        dirs = [{'date': dir,
                 'path': os.path.join(save_dir, dir)}
                for dir in os.listdir(save_dir)
                if is_valid_date_string(dir)]

    write_to_influxdb(profile_path, dirs)


if __name__ == "__main__":
    sys.exit(main())
