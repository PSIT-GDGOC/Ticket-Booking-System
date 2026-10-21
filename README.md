# 🎟️ Ticket Booking System

A Python/Django web application where users can browse events, select seats, book and cancel tickets, and view their booking history. Admins can manage events, seats, and bookings from the Django admin panel.

## Features

- User registration, login, and logout
- Browse and search events
- Seat selection with live availability
- Book and cancel tickets
- Booking history for each user
- Double-booking prevention using database transactions
- Admin panel to manage events, seats, and bookings
- Email confirmation after a successful booking
- Payment integration (planned)

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Language  | Python 3.10+                        |
| Framework | Django                              |
| Database  | SQLite (development), PostgreSQL/MySQL (production) |
| Frontend  | HTML, CSS, Bootstrap, JavaScript    |
| Tools     | Git, GitHub, Postman                |

## Project Structure

```
Ticket-Booking-System/
├── Backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/      # Project settings and main URLs
│   ├── users/       # Registration, login, profile
│   ├── events/      # Events and seats
│   └── bookings/    # Booking, cancellation and confirmation emails
├── Frontend/
│   ├── templates/   # HTML templates
│   └── static/      # CSS, JS, images
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ShreyanshFS/Ticket-Booking-System.git
cd Ticket-Booking-System

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r Backend/requirements.txt

# 4. Move into the Django project (run all manage.py commands from here)
cd Backend

# 5. Set up environment variables
copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux
# then edit .env with your own values

# 6. Apply database migrations
python manage.py migrate

# 7. Create an admin user
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
Admin panel: http://127.0.0.1:8000/admin/

### Verify the setup (optional)

Run these from the `Backend/` folder:

```bash
python manage.py check
python manage.py test
```

## Environment Variables

Copy `Backend/.env.example` to `Backend/.env` (next to `manage.py`) and fill in your values. Only email is configured through `.env`:

```
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_TIMEOUT=10
DEFAULT_FROM_EMAIL=Ticketly <no-reply@example.com>
```

Leave `EMAIL_HOST` empty in development: booking confirmation emails are then printed to the console instead of being sent.

Never commit your `.env` file.

## Usage

1. Register a new account or log in.
2. Browse the list of events.
3. Open an event and choose your seats.
4. Confirm the booking.
5. View or cancel bookings from **My Bookings**.

Admins can log in at `/admin/` to add events, set seat layouts, and manage all bookings.

## Database Design

| Table         | Key Fields                                              |
|---------------|---------------------------------------------------------|
| User          | id, name, email, password, role                         |
| Event         | id, title, description, venue, date_time, price         |
| Seat          | id, event, seat_number, status                          |
| Booking       | id, user, event, total_amount, status, created_at       |
| BookingSeat   | booking, seat                                           |
| Payment       | id, booking, amount, status, method                     |

## URL Routes (example)

| URL                      | Description              |
|--------------------------|--------------------------|
| `/`                      | Home / event list        |
| `/register/`             | User registration        |
| `/login/`                | User login               |
| `/events/<id>/`          | Event details and seats  |
| `/book/<event_id>/`      | Book seats               |
| `/my-bookings/`          | Booking history          |
| `/cancel/<booking_id>/`  | Cancel a booking         |
| `/admin/`                | Admin panel              |

## Screenshots

Add screenshots of your app here:

```
![Home Page](screenshots/home.png)
![Seat Selection](screenshots/seats.png)
```

## Future Improvements

- Online payment (Razorpay / Stripe)
- Email and SMS confirmations
- QR code tickets and PDF download
- REST API with Django REST Framework
- Event categories and filters

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

SUNSTUTI SRIVASTAVA
GitHub: [@sunstutisrivastava-bit](https://github.com/sunstutisrivastava-bit)
