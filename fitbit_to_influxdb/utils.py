from datetime import datetime, timedelta
import pytz as tz

def get_date_string(t):
    return t.strftime('%Y-%m-%d')

def get_date_from_string(time_zone_string, date_string):
    # Get the tzinfo object from the time zone string
    time_zone_info = tz.gettz(time_zone_string)

    # Parse the date into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    # Make the datetime object time zone aware
    time_object_aware = date_object.replace(tzinfo=time_zone_info)

    return time_object_aware

def get_timedelta_from_string(time_string):
    # Parse the time string into a datetime object
    time_object = datetime.strptime(time_string, '%H:%M:%S')

    return timedelta(hours=time_object.hour,
                     minutes=time_object.minute,
                     seconds=time_object.second)

def get_datetime_from_string(time_zone_string, date_string, time_string):
    date = get_date_from_string(time_zone_string, date_string)
    return date + get_timedelta_from_string(time_string)

def get_unix_time_seconds(date, time_24):
    return int(round((date + get_timedelta_from_string(time_24)).timestamp()))

def make_influx_safe(my_str):
    return my_str.replace(' ', '\ ')
