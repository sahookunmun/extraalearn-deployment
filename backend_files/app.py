import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
learn_api = Flask("ExtraaLearn")

# Load the trained model pipeline safely
try:
    model = joblib.load("learn_model.joblib")
    print("Model pipeline loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Home endpoint
@learn_api.get('/')
def home():
    return "Welcome to the ExtraaLearn Lead Prediction Backend API"

# Prediction endpoint matching target schema
@learn_api.post('/v1/predict')
def predict_sales():
    if not model:
        return jsonify({'error': 'Model pipeline not loaded.'}), 500
        
    try:
        data = request.get_json(force=True)
        
        # Map incoming JSON attributes into the model feature structure
        sample = {
            'age': int(data['age']),
            'current_occupation': str(data['current_occupation']),
            'first_interaction': str(data['first_interaction']),
            'profile_completed': str(data['profile_completed']),
            'website_visits': int(data['website_visits']),
            'time_spent_on_website': int(data['time_spent_on_website']),
            'page_views_per_visit': float(data['page_views_per_visit']),
            'last_activity': str(data['last_activity']),
            'print_media_type1': str(data['print_media_type1']),
            'print_media_type2': str(data['print_media_type2']),
            'digital_media': str(data['digital_media']),
            'educational_channels': str(data['educational_channels']),
            'referral': str(data['referral'])
        }

        # Convert raw record to DataFrame
        input_data = pd.DataFrame([sample])

        # Generate prediction using our serialized pipeline
        prediction = int(model.predict(input_data)[0])

        return jsonify({'Lead': prediction})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run Flask application on port 5000
    learn_api.run(host='0.0.0.0', port=5000, debug=True)
