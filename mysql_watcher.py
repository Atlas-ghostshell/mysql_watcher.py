mysql_watcher.py

import re import time import subprocess from pathlib import Path

=== CONFIGURATION ===

MYSQL_LOG_PATH = "/var/log/mysql/mysql.log"  # Adjust path if different ALERT_EMAIL_TO = "muriukigeoffrey472@gmail.com" ALERT_EMAIL_FROM = "muriukigeoffrey472@gmail.com" MSMTP_CONFIG_PATH = "/etc/msmtprc"  # Ensure this path is correct and accessible ALERT_LOG = "/var/log/mysql-alerts.log"

=== FUNCTION TO SEND EMAIL USING MSMTP ===

def send_email_alert(user, timestamp, query): subject = f"[ALERT] DVWA login attempt by '{user}'" body = f""" [ALERT] DVWA login attempt detected!

Timestamp: {timestamp}
User: {user}
Query: {query.strip()}
"""

message = f"Subject: {subject}\nFrom: {ALERT_EMAIL_FROM}\nTo: {ALERT_EMAIL_TO}\n\n{body}"

try:
    subprocess.run(['msmtp', '-C', MSMTP_CONFIG_PATH, ALERT_EMAIL_TO], input=message, text=True, check=True)
    print(f"[+] Email alert sent to {ALERT_EMAIL_TO}")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Could not send email: {e}")

=== FUNCTION TO LOG ALERT LOCALLY ===

def log_alert(user, timestamp, query): with open(ALERT_LOG, 'a') as f: f.write(f"[ALERT] {timestamp} - DVWA login attempt by '{user}'\n") f.write(f"Query: {query.strip()}\n\n")

=== MAIN FUNCTION TO MONITOR MYSQL LOG ===

def monitor_mysql_log(): print("[+] Starting MySQL alert watcher...")

if not Path(MYSQL_LOG_PATH).exists():
    print(f"[ERROR] MySQL log file not found at {MYSQL_LOG_PATH}")
    return

with open(MYSQL_LOG_PATH, 'r') as log:
    log.seek(0, 2)  # Go to end of file

    while True:
        line = log.readline()
        if not line:
            time.sleep(0.5)
            continue

        if re.search(r"SELECT \* FROM users WHERE user='(.*?)'", line):
            match = re.search(r"user='(.*?)'", line)
            user = match.group(1) if match else "unknown"
            timestamp_match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", line)
            timestamp = timestamp_match.group(1) if timestamp_match else time.strftime("%Y-%m-%d %H:%M:%S")

            print("\n[ALERT] DVWA login attempt detected!")
            print(f"User: {user}")
            print(f"Timestamp: {timestamp}")
            print(f"Query: {line.strip()}\n")

            log_alert(user, timestamp, line)
            send_email_alert(user, timestamp, line)

if name == 'main': monitor_mysql_log()