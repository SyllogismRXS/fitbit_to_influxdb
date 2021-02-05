from datetime import datetime, timedelta
from pytz import timezone

def get_date_string(t):
    return t.strftime('%Y-%m-%d')

def get_date_from_string(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

def is_valid_date_string(date_string):
    try:
        get_date_from_string(date_string)
    except:
        return False
    return True

def get_date_from_string_with_zone(time_zone_string, date_string):
    # Get the tzinfo object from the time zone string
    time_zone_info = timezone(time_zone_string)

    # Parse the date into a datetime object
    date_object = get_date_from_string(date_string)

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
    date = get_date_from_string_with_zone(time_zone_string, date_string)
    return date + get_timedelta_from_string(time_string)

def get_unix_time_seconds(date, time_24):
    return int(round((date + get_timedelta_from_string(time_24)).timestamp()))

def make_influx_safe(my_str):
    return my_str.replace(' ', '\ ')
