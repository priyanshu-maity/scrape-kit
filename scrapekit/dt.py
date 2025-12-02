from datetime import datetime
from tzlocal import get_localzone


def convert_utc_to_local(utc_time: datetime) -> datetime:
    """
    Converts a UTC datetime object to the user's local timezone.

    Args:
        utc_time (datetime): The UTC datetime object to be converted.

    Returns:
        datetime: The converted datetime object in the user's local timezone.
    """
    local_timezone = get_localzone()
    local_time = utc_time.astimezone(local_timezone)
    return local_time