import boto3
import os
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from io import BytesIO

def S3Data(fileKey):
    try:
        print("Attempting to fetch data from S3")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("ACCESS_KEY_AWS"),
            aws_secret_access_key=os.getenv("SECRET_KEY_AWS"),
            region_name=os.getenv("AWS_BUCKET_REGION")
        )
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        fileKey = fileKey

        response = s3_client.get_object(Bucket=bucket_name, Key=fileKey)
        print("Data fetched from S3, processing as Excel")
        file_stream = response['Body'].read()
        excel_data = pd.read_excel(BytesIO(file_stream))
        print("Excel file loaded into DataFrame")
        return excel_data  # Read the file contents
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except PartialCredentialsError:
        return {"error": "Incomplete credentials provided."}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"error": f"Error: {str(e)}"}


