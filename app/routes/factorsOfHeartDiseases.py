from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.S3Data import S3Data
from io import BytesIO
from .heartDisease import upload_to_s3
import os
import boto3
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

router = APIRouter()


@router.get("/bmi-Vs-Heart")
async def bmiVsHeart():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        # Ensure 'HeartDisease' column is binary (1 for 'Yes' and 0 for 'No')
        fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)

        # Categorize BMI
        def categorize_bmi(bmi):
            if bmi < 18.5:
                return 'Underweight (0-18.5)'
            elif 18.5 <= bmi < 24.9:
                return 'Normal (18.5-24.9)'
            elif 25 <= bmi < 29.9:
                return 'Overweight (25-29.9)'
            elif 30 <= bmi < 34.9:
                return 'Obese (30-34.9)'
            else:
                return 'Severely Obese (35+)'

        fetchedData['BMI_Category'] = fetchedData['BMI'].apply(categorize_bmi)

        # Order categories
        bmi_order = ['Underweight (0-18.5)', 'Normal (18.5-24.9)', 'Overweight (25-29.9)', 'Obese (30-34.9)',
                     'Severely Obese (35+)']
        fetchedData['BMI_Category'] = pd.Categorical(fetchedData['BMI_Category'], categories=bmi_order, ordered=True)

        print("Starting to plot.........")

        # Plotting
        plt.figure(figsize=(8, 6))
        sns.countplot(x='BMI_Category', hue='HeartDisease', data=fetchedData, palette="coolwarm")
        plt.title('Heart Disease Prevalence by BMI Category')
        plt.xlabel('BMI Category')
        plt.ylabel('Count')
        plt.legend(title='Heart Disease', loc='upper right', labels=['No', 'Yes'])
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "bmi-Vs-Heart.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/smokingHeart")
async def count_plot_smoking_habits():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)
        # Filter to include only heart disease cases

        df_heart_disease = fetchedData[fetchedData['HeartDisease'] == 1]
        print("Starting to plot.........")

        # Plotting
        plt.figure(figsize=(8, 6))
        sns.countplot(x='Smoking', data=df_heart_disease, palette="coolwarm")
        plt.title('Smoking Habits of Individuals with Heart Disease')
        plt.xlabel('Smoking')
        plt.ylabel('Count')
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "count_smoking_habits.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        print(JSONResponse(content=upload_result, status_code=200))
        return JSONResponse(content=upload_result, status_code=200)

@router.get("/alcoholHeart")
async def count_plot_alcohol_drinking():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)
        # Filter to include only heart disease cases
        df_heart_disease = fetchedData[fetchedData['HeartDisease'] == 1]

        print("Starting to plot.........")

        # Plotting
        plt.figure(figsize=(8, 6))
        sns.countplot(x='AlcoholDrinking', data=df_heart_disease, palette="coolwarm")
        plt.title('Alcohol Drinking for Individuals with Heart Disease')
        plt.xlabel('Alcohol Drinking')
        plt.ylabel('Count')
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "count_alcohol_drinking.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/physicalActivity-Sleep-HealthyHeart")
async def box_plot_physical_activity_vs_sleep_time():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)
        # Filter to include only heart disease cases
        df_heart_disease = fetchedData[fetchedData['HeartDisease'] == 1]

        print("Starting to plot.........")

        # Plotting
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='PhysicalActivity', y='SleepTime', data=df_heart_disease, palette="coolwarm")
        plt.title('Physical Activity vs. Sleep Time for Individuals with Heart Disease')
        plt.xlabel('Physical Activity (Yes/No)')
        plt.ylabel('Sleep Time (hours)')
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "box_physical_activity_sleep_time.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/generalHealth-Heart")
async def bar_plot_general_health_vs_heart_disease():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        # Order General Health categories
        gen_health_order = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
        fetchedData['GenHealth'] = pd.Categorical(fetchedData['GenHealth'], categories=gen_health_order, ordered=True)

        print("Starting to plot.........")

        # Plot ordered General Health vs Heart Disease
        plt.figure(figsize=(10, 6))
        sns.barplot(x='GenHealth', y='HeartDisease', data=fetchedData, hue='GenHealth', palette="coolwarm", legend=False)
        plt.title('Heart Disease Prevalence by General Health')
        plt.xlabel('General Health')
        plt.ylabel('Prevalence of Heart Disease (0.10 = 10%)')  # Clarified the meaning of prevalence
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "bar_general_health_heart_disease.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/sleepVsHeart-modified")
async def histogram_sleep_time_vs_heart_disease():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        print("Starting to plot.........")

        # Plot histogram of Sleep Time vs. Heart Disease
        plt.figure(figsize=(8, 6))
        sns.histplot(data=fetchedData, x='SleepTime', hue='HeartDisease', kde=True,
                     palette="coolwarm", multiple="stack")
        plt.title('Distribution of Sleep Time and Heart Disease')
        plt.xlabel('Sleep Time (hours)')
        plt.ylabel('Frequency')
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "histogram_sleep_time_heart_disease.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/physicalActivity-HeartDiseases")
async def count_plot_physical_activity_vs_heart_disease():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])
    else:
        print("Fetched data successfully")

        fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)

        # Filter the dataset to include only individuals with heart disease
        df_heart_disease = fetchedData[fetchedData['HeartDisease'] == 1]

        print("Starting to plot.........")

        # Plot count of Physical Activity for individuals with heart disease
        plt.figure(figsize=(8, 6))
        sns.countplot(x='PhysicalActivity', data=df_heart_disease, palette="coolwarm")
        plt.title('Physical Activity for Individuals with Heart Disease')
        plt.xlabel('Physical Activity (Yes/No)')
        plt.ylabel('Count')
        plt.tight_layout()

        print("Plotting completed....")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done........")

        # Upload the image to S3
        filename = "count_physical_activity_heart_disease.svg"
        upload_result = upload_to_s3(img_buffer, filename)
        print(upload_result)
        if 'error' in upload_result:
            raise HTTPException(status_code=500, detail=upload_result['error'])

        return JSONResponse(content=upload_result, status_code=200)

