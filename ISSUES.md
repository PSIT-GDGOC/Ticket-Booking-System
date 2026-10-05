# Project Issues

Copy each issue into GitHub (**Issues → New issue**). Suggested labels are shown for each.

**Labels to create:** `setup`, `backend`, `feature`, `enhancement`, `bug`, `testing`, `ui`, `documentation`

---

## 1. Set up Django project structure

**Label:** `setup`

**Description:**
Initialize the Django project and apps.

**Tasks:**
- [ ] Create virtual environment and install Django
- [ ] Create project `config` and apps `users`, `events`, `bookings`
- [ ] Add `requirements.txt` and `.env.example`
- [ ] Configure settings to read secrets from `.env`

---

## 2. Design database models

**Label:** `backend`

**Description:**
Define the core models and relationships.

**Tasks:**
- [ ] Create `Event`, `Seat`, `Booking`, `BookingSeat` models
- [ ] Add status fields (available / booked, confirmed / cancelled)
- [ ] Run migrations
- [ ] Register models in the admin panel

---

## 3. Implement user registration

**Label:** `feature`

**Description:**
Allow new users to create an account.

**Tasks:**
- [ ] Registration form with name, email, password
- [ ] Validate duplicate emails and weak passwords
- [ ] Redirect to login after signup

---

## 4. Implement login and logout

**Label:** `feature`

**Description:**
Allow users to log in and out securely.

**Tasks:**
- [ ] Login page with error messages
- [ ] Logout button in navbar
- [ ] Protect booking pages with `login_required`

---

## 5. Create event listing page

**Label:** `feature`

**Description:**
Show all upcoming events on the home page.

**Tasks:**
- [ ] Display title, venue, date and price
- [ ] Show only upcoming events
- [ ] Add pagination

---

## 6. Add event search and filters

**Label:** `enhancement`

**Description:**
Help users find events quickly.

**Tasks:**
- [ ] Search by title or venue
- [ ] Filter by date and price
- [ ] Show a message when no results are found

---

## 7. Create event detail page with seat layout

**Label:** `feature`

**Description:**
Show event info and available seats.

**Tasks:**
- [ ] Display seat grid with available / booked states
- [ ] Allow selecting multiple seats
- [ ] Show the total price live

---

## 8. Implement seat booking

**Label:** `feature`

**Description:**
Let logged-in users book selected seats.

**Tasks:**
- [ ] Create booking and link selected seats
- [ ] Mark seats as booked
- [ ] Show a confirmation page

---

## 9. Prevent double booking of seats

**Label:** `bug`

**Description:**
Two users must not be able to book the same seat at the same time.

**Tasks:**
- [ ] Use `transaction.atomic()` with `select_for_update()`
- [ ] Re-check seat status before saving
- [ ] Show a friendly error if the seat was just taken
- [ ] Add a test for concurrent booking

---

## 10. Add My Bookings page

**Label:** `feature`

**Description:**
Users can view their booking history.

**Tasks:**
- [ ] List bookings with event, seats, amount and status
- [ ] Order by most recent first
- [ ] Link each booking to its detail page

---

## 11. Implement booking cancellation

**Label:** `feature`

**Description:**
Users can cancel a booking and free the seats.

**Tasks:**
- [ ] Add a cancel button with confirmation
- [ ] Set booking status to cancelled
- [ ] Release seats back to available
- [ ] Block cancellation after the event date

---

## 12. Customize Django admin panel

**Label:** `enhancement`

**Description:**
Make it easy for admins to manage data.

**Tasks:**
- [ ] Add list display, filters and search for events and bookings
- [ ] Add bulk action to generate seats for an event

---

## 13. Add email confirmation for bookings

**Label:** `enhancement`

**Description:**
Send an email after a successful booking.

**Tasks:**
- [ ] Configure SMTP settings via `.env`
- [ ] Create an email template with booking details
- [ ] Send the email after booking is confirmed

---

## 14. Integrate online payment

**Label:** `enhancement`

**Description:**
Accept payments using Razorpay or Stripe in test mode.

**Tasks:**
- [ ] Create a payment model and checkout flow
- [ ] Verify payment before confirming the booking
- [ ] Handle failed and cancelled payments

---

## 15. Generate PDF ticket with QR code

**Label:** `enhancement`

**Description:**
Provide a downloadable ticket for each booking.

**Tasks:**
- [ ] Generate a unique QR code per booking
- [ ] Create a PDF ticket with event and seat info
- [ ] Add a download button on the booking page

---

## 16. Write unit tests

**Label:** `testing`

**Description:**
Add tests for core features.

**Tasks:**
- [ ] Test models and booking logic
- [ ] Test views and permissions
- [ ] Aim for tests on registration, booking and cancellation

---

## 17. Improve UI with Bootstrap

**Label:** `ui`

**Description:**
Make the interface clean and responsive.

**Tasks:**
- [ ] Add a base template with navbar and footer
- [ ] Make pages mobile friendly
- [ ] Style the seat selection grid

---

## 18. Add screenshots and finalize README

**Label:** `documentation`

**Description:**
Complete project documentation.

**Tasks:**
- [ ] Add screenshots to `screenshots/`
- [ ] Update URL routes and setup steps
- [ ] Verify installation steps on a fresh machine

---

