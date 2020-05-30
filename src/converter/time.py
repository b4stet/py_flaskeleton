from datetime import datetime, timedelta, timezone


class TimeConverter():
    __format = '%Y-%m-%d %H:%M:%S UTC'

    def __init__(self):
        pass

    def to_datetime(self, date_str):
        try:
            time = datetime.strptime(date_str, self.__format)
            time = time.astimezone(timezone.utc)

        except Exception:
            raise ValueError('Expected a date format {}, got {}'.format(self.__format, date_str))

        return time

    def to_str(self, date_dt):
        return date_dt.strftime(self.__format)
