# Nexora Automations | Client Onboarding Portal

A full-stack, automated lead generation and client onboarding portal built for service-based businesses. 

## 🚀 Live Demo
[View the Live Portal Here](http://NovaAutomation.pythonanywhere.com)

## ⚙️ Core Features
* **Modern UI:** Responsive, high-conversion frontend styled with a custom Coastal Retreat aesthetic.
* **Database Management:** Secure SQLite database integration to capture and store lead data.
* **Automated Notifications:** Real-time Discord webhook integration for instant team alerts on new leads.
* **Email Routing:** Automated SMTP integration to instantly send customized HTML welcome emails to new clients.
* **Secure Admin Dashboard:** Password-protected backend portal to view, manage, and track incoming leads with automated timestamping.

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Database:** SQLite3
* **Integrations:** Discord API, SMTP Email Server

## 💻 Local Installation
1. Clone the repository.
2. Install Flask: `pip install flask`
3. Update the `DISCORD_WEBHOOK_URL`, `EMAIL_ADDRESS`, and `EMAIL_PASSWORD` variables in `app.py` with your credentials.
4. Run the application: `python app.py`
