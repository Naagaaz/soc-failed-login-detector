import subprocess
import re
from datetime import datetime, timedelta

FAILED_THRESHOLD = 5
TIME_WINDOW = timedelta(minutes=2)

attempts = {}

command = ["journalctl", "-u", "ssh", "--no-pager"]

process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

for line in process.stdout:
    if "Failed password" in line:
        time_match = re.match(r"^(\w+\s+\d+\s+\d+:\d+:\d+)", line)
        ip_match = re.search(r"from ([0-9.]+)", line)

        if time_match and ip_match:
            time_str = time_match.group(1)
            ip = ip_match.group(1)

            log_time = datetime.strptime(time_str, "%b %d %H:%M:%S")
            attempts.setdefault(ip, []).append(log_time)

print("=== Brute Force Detection Alerts ===")

alert_found = False

for ip, times in attempts.items():
    times.sort()
    for i in range(len(times)):
        window = [t for t in times if t >= times[i] and t <= times[i] + TIME_WINDOW]
        if len(window) >= FAILED_THRESHOLD:
            print(f"ALERT: Possible brute-force from {ip} ({len(window)} attempts in 2 minutes)")
            alert_found = True
            break

if not alert_found:
    print("No brute-force activity detected.")
