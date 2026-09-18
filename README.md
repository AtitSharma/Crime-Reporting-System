# Crime Reporting System (CRS)

A web-based Crime Reporting System built with Django that allows citizens to report crimes, track investigation status, and helps police manage and respond to reports through an admin dashboard with analytics.

## Features

- **Report a Crime** — Citizens can submit detailed crime reports with proof documents
- **Track Reports** — Look up reports using email and phone number
- **Status Updates** — Reports progress through Pending, Investigating, and Action Taken
- **Police Portal** — Authenticated police officers can update report status and add explanations
- **Admin Dashboard** — Analytics with charts for station-wise, time-wise, and status-wise breakdowns
- **Responsive Design** — Works on desktop, tablet, and mobile devices
- **Database Seeding** — Pre-loaded with 12 Nepal police stations and 120 realistic crime reports

## Tech Stack

- **Backend:** Django 5.1.7, Python 3.10+
- **Database:** PostgreSQL (via psycopg 3.2.6)
- **Frontend:** HTML, CSS, Bootstrap 5, Font Awesome 6
- **Admin:** django-jet, django-admin-interface
- **Environment:** python-decouple for `.env` management

## Prerequisites

- Python 3.10 or higher
- PostgreSQL
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Crime-Reporting-System.git
cd Crime-Reporting-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials and a secret key:

```
DJANGO_SECRET_KEY=your-secure-random-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=crs_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE crs_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crs_db TO your_db_user;
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Seed the database (optional)

Populates the database with 12 police stations across Nepal and 120 realistic crime reports:

```bash
python manage.py seed_data
```

### 8. Create a superuser (admin/police account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set email, name, and password.

### 9. Run the development server

```bash
python manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) to access the application.

## Project Structure

```
Crime-Reporting-System/
├── .env                        # Environment variables (not committed)
├── .env.example                # Environment template
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── crs/                        # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── report/                     # Core crime reporting app
│   ├── models.py               # CrimeReport, PoliceStation models
│   ├── views.py                # All views + analytics API
│   ├── forms.py                # Report creation and update forms
│   ├── urls.py                 # URL routing
│   ├── algorithms.py           # Nearest police station (Haversine)
│   ├── management/commands/
│   │   └── seed_data.py        # Database seeding command
│   └── templates/              # HTML templates
├── user_management/            # User registration and auth
│   ├── models.py               # Custom User model (email-based)
│   ├── views.py                # Register, logout views
│   └── templates/
├── templates/                  # Global templates
│   ├── base.html
│   └── navbar.html
├── static/                     # CSS, JS, images, fonts
└── mediafiles/                 # Uploaded proof documents
```

## URL Routes

### Public Pages

| URL | Description |
|-----|-------------|
| `/` | Home page — recent public crime reports |
| `/reports/` | Submit a new crime report |
| `/contact-details/` | Look up your reports by email + phone |

### Authenticated Pages

| URL | Description |
|-----|-------------|
| `/admin/login/` | Police portal login |
| `/users/register/` | Police officer registration |
| `/reports/update/<id>/` | Update a crime report |
| `/reports/delete/<id>/` | Delete a crime report |

### Admin & API

| URL | Description |
|-----|-------------|
| `/admin/` | Django admin panel |
| `/admin/analytics-data/` | Analytics JSON API (staff only) |

## How It Works

### Citizen Flow
1. A citizen visits the home page and clicks **Report a Crime**
2. They fill in their name, email, phone, incident details, and optionally attach proof
3. The system auto-assigns the nearest police station based on their geolocation
4. The report is saved with **Pending** status
5. The citizen can track their reports anytime using their email and phone number

### Police Flow
1. A police officer registers and logs in through the Police Portal
2. They can view all reports assigned to their station
3. They can update the report status (Pending → Investigating → Action Taken)
4. They can add an official explanation/response to the report
5. The analytics dashboard provides station-wise and time-wise breakdowns

## Haversine Algorithm — Auto-Assigning Nearest Police Station

### Why is it used?

When a citizen submits a crime report, the system needs to automatically assign it to the **nearest police station** based on the citizen's location. Instead of asking the user to manually select a station (which they may not know), the system captures their geolocation via the browser and uses the **Haversine formula** to calculate the closest station.

### How does it work?

The Haversine formula calculates the **great-circle distance** between two points on a sphere (Earth) given their latitude and longitude:

```
d = 2 * R * arcsin( sqrt( sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2) ) )
```

Where:
- `d` = distance between the two points (in kilometers)
- `R` = radius of Earth (6,371 km)
- `lat1, lon1` = coordinates of the citizen's location
- `lat2, lon2` = coordinates of a police station

**Step-by-step process:**

1. Citizen opens the report form — the browser requests geolocation permission
2. On grant, JavaScript captures `latitude` and `longitude` and stores them in hidden form fields
3. On form submission, `nearest_police_station()` in `report/algorithms.py` is called
4. It fetches all `PoliceStation` records from the database
5. It runs the Haversine formula against every station to compute distances
6. The station with the **minimum distance** is selected and assigned to the report

### How it helps the system

- **No manual selection needed** — citizens don't need to know which police station covers their area
- **Automatic routing** — reports are directed to the correct station immediately
- **Accuracy** — uses real GPS coordinates for precise distance calculation
- **Scales well** — adding new police stations automatically includes them in the assignment logic

### Implementation

The algorithm lives in `report/algorithms.py`:

```python
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def nearest_police_station(user_lat, user_lon):
    stations = PoliceStation.objects.all()
    nearest_station = min(
        stations,
        key=lambda station: haversine(Decimal(user_lat), Decimal(user_lon),
                                       station.latitude, station.longitude)
    )
    return nearest_station
```

Called from `ReportCreationForm.save()` in `report/forms.py` during report creation.

## Seed Data

The `seed_data` management command populates the database with:

- **12 Police Stations** across Nepal (Kathmandu, Lalitpur, Bhaktapur, Pokhara, Biratnagar, Birgunj, Butwal, Dharan, Hetauda, Nepalgunj, Janakpur, Itahari)
- **120 Crime Reports** (10 per station) with realistic incident types including robbery, domestic violence, theft, hit and run, cyber fraud, assault, shoplifting, drug possession, and more

Run anytime to re-seed (clears existing data first):

```bash
python manage.py seed_data
```
