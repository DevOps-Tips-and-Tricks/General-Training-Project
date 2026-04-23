from fastapi import FastAPI
from app.routers import items

# Initialize FastAPI App
app = FastAPI(
    title="FastAPI Redis CRUD",
    description="A simple inventory management API using Redis.",
    version="1.0.0"
)

# Include Routers
app.include_router(items.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Redis CRUD API. Visit /docs to test the endpoints."}
