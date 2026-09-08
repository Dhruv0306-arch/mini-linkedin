# Phase 1 — Skeletons + Solutions

Two parallel folders, same file layout:

- **`skeleton/`** — files with `# TODO` comments and hints, functions raise
  `NotImplementedError`. This is what you actually write in.
- **`solution/`** — fully working reference implementation. Check yourself
  against it, or fall back to it if you get stuck — don't start here.

## Suggested order

1. **Step (a)** — `skeleton/app/storage/memory.py`. Write the in-memory DB.
   Test it directly in a Python shell before touching FastAPI:
   ```python
   from app.storage.memory import db
   u = db.create_user(email="a@b.com", full_name="Ada")
   print(u)
   print(db.get_user_by_email("a@b.com"))
   ```
2. **Step (b)** — `skeleton/app/schemas/{user,job,application}.py`. Pure
   Pydantic, no FastAPI needed yet. Test with:
   ```python
   from app.schemas.job import JobCreate
   j = JobCreate(title="x", company_name="y", location="z", description="d")
   print(j)
   ```
3. **Step (c)** — `skeleton/app/routers/jobs_step_c.py` (GET + POST only).
   You'll also need a minimal `main.py` that includes this router to run
   `uvicorn app.main:app --reload` and test via `/docs`.
4. **Step (d)** — `skeleton/app/routers/jobs_step_d.py`. Full CRUD +
   filtering + pagination. Same file, more endpoints.
5. **Step (e)** — `skeleton/app/core/security.py`,
   `skeleton/app/routers/auth.py`, and
   `skeleton/app/routers/AUTH_WIRING_NOTES.py` (this one's not code to
   run — it's a guide to the small diffs you make in your jobs router
   once auth exists: swapping hardcoded `posted_by=1` for the real
   logged-in user, and adding ownership checks on update/delete).

At each step, run the server and poke at `/docs` before moving to the next.
Don't write all 5 steps then test once — you'll have a much harder time
finding what broke.

## Running the solution (for comparison only)

```bash
cd solution
python3 -m venv venv && source venv/bin/activate
pip install fastapi "uvicorn[standard]" "pydantic[email]" passlib[bcrypt] python-multipart
uvicorn app.main:app --reload
```
