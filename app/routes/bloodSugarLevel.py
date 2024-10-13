print("BloodSugarLevel has been reached")

from fastapi import APIRouter
from app.services.S3Data import S3Data
import os

router = APIRouter()

@router.get("/")
async def read_bloodSugarLevel():
    filekey = 'blood_sugar_levels 1.xlsx'
    fetchedData = S3Data(filekey)
    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        print(f"Error occurred: {fetchedData}")
        return fetchedData
    else:
        print("Data fetched successfully:", fetchedData)
        data_preview = fetchedData.head().to_dict()
        return {"data": data_preview}

