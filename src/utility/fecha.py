from datetime import datetime
from zoneinfo import ZoneInfo


def get_today():
    argentina = ZoneInfo("America/Argentina/Buenos_Aires")
    return datetime.now(argentina).date()
