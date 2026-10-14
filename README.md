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
- Email confirmation and payment integration (planned)

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
ticket-booking-system/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── config/          # Project settings and main URLs
├── users/           # Registration, login, profile
├── events/          # Events and seats
├── bookings/        # Booking and cancellation logic
├── templates/       # HTML templates
└── static/          # CSS, JS, images
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/ticket-booking-system.git
cd ticket-booking-system

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env           # Windows: copy .env.example .env
# then edit .env with your own values

# 5. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
Admin panel: http://127.0.0.1:8000/admin/

## Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=ticket_booking
DB_USER=your_user
DB_PASSWORD=your_password
```

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
