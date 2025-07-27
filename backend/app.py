from flask import Flask, jsonify, render_template
import joblib
import numpy as np
import datetime
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

model = joblib.load('C:/Users/user/Downloads/raseen_Project/model/drone_bird_model.pk1')
print("Has predict_proba:", hasattr(model, "predict_proba"))

df = pd.read_csv('C:/Users/user/Downloads/raseen_Project/backend/test.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_random', methods=['GET'])
def predict_random():
    row = df.sample(n=1).iloc[0]
    
    energy = float(row['energy'])
    size_score = float(row['size_score'])
    flap_rate = float(row['flap_rate'])
    altitude = float(row['altitude'])
    speed = float(row['speed'])
    
    location = row.get('location', 'unknown')
    timestamp = row.get('timestamp', str(datetime.datetime.now()))

    X_input = pd.DataFrame([{
    'energy': energy,
    'size_score': size_score,
    'flap_rate': flap_rate,
    'altitude': altitude,
    'speed': speed
    }])
    
    prediction = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)[0][prediction]

    result = {
        'prediction': 'drone' if prediction == 1 else 'bird',
        'confidence': f"{proba * 100:.1f}%",
        'features': {
            'energy': energy,
            'size_score': size_score,
            'flap_rate': flap_rate,
            'altitude': altitude,
            'speed': speed
        },
        'location': location,
        'timestamp': timestamp
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
