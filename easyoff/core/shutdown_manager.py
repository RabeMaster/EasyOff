import re
import subprocess


class ShutdownManager:
    @staticmethod
    def is_scheduled():
        try:
            query = "*[System[(Provider[@Name='User32'] and (EventID=1074 or EventID=1075)) or (Provider[@Name='EventLog'] and EventID=6005) or (Provider[@Name='Microsoft-Windows-Kernel-General'] and EventID=12)]]"
            cmd = ["wevtutil", "qe", "System", f"/q:{query}", "/c:1", "/rd:true", "/f:xml"]

            result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            match = re.search(r"<EventID(?:[^>]*)>(\d+)</EventID>", result.stdout)

            if match and match.group(1) == "1074":
                return True

            return False

        except Exception:
            return False

    @staticmethod
    def cancel():
        try:
            subprocess.run(["shutdown", "-a"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except Exception:
            return False

    @staticmethod
    def schedule(seconds: int, reboot: bool = False, force: bool = False):
        command = ["shutdown"]

        if reboot:
            command.append("-r")
        else:
            command.append("-s")

        if force:
            command.append("-f")

        command.extend(["-t", str(seconds)])

        try:
            result = subprocess.run(command, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return "SUCCESS"
            elif result.returncode == 1190:
                return "ALREADY_SCHEDULED"
            else:
                return "ERROR"

        except Exception:
            return "ERROR"
