from flask import Flask, send_file, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the hospital recommendation dataset CSV
hospital_data = pd.read_csv('C:\\Users\\DIVYA\\Desktop\\Medisphere\\hospital\\hospital_recommendation_dataset_UPDATED.csv')

def recommend_hospital(patient_location, patient_illness):
    try:
        # Filter hospitals by the patient's location and illness
        hospitals_with_criteria = hospital_data[(hospital_data['Location'].str.contains(patient_location, case=False)) &
                                                (hospital_data['Specialties'].str.contains(patient_illness, case=False))]

        if hospitals_with_criteria.empty:
            return {"error": "Sorry, there are no hospitals in {} specializing in {}.".format(patient_location, patient_illness)}

        # Sort hospitals by quality measures or any other relevant criteria
        recommended_hospital = hospitals_with_criteria.iloc[0]  # For simplicity, just recommend the first hospital

        return {"Hospital": recommended_hospital['Hospital Name'], "Location": recommended_hospital['Location']}
    except Exception as e:
        return {"error": "An error occurred: {}".format(e)}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    location = request.args.get('location')
    illness = request.args.get('illness')
    return jsonify(recommend_hospital(location, illness))

if __name__ == "__main__":
    app.run(debug=True)
