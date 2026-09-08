"""
In-memory storage layer - stands in for a real database in phase 1.

WHY THIS SHAPE:method names mirror what a DB layer will look like in
Phase 2 (create_x, get_x, list_x, update_x, delete_x). Keep that pattern —
it's what makes swapping to SQLAlchemy later a small diff instead of a
rewrite of every router."""

from itertools import count
from typing import Optional

class InMemoryDB:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self.jobs: dict[int, dict] = {}
        self.applications: dict[int, dict] = {}

        self._user_ids = count(1)
        self._job_ids = count(1)
        self._application_ids = count(1)


    # USERS
    def create_user(self, **kwargs) -> dict:
        user_id = next(self._user_ids)
        user = {"id": user_id, **kwargs}
        self.users[user_id] = user
        return user

    def get_user_by_email(self , email: str) -> Optional[dict]:
        return next((u for u in self.users.values() if u["email"] == email), None)

    def get_user(self, user_id: int) -> Optional[dict]:
        return self.users.get(user_id)

    # JOBS

    def create_job(self, **kwargs) -> dict:
        job_id = next(self._job_ids)
        job = {"id" : job_id, **kwargs}
        self.jobs[job_id] = job
        return job

    def get_job(self, job_id:int) -> Optional[dict]:
        return self.jobs.get(job_id)

    def list_jobs(self) -> list[dict]:
        return list(self.jobs.values())

    def update_job(self, job_id: int, **fields) -> Optional[dict]:
        job = self.jobs.get(job_id)
        