from datetime import datetime
from typing import Optional
from pydantic import BaseModel , Field


class JobBase(BaseModel):
    title: str
    company_name: str
    location: str
    description: str
    skills: list[str] = Field(default_factory = list)
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote: bool = False


class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[list[str]] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote: Optional[bool] = None

class JobOut(JobBase):
    id: int
    posted_by: int # We'll use the user ID i guess??
    created_at: datetime

    class Config:
        from_attributes = True


class JobListOut(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[JobOut]
    