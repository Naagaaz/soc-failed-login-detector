import subprocess
import re

failed_attempts = {}

# Run journalctl command
command = ["journalctl", "-u", "ssh", "--no-pager"]

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for line in process.stdout:
    if "Failed password" in line:
        ip_match = re.search(r"from ([0-9.]+)", line)
        if ip_match:
            ip = ip_match.group(1)
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

print("=== Failed Login Attempts ===")

if not failed_attempts:
    print("No failed SSH login attempts found.")
else:
    for ip, count in failed_attempts.items():
        if count >= 3:
            print(f"ALERT: {count} failed login attempts from {ip}")
        else:
            print(f"{count} failed login attempts from {ip}")

