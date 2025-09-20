# Sweet Shop Management System

A compact Sweet Shop Management System using **FastAPI** (backend) and **React** (frontend).  
This repository includes JWT auth, admin role management, CRUD for sweets, purchase/restock endpoints, search, categories, and a polished React UI.

---

## Contents
- `backend/` — FastAPI backend (Python)
- `frontend/` — React frontend
- `README_frontend.md` — frontend setup & notes

---

## Quick overview

**Backend**
- `FastAPI`, `SQLAlchemy` with SQLite.
- JWT authentication using `python-jose`, first registered user becomes admin.
- Endpoints:
  - `POST /api/auth/register` — register user (returns `{access_token, token_type, is_admin}`)
  - `POST /api/auth/login` — obtain token (OAuth2 password form)
  - `GET /api/sweets` — list sweets (public, pagination: `skip`, `limit`)
  - `GET /api/sweets/categories` — list categories (public)
  - `GET /api/sweets/{id}` — get sweet by id (public)
  - `GET /api/sweets/search` — search sweets (public) with `query`, `category`, `min_price`, `max_price`
  - `POST /api/sweets` — add sweet (admin only)
  - `PUT /api/sweets/{id}` — update sweet (admin only; partial update supported on frontend)
  - `DELETE /api/sweets/{id}` — delete sweet (admin only)
  - `POST /api/sweets/{id}/purchase?qty=#` — purchase (auth required)
  - `POST /api/sweets/{id}/restock?qty=#` — restock (admin only)

**Frontend**
- React + Vite SPA with:
  - Login, Register, SweetsList, SweetForm (add/edit/restock/delete).
  - Search and filter (query), responsive grid, cards with images and description.
- Environment variable `VITE_API_URL` to point to backend.

---

## Getting started

### Backend (FastAPI)

1) Open terminal, go to `backend/` and create a venv:

```bash
python -m venv .venv
# activate:
# mac/linux: source .venv/bin/activate
# windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Configure environment variables (optional). A sample `.env` is present (`SECRET_KEY`, etc.). Default DB is `sqlite:///./sweetshop.db`.

3) Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

Notes:
- Lightweight SQLite migrations run automatically on startup to add newly introduced columns.
- The first registered user becomes `admin`.

### Frontend (React + Vite)

1) Open terminal, go to `frontend/` and install deps:

```bash
npm install
```

2) Ensure `.env` contains:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

3) Start dev server:

```bash
npm run dev
```

Open the URL shown by Vite (typically http://127.0.0.1:5173)

---

## Testing

Backend tests use `pytest`.

```bash
cd backend
pytest -q
```

The test suite covers registration/login, CRUD, purchase, and search.

---

## Screenshots

Add screenshots of the final app here, e.g.:
- Login/Register screen
- Sweets dashboard with cards and images
- Admin sweet management form

---

## My AI Usage

- Tools used: ChatGPT (Cascade), GitHub Copilot (optional).
- How I used them:
  - Brainstormed API design enhancements (search filters, categories) and admin role management strategy.
  - Generated boilerplate for some Pydantic schemas and improved error handling.
  - Helped write and refactor tests to align with updated API contracts.
  - Assisted in polishing frontend UI structure and state handling for forms and search.
- Reflection:
  - AI accelerated scaffolding and reduced routine boilerplate, letting me focus on domain-specific details and UX polish.
  - I reviewed and adapted all AI suggestions to fit the project’s style and constraints, ensuring correctness and readability.

Per the kata policy, commits that used AI include co-author attribution.

---

## Git workflow & Commit Convention

- Conventional commits (feat, fix, refactor, test, docs, chore).
- For any commit aided by AI, include:

```bash
Co-authored-by: AI Tool Name <AI@users.noreply.github.com>
```

---

## Deployment (optional)

You can deploy the frontend (Vercel/Netlify) and backend (Render/Fly.io/Heroku). Ensure CORS is open or configured to your domain.
