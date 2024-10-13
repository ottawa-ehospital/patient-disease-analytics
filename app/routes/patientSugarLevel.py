from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.S3Data import S3Data
from io import BytesIO
from .heartDisease import upload_to_s3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

router = APIRouter()

# Function to calculate BMI and categorize it
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Function to get cholesterol status
def get_cholesterol_status(cholesterol):
    if cholesterol == 0:
        return 'No data'
    elif cholesterol < 200:
        return 'Normal'
    elif 200 <= cholesterol < 240:
        return 'Borderline High'
    else:
        return 'High'

# Function to determine BMI category
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

@router.get("/patient/{patient_id}/sugar-levels")

def get_patient_details(patient_id: int):
    print("At least you have entered the patientSugarLevel route")
    # Fetch patient data from S3
    patient_data_key = "patient_data 1.xlsx"
    blood_sugar_data_key = "blood_sugar_levels 1.xlsx"

    # Read patient data and blood sugar levels data from S3
    patient_data = S3Data(patient_data_key)
    blood_sugar_data = S3Data(blood_sugar_data_key)

    if isinstance(patient_data, dict) and 'error' in patient_data:
        return JSONResponse(status_code=500, content={"message": patient_data['error']})
    if isinstance(blood_sugar_data, dict) and 'error' in blood_sugar_data:
        return JSONResponse(status_code=500, content={"message": blood_sugar_data['error']})

    # Filter patient data based on the given ID
    patient_detail = patient_data[patient_data['id'] == patient_id]

    if patient_detail.empty:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

    # Check if patient data is found
    if not patient_detail.empty:
        # Extract patient details
        first_name = patient_detail['FName'].values[0]
        last_name = patient_detail['LName'].values[0]
        age = int(patient_detail['Age'].values[0])  # Ensure this is an int
        gender = patient_detail['Gender'].values[0]
        height = int(patient_detail['height'].values[0] / 100)  # Convert to meters and then to int for display
        weight = int(patient_detail['weight'].values[0])  # Ensure this is an int
        blood_group = patient_detail['BloodGroup'].values[0]
        serum_choles = int(patient_detail['serumcholestrol'].values[0])  # Ensure this is an int
        blood_sugar = int(patient_detail['fastingbloodsugar'].values[0])  # Ensure this is an int

        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        cholesterol_status = get_cholesterol_status(serum_choles)
        bmi_category = get_bmi_category(bmi)
        blood_sugar_status = 'Diabetic' if blood_sugar == 1 else 'Non-Diabetic'

        # Return patient details as JSON
        return JSONResponse(status_code=200, content={
            "Name": f"{first_name} {last_name}",
            "Age": age,
            "Gender": gender,
            "Height (cm)": height * 100,  # Convert back to cm for display
            "Weight (kg)": weight,
            "Blood Group": blood_group,
            "BMI": round(bmi, 2),
            "BMI Category": bmi_category,
            "Cholesterol (mg/dL)": serum_choles,
            "Cholesterol Status": cholesterol_status,
            "Blood Sugar": blood_sugar,
            "Blood Sugar Status": blood_sugar_status
        })


@router.get("/patient/{patient_id}/monthlySugarReport")
def monthlySugarReport(patient_id: int):
    # Read blood sugar levels data from S3
    blood_sugar_data_key = "blood_sugar_levels 1.xlsx"
    blood_sugar_data = S3Data(blood_sugar_data_key)

    if isinstance(blood_sugar_data, dict) and 'error' in blood_sugar_data:
        raise HTTPException(status_code=500, detail=blood_sugar_data['error'])

    # Check if patient data exists
    if patient_id not in blood_sugar_data["id"].values:
        raise HTTPException(status_code=404, detail=f"No data found for Patient ID: {patient_id}")

    # Filter data for the patient
    patient_data = blood_sugar_data[blood_sugar_data["id"] == patient_id]
    patient_data = patient_data.set_index("id")

    # Extract months and values for plotting
    time_points = list(patient_data.columns)
    blood_sugar_levels = patient_data.loc[patient_id].values

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(time_points, blood_sugar_levels, marker='o', linestyle='-', color='b')
    plt.title(f'Blood Sugar Level vs Time for Patient {patient_id}')
    plt.xlabel('Time')
    plt.ylabel('Blood Sugar Level (mg/dL)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='svg')
    img_buffer.seek(0)
    plt.close()

    # Upload the image to S3
    filename = f"monthlySugarReport_{patient_id}.svg"
    upload_result = upload_to_s3(img_buffer, filename)

    if 'error' in upload_result:
        raise HTTPException(status_code=500, detail=upload_result['error'])

    return JSONResponse(status_code=200, content= upload_result)