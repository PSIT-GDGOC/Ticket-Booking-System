# Ticketly - Ticket Booking System

Ticketly is a Django application for discovering events and viewing event details. The project also contains the booking data model and booking-confirmation email flow that will support the next stage of the product.

## Current status

- The home page lists active events and supports search and category-style filtering in the browser.
- Event detail pages show the event description, date, time, venue, and price.
- Booking models and confirmation-email logic are present in the backend.
- The booking button is not connected to a booking form yet; it currently displays `Booking coming soon`.
- Payment integration is not implemented.

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
│   ├── config/
│   │   ├── settings.py           # Django settings and email configuration
│   │   ├── urls.py               # Project URL routes
│   │   ├── asgi.py               # ASGI entry point
│   │   └── wsgi.py               # WSGI entry point
│   ├── events/
│   │   ├── migrations/           # Event and seat migrations
│   │   ├── models.py             # Event and Seat models
│   │   ├── views.py              # Event page views
│   │   └── admin.py              # Event admin configuration
│   ├── bookings/
│   │   ├── migrations/           # Booking migrations
│   │   ├── models.py             # Booking and BookingSeat models
│   │   ├── emails.py             # Booking-confirmation email helpers
│   │   ├── signals.py            # Sends confirmations after commit
│   │   ├── test_emails.py        # Email-flow tests
│   │   └── templates/bookings/email/
│   │       ├── booking_confirmation.html
│   │       └── booking_confirmation.txt
│   └── users/
│       ├── migrations/
│       ├── models.py
│       ├── views.py
│       └── admin.py
├── Frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── event_detail.html
│   └── static/
│       └── style.css
├── .gitignore
├── LICENSE
└── README.md
```

`Backend/.env` and `Backend/db.sqlite3` are local files. They are not part of the setup tree and should not be committed.

## Setup

### Prerequisites

- Python 3.12 or newer
- Git
- PowerShell on Windows, or a POSIX-compatible shell on macOS/Linux

### 1. Clone the repository

```bash
git clone <repository-url>
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

### 3. Install backend dependencies

Run this from the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -r Backend/requirements.txt
```

### 4. Create the local environment file

Windows PowerShell:

```powershell
Copy-Item Backend/.env.example Backend/.env
```

macOS/Linux:

```bash
cp Backend/.env.example Backend/.env
```

Edit `Backend/.env` before enabling email delivery. The project loads this file automatically from the `Backend/` directory.

### 5. Create the database

Change into the directory containing `manage.py`, then apply the existing migrations:

```bash
cd Backend
python manage.py migrate
```

The local SQLite database starts empty. No event seed data is included, so event records must be added before the home page can display event cards.

### 6. Start the development server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

## Email configuration

Email delivery is optional during local development.

- Leave `EMAIL_HOST` empty to use Django's console email backend. Messages are printed in the server terminal.
- Set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and the TLS/SSL options to use an SMTP provider.
- For Gmail, use an app password rather than your regular account password.
- Set `DEFAULT_FROM_EMAIL` to an address accepted by the SMTP provider.

Example values are documented in `Backend/.env.example`. Never commit `Backend/.env` or place real credentials in documentation.

## Tests and checks

Run these commands from `Backend/` while the virtual environment is active:

```bash
python manage.py check
python manage.py test
```

The email tests use Django's in-memory test mailbox; they do not send messages to real recipients.

## Current routes

| Route | Description |
| --- | --- |
| `/` | Active event listing |
| `/events/<event_id>/` | Event details |

The booking UI and Django admin route are not currently connected in `Backend/config/urls.py`.

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make and test your changes.
3. Commit with a clear message.
4. Push the branch and open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

SUNSTUTI SRIVASTAVA
GitHub: [@sunstutisrivastava-bit](https://github.com/sunstutisrivastava-bit)
