print("HeartDisease has been reached")

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.S3Data import S3Data
from io import BytesIO
import os
import boto3
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

router = APIRouter()


def upload_to_s3(image_data, filename):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id = os.getenv("ACCESS_KEY_AWS"),
            aws_secret_access_key = os.getenv("SECRET_KEY_AWS"),
            region_name = os.getenv("AWS_BUCKET_REGION")
        )
        bucket_name = os.getenv("AWS_UPLOAD_BUCKET")

        # Upload the file to S3
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=image_data, ContentType='image/svg+xml')

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': filename},
            ExpiresIn=3600  # URL expiration time in seconds (1 hour)
        )
        return {"url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")


@router.get("/countDiseases")
async def count_plot():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")
        # Select relevant columns and melt the DataFrame
        columns_of_interest = ['HeartDisease', 'Asthma', 'KidneyDisease', 'SkinCancer']
        disease_data = fetchedData[columns_of_interest]
        df_melted = disease_data.melt(id_vars='HeartDisease', value_vars=['Asthma', 'KidneyDisease', 'SkinCancer'],
                                      var_name='Condition', value_name='Presence')
        print("Starting to plot.........")
        # Plotting
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df_melted, x='Condition', hue='HeartDisease', dodge=True, palette='viridis')
        plt.title('Count Plot of Asthma, Kidney Disease, and Skin Cancer by Heart Disease Status')
        plt.xlabel('Condition')
        plt.ylabel('Count')
        plt.legend(title='Heart Disease', loc='upper right')
        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")
        # Upload the image to S3
        filename = "countDiseases.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)


@router.get("/correlationHeatmap")
async def correlation_heatmap():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        columns_of_interest = ['HeartDisease', 'BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']
        df_corr = fetchedData[columns_of_interest]
        df_corr['HeartDisease'] = df_corr['HeartDisease'].map({'Yes': 1, 'No': 0})
        df_corr = df_corr.apply(pd.to_numeric, errors='coerce')

        df_corr = df_corr.dropna()

        corr_matrix = df_corr.corr()

        plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt=".2f")
        plt.title('Correlation Heatmap for Heart Disease and Numerical Features')

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        filename = "correlationHeatmap.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/diabeticHeart")
async def diabeticHeart():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=fetchedData, x='Diabetic', hue='HeartDisease', palette='viridis', dodge=True)
        plt.title('Count Plot of Diabetic Status Categorized by Heart Disease')
        plt.xlabel('Diabetic Status')
        plt.ylabel('Count')
        plt.legend(title='Heart Disease', loc='upper right')

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        filename = "diabeticHeart.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/strokeHeart")
async def strokeHeart():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=fetchedData, x='Stroke', hue='HeartDisease', palette='viridis', dodge=True)
        plt.title('Count Plot of Stroke Categorized by Heart Disease')
        plt.xlabel('Stroke History')
        plt.ylabel('Count')
        plt.legend(title='Heart Disease', loc='upper right')

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        filename = "strokeHeart.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)




# @router.get("/")
# async def heartDisease():
#     filekey = 'heart_2020_cleaned.xlsx'
#     fetchedData = S3Data(filekey)
#
#     if isinstance(fetchedData, dict) and 'error' in fetchedData:
#         return fetchedData
#     else:
#         print("Data fetched successfully:", fetchedData)  # Print the DataFrame
#         data_preview = fetchedData.head().to_dict()
#         return {"data": data_preview}



