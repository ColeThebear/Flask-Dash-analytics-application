# Zendesk Flask Application
A full‑stack Flask + Dash analytics application for visualizing Zendesk ticket data, managing user authentication, and providing a clean, interactive dashboard for operational insights.

This project demonstrates:
- A Flask backend with authentication (login, register, logout)
- A PostgreSQL database with SQLAlchemy ORM
- A Dash dashboard mounted inside Flask
- Environment‑based configuration (dev, test, prod)
- Secure password hashing with Bcrypt
- Blueprint‑based modular architecture
- A data‑driven UI using Plotly, Dash Mantine Components, and Dash DataTable

---

## Features

### Authentication
- User registration and login
- Password hashing with Bcrypt
- Session management with Flask‑Login
- Protected dashboard route

### Dashboard
- Interactive histogram of ticket duration
- Paginated ticket table
- Draggable grid layout
- System information panel (version, environment, commit hash)
- Fully integrated Dash app mounted at `/dashboard/`

### Database
- PostgreSQL backend
- SQLAlchemy ORM models:
- `User`
- `Ticket`
- Automatic table creation on startup

### Configuration
Environment‑specific settings via:
- `dev.env`
- `test.env`
- `PROD.env`

Supports:
- Custom database URLs
- Secret keys
- Deployment metadata
- Git commit extraction (production only)

---

## Project Structure
Zendesk Flask Application/ │ ├── app.py ├── auth.py ├── dashboard.py ├── extensions.py ├── models.py ├── config.py ├── login.py # Legacy (to be removed) ├── logout.py # Legacy (to be removed) ├── register.py # Legacy (to be removed) │ ├── templates/ │ ├── login.html │ ├── register.html │ └── about.html │ ├── instance/ │ ├── dev.env │ ├── test.env │ └── PROD.env │ ├── setup.cfg ├── Zendesk Export.csv ├── Ticket DB Update.sql └── README.md


---

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd zendesk-flask-application


2. Create a virtual environment

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows


3. Install dependencies

pip install -r requirements.txt


4. Configure environment

Copy one of the environment files:

cp instance/dev.env .env


Or set manually:

FLASK_ENV=development
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret


5. Run the application

python app.py


# Dashboard available at:
http://localhost:5000/dashboard/

---

# Testing

Set environment to testing:

FLASK_ENV=testing


Then run your test suite (to be added):

pytest


---

# Deployment

## Production configuration includes:

• Git commit extraction
• Environment‑based DB URL
• Secure secret key loading


## Recommended stack:

• Gunicorn or Waitress
• Nginx reverse proxy
• Systemd service
• Docker (optional)
• AWS Elastic Beanstalk or EC2


---

### Roadmap

See TODO.md for a full breakdown of improvements and next steps.

---

# License

MIT License

---

# Author

Cole
Support Analyst → Python Developer
Focused on Flask, Django, automation, and cloud deployment.