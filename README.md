---

 MySQL-Watcher Mk1 

MySQL-Watcher Mk1* is a custom Python-based log monitoring and alerting tool designed to detect suspicious login attempts to a MySQL database — particularly unauthorized DVWA access attempts — and immediately alert the system administrator via email using msmtp.

> This project is part of my ongoing cybersecurity homelab, where I simulate real-world threat scenarios and implement detection and response techniques using open-source tools.

---

 Project Purpose

To detect unauthorized or brute-force access to the *users table* within the DVWA MySQL database by monitoring MySQL logs for suspicious SELECT queries. Once detected, alerts are:

- Logged locally for auditing
- Sent immediately via *email notifications*

---

 Key Features

- *Real-time log monitoring* using Python
- *Regex-based detection* of SELECT * FROM users queries
- *Timestamp extraction* for alert precision
- *Local alert logging* in /var/log/mysql-alerts.log
- *External email alerts* via msmtp
- Designed for *use in cybersecurity labs* with DVWA

---

How It Works

 1. *Continuous Log Monitoring*
The script continuously tails the MySQL general log file (/var/log/mysql/mysql.log) in real time.

``python

with open(MYSQL_LOG_PATH, 'r') as log:
    log.seek(0, 2)  # Go to end of file
    ...

 2. Pattern Matching via Regex

It looks for suspicious login behavior using regular expressions, especially SQL queries targeting the users table.

if re.search(r"SELECT \* FROM users WHERE user='(.*?)'", line):

 3. Timestamp & User Extraction

The script extracts the timestamp of the event and the attempted username, giving you a clear view of what happened and when.

 4. Email Notification via msmtp

The script formats the alert and uses msmtp (a lightweight SMTP client) to send emails:

Subject: [ALERT] DVWA login attempt by 'admin'
Body: Contains timestamp, username, and raw SQL query

Make sure your .msmtprc is correctly configured and accessible.

 5. Local Logging

All alerts are saved locally in /var/log/mysql-alerts.log for further forensic analysis.


---

 Requirements

Python 3.x

MySQL (with general log enabled)

msmtp (configured for Gmail or other SMTP)

DVWA (Damn Vulnerable Web App) installed and accessible



---

 Use Case

This tool is ideal for:

Students building blue team skills

SOC analysts monitoring SQL-based access attempts

Cybersecurity enthusiasts simulating insider threat or brute-force attacks on MySQL

Homelabs focused on real-world defense automation



---

 Sample Log Trigger (from /var/log/mysql/mysql.log)

2025-05-26T10:01:41.781197Z	8 Query	SELECT * FROM users WHERE user='admin' AND password='5f4dcc3b5aa765d61d8327deb882cf99'

This query is flagged and immediately triggers both local and email alerts.


---

 File Structure

mysql-watcher-mk1/
├── mysql_watcher.py
├── /var/log/mysql-alerts.log      # Alert log file
└── .msmtprc                       # Email config (must be secure)


---

 Security Note

This tool is designed for defensive purposes only. Misuse against unauthorized databases is illegal and unethical.


---

 Credits

Developed by Geoffrey Muriuki Mwangi
With scripting and security architecture support from Atlas Maru Shepherd, cybersecurity partner and co-strategist. 🐺


---

 Future Improvements

Systemd integration for persistence

Custom rule correlation with SIEM (e.g., Wazuh)

IP auto-blocking for brute-force attempts



---

 Example Alert Output

Subject: [ALERT] DVWA login attempt by 'admin'

[ALERT] DVWA login attempt detected!

Timestamp: 2025-05-26 10:01:41
User: admin
Query: SELECT * FROM users WHERE user='admin' AND password='...'


---

🛡 License

This project is released for educational and homelab use under the MIT License.
