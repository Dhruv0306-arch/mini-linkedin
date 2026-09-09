from fastapi import FastAPI 

from app.routers import auth , jobs , users

app = FastAPI(title = "Job Board Backend" , version= "0.1.0")

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(users.router)

@app.get("/", tags=["health"])

def health_check():
    return {"status": "ok", "phase": 1}