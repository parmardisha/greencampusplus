# GreenPulse

GreenPulse is a small Flask app for logging everyday activities and viewing
their estimated greenhouse-gas emissions.

## Run locally

Python 3.9 or newer is recommended.

```powershell
cd greenpulse
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The SQLite database, `greenpulse.db`, is created
automatically beside `app.py` on first run.

## How estimates work

Each activity is multiplied by a fixed emissions factor in
`sustainability.py`. Factors are indicative kg CO2e per kWh or km, not a
personalized lifecycle assessment; actual emissions vary by location, energy
mix, vehicle, and other conditions.

## API

- `GET /api/dashboard` — summary, recent activities, and supported categories.
- `POST /api/activities` — add an activity with JSON fields `description`,
  `category`, and `amount`.
- `DELETE /api/activities/<id>` — remove an activity.
