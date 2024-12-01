print("LungCancer has been reached")

from fastapi import APIRouter, HTTPException, Response
from io import BytesIO
import zipfile
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import httpx

router = APIRouter()

@router.get("/ChronicDiseaseAndAllergyWithAndWithoutLungCancer")
async def chronic_disease_and_allergy_with_and_without_lung_cancer():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        lc_corr2 = pd.DataFrame(data)

        # Map lung cancer values
        lc_corr2['lung_cancer'] = lc_corr2['lung_cancer'].map({'yes': 2, 'no': 1}).fillna(0)

        # Ensure valid data
        if lc_corr2['lung_cancer'].isnull().any():
            raise HTTPException(status_code=400, detail="Invalid data in lung_cancer column.")

        # Separate the dataset by lung cancer diagnosis
        lung_cancer_yes = lc_corr2[lc_corr2['lung_cancer'] == 2]
        lung_cancer_no = lc_corr2[lc_corr2['lung_cancer'] == 1]

        # Check if subsets are empty
        if lung_cancer_yes.empty or lung_cancer_no.empty:
            raise HTTPException(status_code=400, detail="Insufficient data to generate the plot.")

        # Calculate the incidence of chronic diseases and allergies
        chronic_disease_yes = lung_cancer_yes['chronic_disease'].value_counts(normalize=True).get(2, 0) * 100
        allergy_yes = lung_cancer_yes['allergy'].value_counts(normalize=True).get(2, 0) * 100

        chronic_disease_no = lung_cancer_no['chronic_disease'].value_counts(normalize=True).get(2, 0) * 100
        allergy_no = lung_cancer_no['allergy'].value_counts(normalize=True).get(2, 0) * 100

        # Create a DataFrame for visualization
        incidence_df = pd.DataFrame({
            'Condition': ['Chronic Disease', 'Allergy'],
            'With Lung Cancer (%)': [chronic_disease_yes, allergy_yes],
            'Without Lung Cancer (%)': [chronic_disease_no, allergy_no]
        })

        # Debug: Print calculated values
        print("Incidence DataFrame:")
        print(incidence_df)

        # Plot the data
        print("Starting to plot...")
        plt.figure(figsize=(8,6))
        bar_width = 0.35  # Width of each bar

        # Position of the bars on the x-axis
        index = range(len(incidence_df['Condition']))

        # Plot bars for patients with lung cancer
        plt.bar(index, incidence_df['With Lung Cancer (%)'], width=bar_width, label='With Lung Cancer', color='salmon')

        # Plot bars for patients without lung cancer
        plt.bar([i + bar_width for i in index], incidence_df['Without Lung Cancer (%)'], width=bar_width,
                label='Without Lung Cancer', color='skyblue')

        # Labeling
        plt.title('Incidence of Chronic Disease and Allergy in Patients With and Without Lung Cancer')
        plt.xlabel('Condition')
        plt.ylabel('Incidence (%)')
        plt.xticks([i + bar_width / 2 for i in index], incidence_df['Condition'], rotation=45)
        plt.legend()
        plt.ylim(0, 100)  # Set y-axis limit to 100% for percentage

        # Adding data labels on each bar
        for i, val in enumerate(incidence_df['With Lung Cancer (%)']):
            plt.text(i, val + 1, f'{val:.1f}%', ha='center', color='salmon')
        for i, val in enumerate(incidence_df['Without Lung Cancer (%)']):
            plt.text(i + bar_width, val + 1, f'{val:.1f}%', ha='center', color='skyblue')

        plt.tight_layout()

        print("Plotting completed...")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=ChronicDiseaseAndAllergyWithAndWithoutLungCancer.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/Correlation_Between_Symptoms_And_Lung_Cancer_Diagnosis")
async def correlation_between_symptoms_and_lung_cancer_diagnosis():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        lc_corr2 = pd.DataFrame(data)

        # Map lung cancer values
        lc_corr2['lung_cancer'] = lc_corr2['lung_cancer'].map({'yes': 2, 'no': 1}).fillna(0)
        symptoms = ['yellow_fingers', 'anxiety', 'coughing', 'wheezing', 'chest_pain', 'lung_cancer']
        df_symptoms = lc_corr2[symptoms]

        # Calculate the correlation matrix
        correlation_matrix = df_symptoms.corr()

        # Plotting the correlation matrix as a heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlation between Symptoms and Lung Cancer Diagnosis')

        print("Plotting completed...")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=correlation_between_symptoms_and_lung_cancer_diagnosis.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/Lung_Cancer_Gender_Distribution")
