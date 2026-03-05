from PySide6.QtCore import QDate, QDateTime, QTime, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from easyoff.core.shutdown_manager import ShutdownManager
from easyoff.utils.time_utils import TimeUtils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyOff")
        self.setFixedSize(250, 200)

        self._init_ui()
        QTimer.singleShot(0, self.check_initial_state)

    def _init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.layout.addWidget(QLabel("예약 날짜:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.layout.addWidget(self.date_edit)

        self.layout.addWidget(QLabel("예약 시간 (시 / 분):"))
        self.time_layout = QHBoxLayout()
        self.hour_combo = QComboBox()
        self.hour_combo.addItems([f"{i:02d}" for i in range(24)])
        self.minute_combo = QComboBox()
        self.minute_combo.addItems([f"{i:02d}" for i in range(60)])

        current_time = QTime.currentTime()
        self.hour_combo.setCurrentText(f"{current_time.hour():02d}")
        self.minute_combo.setCurrentText(f"{current_time.minute():02d}")

        self.time_layout.addWidget(self.hour_combo)
        self.time_layout.addWidget(QLabel("시"))
        self.time_layout.addWidget(self.minute_combo)
        self.time_layout.addWidget(QLabel("분"))
        self.layout.addLayout(self.time_layout)

        self.option_layout = QHBoxLayout()
        self.force_checkbox = QCheckBox("강제 종료")
        self.reboot_checkbox = QCheckBox("재부팅")
        self.option_layout.addWidget(self.force_checkbox)
        self.option_layout.addWidget(self.reboot_checkbox)
        self.layout.addLayout(self.option_layout)

        self.button_layout = QHBoxLayout()
        self.schedule_button = QPushButton("예약")
        self.cancel_button = QPushButton("예약 취소")
        self.button_layout.addWidget(self.schedule_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.schedule_button.clicked.connect(self.on_schedule_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

    def _ask_yes_no(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes

    def _get_target_datetime(self) -> QDateTime:
        selected_date = self.date_edit.date()
        selected_hour = int(self.hour_combo.currentText())
        selected_minute = int(self.minute_combo.currentText())
        selected_time = QTime(selected_hour, selected_minute)
        return QDateTime(selected_date, selected_time)

    def check_initial_state(self):
        if not ShutdownManager.is_scheduled():
            return

        msg = "이미 종료 예약이 존재합니다.\n예약을 취소하고 새로 설정하시겠습니까?"
        if self._ask_yes_no("확인", msg):
            ShutdownManager.cancel()
        else:
            QApplication.instance().quit()

    def on_schedule_clicked(self):
        target_qdt = self._get_target_datetime()
        current_qdt = QDateTime.currentDateTime()

        if target_qdt <= current_qdt:
            QMessageBox.warning(self, "경고", "선택한 시간이 현재 시간보다 이전입니다.\n미래 시간을 선택해주세요.")
            return

        seconds = TimeUtils.get_seconds_difference(target_qdt)
        time_str = target_qdt.toString("yyyy-MM-dd HH:mm")
        remaining_str = TimeUtils.format_timedelta(seconds)

        msg = f"예약 시간: {time_str}\n남은 시간: {remaining_str}\n\n종료를 예약하시겠습니까?"
        if not self._ask_yes_no("예약 확인", msg):
            return

        self._process_scheduling(seconds)

    def _process_scheduling(self, seconds: int):
        reboot = self.reboot_checkbox.isChecked()
        force = self.force_checkbox.isChecked()

        status = ShutdownManager.schedule(seconds, reboot, force)

        if status == "SUCCESS":
            QMessageBox.information(self, "성공", "예약이 완료되었습니다.")
            return

        if status == "ALREADY_SCHEDULED":
            msg = "외부에서 설정된 다른 종료 예약이 존재합니다.\n기존 예약을 취소하고 새로 설정하시겠습니까?"
            if self._ask_yes_no("예약 충돌", msg):
                ShutdownManager.cancel()
                if ShutdownManager.schedule(seconds, reboot, force) == "SUCCESS":
                    QMessageBox.information(self, "성공", "기존 예약을 취소하고 새로 예약이 완료되었습니다.")
                else:
                    QMessageBox.critical(self, "오류", "새 예약 설정 중 문제가 발생했습니다.")
            return

        QMessageBox.critical(self, "오류", "예약 설정 중 알 수 없는 문제가 발생했습니다.")

    def on_cancel_clicked(self):
        ShutdownManager.cancel()
        QMessageBox.information(self, "알림", "예약이 취소되었습니다.")
