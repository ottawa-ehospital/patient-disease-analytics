from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes_and_controllers import heartDisease, patientSugarLevel, factorsOfHeartDiseases, lungCancer

app.include_router(heartDisease.router, prefix="/heartDisease", tags = ["heartDisease"])
app.include_router(patientSugarLevel.router, prefix="/patientSugarLevel", tags=["patientSugarLevel"])
app.include_router(factorsOfHeartDiseases.router, prefix = "/factorsOfHeartDiseases", tags=["factorsOfHeartDiseases"])
app.include_router(lungCancer.router, prefix = "/lungCancer", tags=["lungCancer"])










