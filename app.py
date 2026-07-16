import os
import requests  # Telegram API call karne ke liye
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.secret_key = "super_secret_key_zindagi_bhar"

# --- TELEGRAM CONFIGURATION (UPDATED WITH YOUR DETAILS) ---
TELEGRAM_BOT_TOKEN = "8903839809:AAGFAtDI4HVNwxd4IzCH4WAhY12FY73BvA0"
TELEGRAM_CHAT_ID = "8036623116"

# Cloudinary Config
cloudinary.config( 
  cloud_name = "dpajpnhq8", 
  api_key = "787696411895168", 
  api_secret = "jwu8KaVGhPajsSch7hwFvqLAh4A",
  secure = True
)

USER_USERNAME = "admin"  
USER_PASSWORD = "password123"  
uploaded_files_db = []

# Telegram par message bhejne ka function
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram message send karne me error: {str(e)}")

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USER_USERNAME and password == USER_PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return "Galat Username ya Password! Wapas try karein."
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/login')
        
    # Real IP detect karna
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()
        
    # Telegram par notification bhejna (User ko pata bhi nahi chalega)
    telegram_msg = f"🔔 *Naya Login Detect Hua!*\n🌐 *IP Address:* `{user_ip}`"
    send_telegram_message(telegram_msg)
    
    # Simple dashboard render karna bina kisi IP box ke
    return render_template('dashboard.html', files=uploaded_files_db)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logged_in' not in session:
        return redirect('/login')
    if 'file' not in request.files:
        return "Koi file select nahi ki!"
    file = request.files['file']
    if file.filename == '':
        return "File ka naam khali hai!"
    if file:
        try:
            upload_result = cloudinary.uploader.upload(file, resource_type="auto")
            file_url = upload_result.get('secure_url')
            file_type = upload_result.get('resource_type') 
            uploaded_files_db.append({'url': file_url, 'type': file_type})
            return redirect('/dashboard')
        except Exception as e:
            return f"Upload me error aaya: {str(e)}"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



