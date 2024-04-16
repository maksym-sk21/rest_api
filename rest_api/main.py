from fastapi import FastAPI
from src.routes.contacts import router as contact_router

app = FastAPI()

app.include_router(contact_router)

