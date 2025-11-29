"""
Main FastAPI application entry point for EduCred.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS, API_PREFIX

app = FastAPI(
    title="EduCred API",
    description="AI-Powered Certificate Authenticity Analyzer",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "EduCred API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Import and include routes
from app.routes import certificate
app.include_router(certificate.router, prefix=API_PREFIX)

