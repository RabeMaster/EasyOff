from datetime import datetime

from PySide6.QtCore import QDateTime


class TimeUtils:
    @staticmethod
    def get_seconds_difference(target_qdatetime: QDateTime) -> int:
        target_datetime = target_qdatetime.toPython()
        now = datetime.now()
        difference = target_datetime - now
        return int(difference.total_seconds())

    @staticmethod
    def format_timedelta(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f"{hours}시간 {minutes}분"
        return f"{minutes}분"
