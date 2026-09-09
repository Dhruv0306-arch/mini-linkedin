from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.schemas.job import JobCreate, JobOut
from app.storage.memory import db

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobOut])
def list_jobs():
    return db.list_jobs()


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate):
    job = db.create_job(
        **payload.model_dump(),
        posted_by=1,  # placeholder until auth (step e) exists
        created_at=datetime.now(timezone.utc),
    )
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int):
    job = db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