async def lung_cancer_analysis_plots():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        # Fetch data from the external database
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        # Load data into a DataFrame
        lcancer = pd.DataFrame(data)
        lcancer['smoking'] = lcancer['smoking'].map({2: 'Yes', 1: 'No'})

        plt.figure(figsize=(8,6))
        sns.countplot(data=lcancer, x='gender', palette='pastel')
        plt.title('Gender Distribution of Patients')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.show()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=Lung Cancer Gender Distribution of Patients.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/smoking_non_smoking_gender_age")
async def lung_cancer_analysis_plots():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        # Fetch data from the external database
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        # Load data into a DataFrame
        lcancer = pd.DataFrame(data)
        lcancer['smoking'] = lcancer['smoking'].map({2: 'Yes', 1: 'No'})

        plt.figure(figsize=(8,6))
        sns.boxplot(data=lcancer, x='smoking', y='age', hue='gender', palette='coolwarm')
        plt.title('Smoking Status by Gender and Age')
        plt.xlabel('Smoking Status')
        plt.ylabel('Age')
        plt.legend(title='Gender')
        plt.show()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=smoking_non_smoking_gender_age.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/lung_cancer_diagnosis_smoking_status")
async def lung_cancer_analysis_plots():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        # Fetch data from the external database
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        # Load data into a DataFrame
        lcancer = pd.DataFrame(data)
        lcancer['smoking'] = lcancer['smoking'].map({2: 'Yes', 1: 'No'})

        plt.figure(figsize=(8,6))
        sns.countplot(data=lcancer, x='smoking', hue='lung_cancer', palette='Set2')
        plt.title('Lung Cancer Diagnosis by Smoking Status')
        plt.xlabel('Smoking Status')
        plt.ylabel('Count')
        plt.legend(title='Lung Cancer')
        plt.show()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=Lung Cancer Gender Distribution of Patients.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")

@router.get("/Prevalence_Rates_Symptoms_Lung_Cancer_Patients")
async def prevalence_rates_symptoms_lung_cancer_patients():
    database = "https://e-react-node-backend-22ed6864d5f3.herokuapp.com/getLung_cancer_analysis"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(database)
            response.raise_for_status()
            data = response.json()

        lc_symp = pd.DataFrame(data)

        # Map symptoms to binary values for prevalence calculation (1 = No, 2 = Yes)
        symptoms = ['yellow_fingers', 'anxiety', 'coughing', 'wheezing', 'chest_pain']

        # Calculate prevalence of each symptom (percentage of patients with the symptom)
        prevalence = {symptom: (lc_symp[symptom].value_counts(normalize=True)[2] * 100) for symptom in symptoms}

        # Convert the prevalence dictionary to a DataFrame for easy plotting
        prevalence_df = pd.DataFrame(list(prevalence.items()), columns=['Symptom', 'Prevalence (%)'])

        # Plotting the prevalence rates of symptoms
        plt.figure(figsize=(8,6))
        bars = plt.bar(prevalence_df['Symptom'], prevalence_df['Prevalence (%)'], color='teal')
        plt.title('Prevalence Rates of Symptoms in Lung Cancer Patients')
        plt.xlabel('Symptom')
        plt.ylabel('Prevalence (%)')
        plt.ylim(0, 100)  # Ensuring the y-axis is percentage-based
        plt.xticks(rotation=45)


        # Add percentage labels on each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10
            )

        print("Plotting completed...")

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='svg')
        img_buffer.seek(0)
        plt.close()

        print("Image conversion done...")

        headers = {"Content-Disposition": "inline; filename=prevalence_rates_symptoms_lung_cancer_patients.svg"}
        return Response(content=img_buffer.getvalue(), media_type="image/svg+xml", headers=headers, status_code=200)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        raise HTTPException(status_code=400, detail=f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"Request error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail="Error generating the plot")
