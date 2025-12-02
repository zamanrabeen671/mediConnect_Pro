<!--
	Formatted README for mediConnect_Pro
	Generated: 2025-12-02
-->

# mediConnect_Pro

A Python backend for managing medical appointments, users, and prescriptions.

This repository provides a REST API with authentication, doctor/patient profiles, appointment booking, scheduling, and prescription management.

---

## Features

- User management (register/login, JWT authentication)
- Role-based users: patients, doctors, admins
- Doctor profile management and scheduling
- Appointment booking, status tracking (pending, done, rx_issued)
- Prescription creation and file attachments (images/PDFs)

---

## Tech Stack

- Python
- FastAPI (API framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- MySQL (database)
- Pydantic (data validation)
- JWT (auth), Passlib (password hashing)

---

## Quickstart (Windows / macOS / Linux)

1. Clone the repository

```bash
git clone https://github.com/zamanrabeen671/mediConnect_Pro.git
cd mediConnect_Pro
```

2. Create and activate a virtual environment

Windows (PowerShell / CMD):

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file (example):

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/medi_connect_db
JWT_SECRET_KEY=replace-with-a-secure-random-string
JWT_ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=30
```

5. Start the server

Recommended (uvicorn):

```bash
uvicorn app.main:app --reload
```

Alternative (run module):

```bash
python -m app.main
```

The API will be available at `http://127.0.0.1:8000` and interactive docs at `http://127.0.0.1:8000/docs`.

---

## Project Structure

Top-level layout (important files/folders):

```
readme.md
requirements.txt
app/
	auth.py
	database.py
	main.py
	models.py
	schemas.py
	utils.py
	routers/
		appointments.py
		doctors.py
		patients.py
		prescriptions.py
		schedules.py
		users.py
```

---

## API Overview

Main modules (examples):

- `POST /auth/login` — obtain JWT token
- `POST /users` — create user
- `GET /doctors` — list doctors
- `POST /appointments` — book an appointment
- `POST /prescriptions` — create prescription (attach files)

Refer to the running app's OpenAPI docs (`/docs`) for accurate endpoint signatures and request/response schemas.

---

## Environment & Database

- Ensure MySQL is running and the configured database exists.
- SQLAlchemy models will create tables at runtime (depending on project code). For production use, prefer explicit migrations.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and add tests where applicable
4. Open a pull request describing your changes

If you want, I can add a CONTRIBUTING.md and a small PR template.

---

## License

This project does not include a license file. If you want an open-source license added (MIT, Apache-2.0, etc.), tell me which one and I will add it.

---

## Contact

Repository owner: `zamanrabeen671` (GitHub)

If you'd like, I can:

- add badges (CI, PyPI, license)
- add example requests and responses
- add a `docker-compose` for local MySQL

Tell me which follow-up you'd like next.