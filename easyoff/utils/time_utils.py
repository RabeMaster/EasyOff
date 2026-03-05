from PySide6.QtCore import QDateTime


class TimeUtils:
    @staticmethod
    def get_seconds_difference(target_qdatetime: QDateTime) -> int:
        return QDateTime.currentDateTime().secsTo(target_qdatetime)

    @staticmethod
    def format_timedelta(seconds: int) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60

        if hours > 0:
            return f"{hours}시간 {minutes}분"

        return f"{minutes}분"
