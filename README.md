# Event Management API

This project is a Django-based REST API for managing events and ticket purchases. It supports role-based access control with **Admin** and **User** roles.

---
## Installation Instructions

### 1. Clone the repository:
```bash
git clone <repository_url>
cd event-management-api
```
### 2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies:
```bash
pip install -r requirements.txt
```
### 4. Set up the database:
```bash
    Update the database settings in settings.py.
```
### 5. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Run the server:
```bash
python manage.py runserver
```
### Usage Instructions
* Use Postman or any other API client to interact with the API endpoints.
* Authenticate users by obtaining and passing JWT tokens in the Authorization header.
### Folder Structure
```
event-management-api/
├── api/
│   ├── models.py          # Models: User, Event, Ticket
│   ├── views.py           # API logic
│   ├── serializers.py     # Serializers for request/response
│   ├── urls.py            # API routing
├── manage.py              # Django management script
├── settings.py            # Project settings
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```
---
### Notes and Considerations
1. The system ensures role-based access for Admin and User actions.
2. Error handling is implemented for edge cases, such as non-existent events or invalid ticket requests.
3. JWT-based authentication provides secure access to the API.
