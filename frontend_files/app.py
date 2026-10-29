import streamlit as st
import requests

st.set_page_config(page_title="ExtraaLearn Lead Conversion Predictor", layout="centered")

st.title("💼 ExtraaLearn Lead Predictor")
st.write("Enter the prospective student's details below to estimate their likelihood of enrollment conversion.")

# Input Forms
age = st.number_input("Age", min_value=18, max_value=90, value=35, step=1)
current_occupation = st.selectbox("Current Occupation", ["Professional", "Unemployed", "Student"])
first_interaction = st.selectbox("First Interaction", ["Website", "Mobile App"])
profile_completed = st.selectbox("Profile Completion Level", ["High", "Medium", "Low"])
website_visits = st.number_input("Website Visits", min_value=0, max_value=100, value=3, step=1)
time_spent_on_website = st.number_input("Time Spent on Website (seconds)", min_value=0, max_value=10000, value=500, step=10)
page_views_per_visit = st.number_input("Page Views per Visit", min_value=0.0, max_value=50.0, value=2.5, step=0.5)
last_activity = st.selectbox("Last Activity", ["Email Activity", "Website Activity", "Phone Activity"])
print_media_type1 = st.selectbox("Reached via Newspaper Ads?", ["No", "Yes"])
print_media_type2 = st.selectbox("Reached via Magazine Ads?", ["No", "Yes"])
digital_media = st.selectbox("Reached via Digital Ads?", ["No", "Yes"])
educational_channels = st.selectbox("Reached via Educational Channels?", ["No", "Yes"])
referral = st.selectbox("Referral Lead?", ["No", "Yes"])

if st.button("Predict Conversion Status", type="primary"):
    payload = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }
    
    # Target the backend service inside the Docker Compose network
    backend_url = "http://backend:5000/v1/predict"
    
    try:
        response = requests.post(backend_url, json=payload, timeout=10)
        if response.status_code == 200:
            prediction = response.json().get("Lead", 0)
            if prediction == 1:
                st.success("🎉 Prediction: High Probability of Conversion (Warm Lead!)")
            else:
                st.warning("⚠️ Prediction: Low Probability of Conversion (Cold Lead)")
        else:
            st.error(f"Error: Backend returned status code {response.status_code} ({response.text})")
    except Exception as e:
        st.error(f"Could not connect to the backend server. Error: {e}")
