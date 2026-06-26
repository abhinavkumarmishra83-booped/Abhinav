import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.secret_key = "super_secret_key_zindagi_bhar"  # Session secure rakhne ke liye

# --- CLOUDINARY CONFIGURATION (UPDATED) ---
cloudinary.config( 
  cloud_name = "dpajpnhq8", 
  api_key = "787696411895168", 
  api_secret = "jwu8KaVGhPajsSch7hwFvqLAh4A",
  secure = True
)

# --- APNA USERNAME AUR PASSWORD SET KAREIN ---
USER_USERNAME = "admin"  # Aap apna manpasand username yahan rakh sakte hain
USER_PASSWORD = "password123"  # Aap apna manpasand password yahan rakh sakte hain

# Ek khali list uploaded files ke links ko yaad rakhne ke liye
uploaded_files_db = []

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
            # Yeh line file ko direct Cloudinary par upload kar degi
            upload_result = cloudinary.uploader.upload(file, resource_type="auto")
            
            # Cloudinary se jo permanent link milega, use hum save kar lenge
            file_url = upload_result.get('secure_url')
            file_type = upload_result.get('resource_type') # image ya video
            
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

