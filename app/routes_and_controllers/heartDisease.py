print("HeartDisease has been reached")

from fastapi import APIRouter, HTTPException, Response
from io import BytesIO
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import httpx

router = APIRouter()

@router.get("/countDiseases")
async def count_plot():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getHeart_disease_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        fetchedData = pd.DataFrame(data)

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
            plt.figure(figsize=(10, 6))
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

            headers = {"Content-Disposition": "inline; filename=countDiseases.svg"}
            return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")


@router.get("/correlationHeatmap")
async def correlation_heatmap():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getHeart_disease_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()
        # filekey = 'heart_2020_cleaned.xlsx'
        # fetchedData = S3Data(filekey)

        fetchedData = pd.DataFrame(data)

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

            headers = {"Content-Disposition": "inline; filename=correlationHeatmap.svg"}
            return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/diabeticHeart")
async def diabeticHeart():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getHeart_disease_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()
        # filekey = 'heart_2020_cleaned.xlsx'
        # fetchedData = S3Data(filekey)

        fetchedData = pd.DataFrame(data)

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

            headers = {"Content-Disposition": "inline; filename=diabeticHeart.svg"}
            return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/strokeHeart")
async def strokeHeart():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getHeart_disease_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()
        # filekey = 'heart_2020_cleaned.xlsx'
        # fetchedData = S3Data(filekey)

        fetchedData = pd.DataFrame(data)

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

            headers = {"Content-Disposition": "inline; filename=strokeHeart.svg"}
            return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")











