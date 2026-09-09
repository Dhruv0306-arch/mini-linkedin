from datetime import datetime , timezone
from typing import Optional
from fastapi import APIRouter , Depends , HTTPException , Query , status

from app.core.security import get_current_user
from app.schemas.application import ApplicationCreate, ApplicationOut
from app.schemas.job import JobCreate, JobListOut, JobOut, JobUpdate
from app.storage.memory import db


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=JobListOut)
def list_jobs(
    location: Optional[str] = None,
    skill: Optional[str] = None,
    remote: Optional[bool] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    q: Optional[str] = None,
    page: int = Query(10, ge=1, le=100),
    page_size: int = Query(10, ge=1, le=100),
):
    results = db.list_jobs()

    if location:
        results = [j for j in results if location.lower() in j["location"].lower()]
    if skill:
        results = [j for j in results if skill.lower() in [s.lower() for s in j["skills"]]]
    if remote is not None:
        results = [j for j in results if j["remote"] == remote]
    if salary_min is not None:
        results = [j for j in results if (j["salary_max"] or 0) >= salary_min]
    if salary_max is not None:
        results = [j for j in results if (j["salary_min"] or 0) <= salary_max]
    if q:
        ql = q.lower()
        results = [
            j for j in results
            if ql in j["title"].lower() or ql in j["description"].lower()
        ]
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    page_results = results[start:end]

    return JobListOut(total=total, page=page, page_size=page_size, results=page_results)


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, current_user: dict = Depends(get_current_user)):
    job = db.create_job(
        **payload.model_dump(),
        posted_by = current_user["id"],
        created_at = datetime.now(timezone.utc),
    )
    return job

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int):
    job = db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, payload: JobUpdate, current_user: dict = Depends(get_current_user)):
    job = db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["posted_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job")

    updated = db.update_job(job_id, **payload.model_dump(exclude_unset=True))
    return updated

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, current_user: dict = Depends(get_current_user)):
    job = db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["posted_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")

    db.delete_job(job_id)

@router.post("/{job_id}/apply", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def apply_to_job(
    job_id: int,
    payload: ApplicationCreate,
    current_user: dict = Depends(get_current_user),
):
    job = db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if db.has_applied(job_id, current_user["id"]):
        raise HTTPException(status_code=400, detail="You already applied to this job")

    application = db.create_application(
        job_id=job_id,
        user_id=current_user["id"],
        cover_note=payload.cover_note,
        created_at=datetime.now(timezone.utc),
    )
    return application
