from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import routes
from app.routes import candidate, role, stage, application, experience, opening

# Import database connection
from app.database.connection import get_db, init_db

# Create FastAPI app
app = FastAPI(
    title="Recruitment API",
    description="API for managing recruitment processes",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidate.router, prefix="/candidates", tags=["Candidates"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(stage.router, prefix="/stages", tags=["Stages"])
app.include_router(application.router, prefix="/applications", tags=["Applications"])
app.include_router(experience.router, prefix="/experiences", tags=["Experiences"])
app.include_router(opening.router, prefix="/openings", tags=["Openings"])


@app.on_event("startup")
async def startup():
    """Initialize connections and resources on startup."""
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    """Close connections and free resources on shutdown."""
    # Add shutdown logic here if needed
    pass


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Recruitment API is running"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

