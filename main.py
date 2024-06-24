from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.router import router
import routes

app = FastAPI(title="VQA Annotator", version="0.0.1")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(router)