@router.get("/ageVsDisease")
async def age_vs_heart_disease_prevalence():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])

    print("Fetched data successfully")

    # Ensure data is properly formatted
    fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Group by age category and calculate heart disease prevalence
    age_heart_disease = fetchedData.groupby('AgeCategory')['HeartDisease'].mean()

    # Plot Age Category vs. Heart Disease Prevalence
    plt.figure(figsize=(10, 6))
    sns.barplot(x=age_heart_disease.index, y=age_heart_disease.values, palette="coolwarm")
    plt.title('Heart Disease Prevalence by Age Category')
    plt.xlabel('Age Category')
    plt.ylabel('Prevalence of Heart Disease')
    plt.xticks(rotation=45)
    plt.tight_layout()

    print("Plotting completed....")

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='svg')
    img_buffer.seek(0)
    plt.close()

    print("Image conversion done........")

    # Upload the image to S3
    filename = "age_vs_heart_disease_prevalence.svg"
    upload_result = upload_to_s3(img_buffer, filename)
    print(upload_result)
    if 'error' in upload_result:
        raise HTTPException(status_code=500, detail=upload_result['error'])

    return JSONResponse(content=upload_result, status_code=200)

@router.get("/bmiVsHeart")
async def bmi_vs_heart_disease_prevalence():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])

    print("Fetched data successfully")

    # Ensure data is properly formatted
    fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)
    fetchedData['BMI'] = pd.to_numeric(fetchedData['BMI'], errors='coerce')

    # Define BMI categories
    def bmi_category(bmi):
        if bmi < 18.5:
            return 'Underweight (0-18.5)'
        elif 18.5 <= bmi < 24.9:
            return 'Normal (18.5-24.9)'
        elif 25 <= bmi < 29.9:
            return 'Overweight (25-29.9)'
        elif 30 <= bmi < 34.9:
            return 'Obese (30-34.9)'
        else:
            return 'Severely Obese (35+)'

    fetchedData['BMI_Category'] = fetchedData['BMI'].apply(bmi_category)

    # Group by BMI category and calculate heart disease prevalence
    bmi_heart_disease = fetchedData.groupby('BMI_Category')['HeartDisease'].mean()

    # Plot BMI Category vs. Heart Disease Prevalence
    plt.figure(figsize=(10, 6))
    sns.barplot(x=bmi_heart_disease.index, y=bmi_heart_disease.values, palette="coolwarm")
    plt.title('Heart Disease Prevalence by BMI Category')
    plt.xlabel('BMI Category')
    plt.ylabel('Prevalence of Heart Disease')
    plt.xticks(rotation=45)
    plt.tight_layout()

    print("Plotting completed....")

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='svg')
    img_buffer.seek(0)
    plt.close()

    print("Image conversion done........")

    # Upload the image to S3
    filename = "bmi_vs_heart_disease_prevalence.svg"
    upload_result = upload_to_s3(img_buffer, filename)
    print(upload_result)
    if 'error' in upload_result:
        raise HTTPException(status_code=500, detail=upload_result['error'])

    return JSONResponse(content=upload_result, status_code=200)

@router.get("/sexVsHeart")
async def sex_vs_heart_disease_prevalence():
    filekey = 'heart_2020_cleaned.xlsx'
    fetchedData = S3Data(filekey)

    if isinstance(fetchedData, dict) and 'error' in fetchedData:
        raise HTTPException(status_code=500, detail=fetchedData['error'])

    print("Fetched data successfully")

    # Ensure data is properly formatted
    fetchedData['HeartDisease'] = fetchedData['HeartDisease'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Group by Sex and calculate heart disease prevalence
    sex_heart_disease = fetchedData.groupby('Sex')['HeartDisease'].mean()

    # Plot Sex vs. Heart Disease Prevalence
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sex_heart_disease.index, y=sex_heart_disease.values, palette="coolwarm")
    plt.title('Heart Disease Prevalence by Sex')
    plt.xlabel('Sex')
    plt.ylabel('Prevalence of Heart Disease')
    plt.tight_layout()

    print("Plotting completed....")

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='svg')
    img_buffer.seek(0)
    plt.close()

    print("Image conversion done........")

    # Upload the image to S3
    filename = "sex_vs_heart_disease_prevalence.svg"
    upload_result = upload_to_s3(img_buffer, filename)
    print(upload_result)
    if 'error' in upload_result:
        raise HTTPException(status_code=500, detail=upload_result['error'])

    return JSONResponse(content=upload_result, status_code=200)
