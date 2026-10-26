# Ticketly — Ticket Booking System

Ticketly is a Django application for discovering events, reserving seats, and managing bookings.

## Features

- Browse active events and view their details.
- Reserve one or more seats with database-backed double-booking prevention.
- Cancel a booking to release its seats.
- Receive booking-confirmation emails after a successful transaction.
- Manage events, seats, bookings, and booking seats in Django admin at `/admin/`.

## Tech stack

- Python 3.12+
- Django 6.1.2
- SQLite for local development
- Django templates, HTML, CSS, and JavaScript
- `python-dotenv` for local environment variables

## Project structure

```text
Ticket-Booking-System/
├── Backend/
│   ├── manage.py                 # Django command-line entry point
│   ├── requirements.txt          # Backend dependencies
│   ├── .env.example              # Safe environment-variable template
│   ├── config/                   # Settings and project URL routes
│   ├── events/                   # Events and seats
│   ├── bookings/                 # Booking, cancellation, and email logic
│   └── users/                    # User application
├── Frontend/
│   ├── templates/                # HTML templates
│   └── static/                   # CSS, JavaScript, and images
├── LICENSE
└── README.md
```

`Backend/.env` and `Backend/db.sqlite3` are local files and should not be committed.

## Setup

Run the following from the repository root.

### 1. Clone the repository

```bash
git clone https://github.com/ShreyanshFS/Ticket-Booking-System.git
cd Ticket-Booking-System
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r Backend/requirements.txt
```

### 4. Configure local environment variables

Windows PowerShell:

```powershell
Copy-Item Backend/.env.example Backend/.env
```

macOS/Linux:

```bash
cp Backend/.env.example Backend/.env
```

Email delivery is optional in local development. Leave `EMAIL_HOST` empty to use Django's console email backend, or add SMTP values to `Backend/.env`. Do not commit that file or real credentials.

### 5. Migrate and run

```bash
cd Backend
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

## Tests and checks

Run these from `Backend/` while the virtual environment is active:

```bash
python manage.py check
python manage.py test
python manage.py test bookings
```

The email tests use Django's in-memory test mailbox and never send real messages.

## Routes

| Route | Description |
| --- | --- |
| `/` | Active event listing |
| `/events/<event_id>/` | Event details and seat booking |
| `/book/<event_id>/` | Create a booking (POST) |
| `/cancel/<booking_id>/` | Cancel the signed-in user's booking (POST) |
| `/admin/` | Django admin |

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`.
2. Make and test your changes.
3. Commit with a clear message.
4. Push the branch and open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
