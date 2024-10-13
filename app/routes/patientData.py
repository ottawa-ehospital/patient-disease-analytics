print("patientData has been reached")

from fastapi import APIRouter
from app.services.S3Data import S3Data
import os

router = APIRouter()

@router.get("/")
async def patientData():
    filekey = 'patient_data 1.xlsx'
    fetchedData = S3Data(filekey)
    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        print(f"Error occurred: {fetchedData}")
        return fetchedData
    else:
        print("Data fetched successfully:", fetchedData)
        data_preview = fetchedData.head().to_dict()
        return {"data": data_preview}