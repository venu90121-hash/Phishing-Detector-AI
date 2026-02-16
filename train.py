import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# --- STEP 1: LOAD DATA ---
df = pd.read_csv('dataset_phishtank.csv') 

# --- STEP 2: AUTO-DETECT COLUMNS ---
# Find the URL column (looks for 'url' or 'url_link')
url_col = [col for col in df.columns if 'url' in col.lower()][0]

# Find the Result column (looks for 'label', 'Result', or just uses the last column)
if 'label' in df.columns:
    target_col = 'label'
elif 'Result' in df.columns:
    target_col = 'Result'
else:
    # If it can't find 'label', it takes the very last column in your CSV
    target_col = df.columns[-1]

print(f"Using '{url_col}' for URLs and '{target_col}' for Labels.")

# --- STEP 3: FEATURE EXTRACTION ---
def get_features(url):
    url = str(url)
    return [
        len(url), 
        url.count('.'), 
        url.count('-'), 
        1 if "@" in url else 0, 
        1 if "https" in url else 0
    ]

X = [get_features(u) for u in df[url_col]]
y = df[target_col]

# --- STEP 4: TRAIN AND SAVE ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

with open('phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("SUCCESS: 'phishing_model.pkl' created! Now you can run app.py.")