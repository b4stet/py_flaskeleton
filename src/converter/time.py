from datetime import datetime, timedelta, timezone


class TimeConverter():
    FORMAT = '%Y-%m-%d %H:%M:%S UTC'

    def __init__(self):
        pass

    def to_datetime(self, date_str):
        try:
            time = datetime.strptime(date_str, self.FORMAT)
            time = time.astimezone(timezone.utc)

        except Exception:
            raise ValueError('Expected a date format {}, got {}'.format(self.FORMAT, date_str))

        return time

    def to_str(self, date_dt: datetime):
        return date_dt.strftime(self.FORMAT)
