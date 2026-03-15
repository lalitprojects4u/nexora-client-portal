from flask import Flask, request, jsonify, render_template_string
import sqlite3
import requests
import smtplib
import os  # <-- We added this to find the exact file path
from email.message import EmailMessage

app = Flask(__name__)

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'YOUR_APP_PASSWORD'
ADMIN_PASSKEY = 'CHANGE_THIS_PASSKEY'
# --- ABSOLUTE PATH SETUP ---
# This gives the server the exact GPS coordinates to save the database right next to this file
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(THIS_FOLDER, 'nexora_master.db')

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- AUTOMATION FUNCTIONS ---
def send_discord_notification(name, email, service):
    if DISCORD_WEBHOOK_URL == 'YOUR_DISCORD_WEBHOOK_URL_HERE':
        print("Skipping Discord: Webhook URL not configured.")
        return

    data = {
        "content": f"🚨 **New Lead Alert!**\n**Name:** {name}\n**Email:** {email}\n**Interest:** {service}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def send_welcome_email(name, to_email):
    if EMAIL_ADDRESS == 'your_email@gmail.com':
        print("Skipping Email: Credentials not configured.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Welcome to Nexora Automations'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    # 1. Plain text fallback (Crucial to prevent going to the Spam folder!)
    msg.set_content(f"Hi {name},\n\nThank you for reaching out to Nexora Automations! We have received your inquiry and will get back to you shortly.\n\nBest,\nThe Nexora Team")

    # 2. The Premium HTML Coastal Retreat Version
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #DBE2DC; margin: 0; padding: 40px 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" max-width="600" style="background-color: #FFFFFF; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(51, 87, 101, 0.1); max-width: 600px; margin: auto;">
            <tr>
                <td style="background-color: #335765; padding: 40px; text-align: center;">
                    <h1 style="color: #FFFFFF; margin: 0; font-size: 32px; letter-spacing: 2px; text-transform: uppercase;">Nexora</h1>
                    <p style="color: #B6D9E0; margin: 5px 0 0 0; font-size: 14px; letter-spacing: 4px; text-transform: uppercase;">Automations</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 40px; color: #335765; line-height: 1.6;">
                    <h2 style="margin-top: 0; color: #335765;">Hello {name},</h2>
                    <p>Thank you for reaching out to us. We have successfully received your request for automation services.</p>
                    <p>Our engineering team is currently reviewing your details. One of our specialists will be in touch with you within the next 24 hours to discuss exactly how we can streamline your business workflows.</p>

                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 35px 0;">
                        <tr>
                            <td align="center">
                                <a href="https://calendly.com/nexoraautomations/30min" target="_blank" style="background-color: #74A8A4; color: #FFFFFF; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; display: inline-block; text-transform: uppercase; letter-spacing: 1px;">Book Your Strategy Call</a>
                            </td>
                        </tr>
                    </table>

                    <p style="margin-bottom: 0;">Best regards,<br><strong style="color: #74A8A4;">The Nexora Engineering Team</strong></p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #f8f9fa; padding: 20px; text-align: center; color: #74A8A4; font-size: 12px; letter-spacing: 1px;">
                    &copy; 2026 Nexora Automations. All rights reserved.
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # 3. Attach the HTML to the email
    msg.add_alternative(html_content, subtype='html')

    # 4. Send it through Google's servers
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- ROUTES ---

# 1. THE FRONTEND FORM
@app.route('/')
def home():
    html_form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nexora Automations | Client Portal</title>
        <style>
            :root {
                /* Exact Coastal Retreat Palette */
                --page-bg: #335765; /* Deep Slate Blue */
                --surface: #FFFFFF; /* Clean White Card */

                --brand-primary: #74A8A4; /* Muted Teal */
                --brand-hover: #335765; /* Hover shifts back to Deep Slate */
                --text-main: #335765; /* Deep Slate for readable text */
                --text-muted: #74A8A4; /* Teal for subtitles */

                --border-light: rgba(51, 87, 101, 0.1);
                --border-input: #B6D9E0; /* Light Sky Blue for input borders */
                --input-bg: #DBE2DC; /* Pale Grey-Green for input backgrounds */
                --shadow-prime: 0 15px 35px rgba(20, 35, 42, 0.4);
            }

            body {
                font-family: 'Segoe UI', system-ui, sans-serif;
                margin: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: var(--page-bg);
                color: #ffffff;
            }

            .container {
                background: var(--surface);
                padding: 45px;
                border-radius: 12px;
                box-shadow: var(--shadow-prime);
                width: 100%;
                max-width: 440px;
                box-sizing: border-box;
                border: 1px solid var(--border-light);
            }

            .header { text-align: center; margin-bottom: 35px; }

            .logo {
                font-size: 36px;
                font-weight: 900;
                letter-spacing: -1.5px;
                /* Low-to-high Coastal gradient */
                background: linear-gradient(to right, #335765, #B6D9E0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0 0 5px 0;
                text-transform: uppercase;
            }

            .header p { margin: 0; color: var(--text-muted); font-size: 13px; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }

            .form-group { margin-bottom: 25px; }

            label {
                display: block;
                margin-bottom: 8px;
                font-size: 13px;
                font-weight: 700;
                color: var(--text-main);
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            input, select {
                width: 100%;
                padding: 16px 20px;
                background: var(--input-bg);
                border: 1px solid var(--border-input);
                border-radius: 8px;
                font-size: 15px;
                color: var(--text-main);
                box-sizing: border-box;
                transition: all 0.3s ease;
            }

            input::placeholder { color: #74A8A4; opacity: 0.7; }
            select option { background: #ffffff; color: var(--text-main); }

            input:focus, select:focus {
                outline: none;
                border-color: var(--text-main);
                background: #FFFFFF;
                box-shadow: 0 0 0 3px rgba(116, 168, 164, 0.2);
            }

            button {
                width: 100%;
                padding: 18px;
                background-color: var(--brand-primary);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 800;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 15px;
                box-shadow: 0 6px 15px rgba(116, 168, 164, 0.3);
                text-transform: uppercase;
                letter-spacing: 2px;
            }

            button:hover {
                background-color: var(--brand-hover);
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(51, 87, 101, 0.3);
            }

            button:active { transform: translateY(0); }

            #status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                background: var(--border-input);
                color: var(--text-main);
                font-size: 14px;
                font-weight: 700;
                text-align: center;
                display: none;
                border: 1px solid var(--brand-primary);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">Nexora</div>
                <p>Automations</p>
            </div>
            <form id="leadForm">
                <div class="form-group">
                    <label for="name">Client Full Name</label>
                    <input type="text" id="name" placeholder="Enter your full name" required>
                </div>
                <div class="form-group">
                    <label for="email">Business Email Address</label>
                    <input type="email" id="email" placeholder="client@company.com" required>
                </div>
                <div class="form-group">
                    <label for="service">Service Requested</label>
                    <select id="service" required>
                        <option value="" disabled selected>Select an automation service...</option>
                        <option value="Custom Workflow Bot">Custom Workflow Bot</option>
                        <option value="Data Entry Automation">Data Entry Automation</option>
                        <option value="API Integration">API Integration</option>
                        <option value="Full-Stack Web App">Full-Stack Web App</option>
                    </select>
                </div>
                <button type="submit" id="submitBtn">Initialize Automation</button>
            </form>
            <div id="status">✨ System integrated! We will contact you shortly.</div>
        </div>
        <script>
            document.getElementById('leadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const btn = document.getElementById('submitBtn');
                const originalText = btn.innerText;
                btn.innerText = 'Processing Request...';
                btn.disabled = true;
                btn.style.opacity = '0.7';

                const data = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    service: document.getElementById('service').value
                };

                try {
                    const response = await fetch('/api/new-lead', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });

                    if (response.ok) {
                        document.getElementById('status').style.display = 'block';
                        document.getElementById('leadForm').reset();
                        setTimeout(() => document.getElementById('status').style.display = 'none', 4000);
                    }
                } finally {
                    btn.innerText = originalText;
                    btn.disabled = false;
                    btn.style.opacity = '1';
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_form)

# 2. THE API ENDPOINT
@app.route('/api/new-lead', methods=['POST'])
def new_lead():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    service = data.get('service')

    if not all([name, email, service]):
        return jsonify({"error": "Missing data"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, email, service) VALUES (?, ?, ?)", (name, email, service))
    conn.commit()
    conn.close()

    send_discord_notification(name, email, service)
    send_welcome_email(name, email)

    return jsonify({"message": "Lead processed successfully!"}), 200

# 3. THE NEW ADMIN DASHBOARD
@app.route('/admin')
def admin_dashboard():
    provided_key = request.args.get('key')
    if provided_key != ADMIN_PASSKEY:
        return "<h1 style='color:red; text-align:center; margin-top:50px;'>⛔ Access Denied: Invalid Security Key</h1>", 403

    # Using the new DB_PATH!
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # We are now asking SQL for the 'timestamp' as the 5th item
    c.execute("SELECT id, name, email, service, timestamp FROM leads ORDER BY id DESC")
    leads = c.fetchall()
    conn.close()

    admin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Nexora Admin Dashboard</title>
        <style>
            :root {
                --page-bg: #DBE2DC;
                --surface: #FFFFFF;
                --text-main: #335765;
                --text-muted: #74A8A4;
                --border-light: #B6D9E0;
            }
            body { font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--page-bg); padding: 40px; color: var(--text-main); margin: 0; }
            .dashboard { max-width: 1100px; margin: auto; background: var(--surface); padding: 40px; border-radius: 16px; box-shadow: 0 15px 35px rgba(51, 87, 101, 0.1); border: 1px solid var(--border-light); }
            .header-flex { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border-light); padding-bottom: 20px; margin-bottom: 30px; }
            h2 { margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; color: var(--text-main); }
            .logo-text { background: linear-gradient(to right, #335765, #74A8A4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
            table { width: 100%; border-collapse: collapse; }
            th, td { text-align: left; padding: 16px; border-bottom: 1px solid var(--border-light); }
            th { background-color: var(--page-bg); font-weight: 700; color: var(--text-main); text-transform: uppercase; font-size: 13px; letter-spacing: 1px; }
            tr:hover { background-color: #f8faf9; }
            .badge { background: #B6D9E0; color: #335765; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
            .id-col { font-weight: bold; color: var(--text-muted); }
            .time-col { color: var(--text-muted); font-size: 13px; font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header-flex">
                <h2><span class="logo-text">Nexora</span> Master Database</h2>
                <div class="badge" style="background: #335765; color: #FFFFFF;">Admin Secured</div>
            </div>
            <table>
                <tr>
                    <th>Date & Time (UTC)</th>
                    <th>Lead ID</th>
                    <th>Client Name</th>
                    <th>Email Address</th>
                    <th>Service Requested</th>
                </tr>
                {% for lead in leads %}
                <tr>
                    <td class="time-col">{{ lead[4] }}</td>
                    <td class="id-col">#{{ lead[0] }}</td>
                    <td><strong>{{ lead[1] }}</strong></td>
                    <td>{{ lead[2] }}</td>
                    <td><span class="badge">{{ lead[3] }}</span></td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" style="text-align:center; padding: 40px; color: var(--text-muted); font-style: italic;">No leads captured yet. Your pipeline is waiting!</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(admin_html, leads=leads)

if __name__ == '__main__':
    app.run(debug=True)