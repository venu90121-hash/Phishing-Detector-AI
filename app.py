from flask import Flask, render_template, request
import pickle
import os
import pandas as pd

app = Flask(__name__)

# --- STEP 1: LOAD THE MODEL GLOBALLY ---
MODEL_PATH = 'phishing_model.pkl'

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    model = None

# --- STEP 2: FEATURE EXTRACTION LOGIC ---
def get_features(url):
    url = str(url).lower()
    return [
        len(url),                # 1. Length
        url.count('.'),          # 2. Dots
        url.count('-'),          # 3. Hyphens
        1 if "@" in url else 0,  # 4. @ Symbol
        1 if "https" in url else 0 # 5. HTTPS check
    ]

# --- STEP 3: MAIN ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = ""
    
    if request.method == 'POST':
        url = request.form.get('url', '').lower()
        
        if not url:
            return render_template('index.html', prediction_text="Please enter a URL")

        # Hybrid Detection Logic
        # Check for manual red flags first
        is_suspicious = (len(url) > 50 or url.count('.') > 3 or "@" in url)
        
        # Check AI model prediction
        if model:
            features = get_features(url)
            prediction = model.predict([features])[0]
        else:
            prediction = 0 # Default if model is missing

        # Final decision: If manual flags OR AI says Phishing (1 or -1)
        if is_suspicious or prediction == 1 or prediction == -1:
            prediction_text = "🔴 WARNING: PHISHING DETECTED!"
        else:
            prediction_text = "🟢 SAFE: PROCEED WITH ACCESS"
            
    return render_template('index.html', prediction_text=prediction_text)

# --- STEP 4: DEPLOYMENT PORT LOGIC ---
# This part tells Render which port to use
if __name__ == "__main__":
    # Use the port assigned by Render, or 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' allows the app to be accessible externally
    app.run(host='0.0.0.0', port=port)