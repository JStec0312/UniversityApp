from __future__ import annotations
from datetime import timedelta, datetime, timezone
from zoneinfo import ZoneInfo
from typing import Protocol

WARSAW = ZoneInfo("Europe/Warsaw")
UTC = timezone.utc

def _truncate_to_minute(dt: datetime) -> datetime:
    """
    Truncate a datetime to minute precision (remove seconds and microseconds).
    
    Args:
        dt (datetime): A datetime object.
        
    Returns:
        datetime: Datetime with seconds and microseconds set to 0.
    """
    return dt.replace(second=0, microsecond=0)


class Clock(Protocol):
    @staticmethod
    def now() -> datetime:
        return  _truncate_to_minute(datetime.now(WARSAW))

    @staticmethod
    def is_before(dt1:datetime, dt2:datetime) -> bool:
        """
        Check if dt1 is before dt2.
        
        Args:
            dt1 (datetime): First datetime object.
            dt2 (datetime): Second datetime object.
            
        Returns:
            bool: True if dt1 is before dt2, False otherwise.
        """
        return dt1 < dt2
    @staticmethod
    def is_after( dt1:datetime, dt2:datetime) -> bool:
        """
        Check if dt1 is after dt2.
        
        Args:
            dt1 (datetime): First datetime object.
            dt2 (datetime): Second datetime object.
            
        Returns:
            bool: True if dt1 is after dt2, False otherwise.
        """
        return dt1 > dt2
    @staticmethod
    def diff_minutes(dt1:datetime, dt2:datetime) -> int:
        """
        Calculate the difference in minutes between two datetimes.
        
        Args:
            dt1 (datetime): First datetime object.
            dt2 (datetime): Second datetime object.
            
        Returns:
            int: Difference in minutes.
        """
        delta = dt2 - dt1
        return int(delta.total_seconds() // 60)
    
    @staticmethod
    def to_pl(dt: datetime) -> datetime:
        """
        Convert a UTC datetime to Warsaw local time (Poland).

        Args:
            dt (datetime): A UTC datetime object.

        Returns:
            datetime: A datetime object in Warsaw local time.
        """
        return dt.astimezone(WARSAW)