from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.routes import bloodSugarLevel, heartDisease, patientData, patientSugarLevel, factorsOfHeartDiseases

print("Hello world")

app.include_router(bloodSugarLevel.router, prefix="/bloodSugarLevel", tags = ["bloodSugarLevel"])
app.include_router(heartDisease.router, prefix="/heartDisease", tags = ["heartDisease"])
app.include_router(patientData.router, prefix="/patientData", tags = ["patientData"])
app.include_router(patientSugarLevel.router, prefix="/patientSugarLevel", tags=["patientSugarLevel"])
app.include_router(factorsOfHeartDiseases.router, prefix = "/factorsOfHeartDiseases", tags=["factorsOfHeartDiseases"])





# Example route for testing S3 access
# @app.get("/test-s3")
# def test_s3_access():
#     try:
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=os.getenv("ACCESS_KEY_AWS"),
#             aws_secret_access_key=os.getenv("SECRET_KEY_AWS"),
#             region_name=os.getenv("AWS_BUCKET_REGION")
#         )
#         bucket_name = os.getenv("AWS_BUCKET_NAME")
#
#         response = s3_client.list_objects_v2(Bucket=bucket_name)
#
#         if 'Contents' in response:
#             objects_list = [obj['Key'] for obj in response['Contents']]
#             return {"message": f"Objects in {bucket_name}: {objects_list}"}
#         else:
#             return {"message": f"No objects found in {bucket_name}."}
#
#     except NoCredentialsError:
#         return {"error": "Credentials not available"}
#     except PartialCredentialsError:
#         return {"error": "Incomplete credentials provided."}
#     except Exception as e:
#         return {"error": f"Error: {str(e)}"}

# origins = [
#     "http://localhost:3000",  # React frontend in development
#     "https://myfrontend.com", # Production frontend
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,        # List of allowed origins (domains)
#     allow_credentials=True,       # Whether to allow cookies and authentication headers
#     allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],          # Allow all request headers
# )
#
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to FastAPI"}
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}




