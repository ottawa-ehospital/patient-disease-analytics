from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
import httpx
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

router = APIRouter()

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_cholesterol_status(cholesterol):
    if cholesterol == 0:
        return 'No data'
    elif cholesterol < 200:
        return 'Normal'
    elif 200 <= cholesterol < 240:
        return 'Borderline High'
    else:
        return 'High'

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
async def get_patient_details(patient_id: int):
    print("At least you have entered the patientSugarLevel route")
    patient_database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getPatients_analysis"
    sugar_report_database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getBlood_sugar_analysis"

    try:
        # Fetch data from APIs
        async with httpx.AsyncClient() as client:
            patient_response = await client.post(patient_database)
            sugar_report_response = await client.post(sugar_report_database)
            patient_response.raise_for_status()
            sugar_report_response.raise_for_status()
            patient_data = pd.DataFrame(patient_response.json())
            blood_sugar_data = pd.DataFrame(sugar_report_response.json())

        # Validate patient data
        if patient_data.empty:
            raise HTTPException(status_code=500, detail="Patient data is empty.")
        if blood_sugar_data.empty:
            raise HTTPException(status_code=500, detail="Blood sugar data is empty.")

        # Filter patient data
        patient_detail = patient_data[patient_data['id'] == patient_id]
        if patient_detail.empty:
            raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

        # Extract patient details
        first_name = patient_detail['FName'].values[0]
        last_name = patient_detail['LName'].values[0]
        age = int(patient_detail['age'].values[0])
        gender = patient_detail['gender'].values[0]
        height = patient_detail['height'].values[0] / 100.0  # Convert to meters
        weight = int(patient_detail['weight'].values[0])
        blood_group = patient_detail['BloodGroup'].values[0]
        serum_choles = int(patient_detail['serum_cholesterol'].values[0])
        blood_sugar = int(patient_detail['fastingbloodsugar'].values[0])

        # Calculate BMI and other details
        bmi = calculate_bmi(weight, height)
        cholesterol_status = get_cholesterol_status(serum_choles)
        bmi_category = get_bmi_category(bmi)
        blood_sugar_status = 'Diabetic' if blood_sugar == 1 else 'Non-Diabetic'

        # Return patient details as JSON
        return JSONResponse(
            status_code=200,
            content={
                "Name": f"{first_name} {last_name}",
                "Age": age,
                "Gender": gender,
                "Height (cm)": round(height * 100, 1),
                "Weight (kg)": weight,
                "Blood Group": blood_group,
                "BMI": round(bmi, 2),
                "BMI Category": bmi_category,
                "Serum Cholesterol": serum_choles,
                "Cholesterol Status": cholesterol_status,
                "Blood Sugar Status": blood_sugar_status,
            },
        )

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the patient details.")

@router.get("/patient/{patient_id}/monthlySugarReport")
async def monthlySugarReport(patient_id: int):
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getBlood_sugar_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        blood_sugar_data = pd.DataFrame(data)

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

        headers = {"Content-Disposition": "inline; filename=monthlysugarreport.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")