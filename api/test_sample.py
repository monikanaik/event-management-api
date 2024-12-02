import json

import pytest
import requests
from rest_framework import status
from django.conf import settings
from django.urls import resolve
from api.models import User  # Ensure the correct User model is being imported
from api.serializers import UserSerializer
from api.models import Event
from rest_framework.test import APIClient
from django.test import TestCase
from django.test.client import Client
from api.models import Ticket, User, Event
from django.urls import reverse
from api.views import top_3_events_by_tickets_sold


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_password",
        "HOST": "localhost",
        "PORT": "3306",
        "ATOMIC_REQUESTS": True,  # Add this key here
    }


# Test case for creating and retrieving a superuser
@pytest.mark.django_db
def test_my_user():
    # Create a superuser
    user = User.objects.create_superuser(username="Mouni@12", password="password123")
    # Retrieve the user
    retrieved_user = User.objects.get(username=user.username)
    # Assert the user is a superuser
    assert retrieved_user.is_superuser


@pytest.mark.django_db
def test_user_serializer_create():
    data = {
        "username": "test_user",
        "password": "password123",
        "role": "user",
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()

    # Verify the user is created correctly
    assert user.username == "test_user"
    assert user.check_password("password123")
    assert user.role == "user"


# Define the endpoint URL
USER_ENDPOINT = "/api/register/"


@pytest.mark.django_db
class TestRegisterUserView:
    def setup_method(self):
        self.client = APIClient()

    def test_user_registration_successful(self):
        """
        Test that a user can register successfully with valid data.
        """
        data = {
            "username": "testuser",
            "password": "password123",
            "role": "admin",
        }
        response = self.client.post(USER_ENDPOINT, data)

        # Assert the response status code
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["username"] == "testuser"

        # Assert the user is created in the database
        assert User.objects.filter(username="testuser").exists()

    def test_user_registration_missing_fields(self):
        """
        Test that registration fails with missing required fields.
        """
        data = {"username": "testuser"}
        response = self.client.post(USER_ENDPOINT, data)

        # Assert the response status code
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data  # Password is required

    def test_user_list_successful(self):
        """
        Test that the API returns a list of users.
        """
        # Make a GET request
        response = self.client.get(USER_ENDPOINT)

        # Assert the response status code
        assert response.status_code == status.HTTP_200_OK

        # Sort the response data by username
        sorted_response_data = sorted(response.data, key=lambda x: x["username"])

        # Assert the correct number of users are returned
        assert sorted_response_data
        assert sorted_response_data[0]["username"] == "Admin"
        assert sorted_response_data[1]["username"] == "abell"


'''
@pytest.mark.django_db
class ObtainJSONWebTokenTestCase(TestCase):
    def setUp(self):
        self.username = "jpueblo"
        self.password = "password"
        self.role = "admin"
        self.user = User.objects.create_user(
            username=self.username, password=self.password, role=self.role
        )

        self.data = {"username": self.username, "password": self.password}
        self.client = APIClient()

    def test_jwt_login_json(self):
        """
        Ensure JWT login view using JSON POST works.
        """
        print(f"DEBUG: APPEND_SLASH = {settings.APPEND_SLASH}")
        print(f"DEBUG: Resolved URL = {resolve('/api/token/')}")
        url = "/api/token/"  # Ensure this has a trailing slash
        response = self.client.post(
            url, data=json.dumps(self.data), content_type="application/json"
        )

        # Debugging output
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.content}")

        # Assert the response status code is 200
        self.assertEqual(
            response.status_code, 200, "Expected status code 200 for successful login"
        )

        # Assert that the token is present in the response
        response_data = json.loads(response.content)
        token = response_data.get("access")
        self.assertIsNotNone(token, "Access token not returned in response")

'''


@pytest.mark.django_db
def get_auth_token():
    """
    Helper function to obtain a JWT token for authentication.
    """
    username = "jpueblo"
    password = "password"
    role = "admin"

    # Create a user
    User.objects.create_user(username=username, password=password, role=role)

    client = APIClient()
    url = "/api/token/"  # Ensure this has a trailing slash
    data = {"username": username, "password": password}

    # Send login request to obtain token
    response = client.post(url, data=json.dumps(data), content_type="application/json")

    # Debugging output
    print(f"DEBUG: APPEND_SLASH = {settings.APPEND_SLASH}")
    print(f"DEBUG: Resolved URL = {resolve('/api/token/')}")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.content}")

    assert (
        response.status_code == status.HTTP_200_OK
    ), "Expected status code 200 for successful login"

    # Extract and return the token
    response_data = json.loads(response.content)
    token = response_data.get("access")
    assert token is not None, "Access token not returned in response"
    return token


@pytest.mark.django_db
def test_event_list():
    """
    Test the Event list endpoint with authentication.
    """
    # Obtain a valid token
    token = get_auth_token()

    # Use APIClient and set the token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Create a sample event
    Event.objects.create(
        name="Bug Report",
        date="2024-12-01",
        total_tickets=2,
        tickets_sold=100,
    )

    # Send GET request to fetch events
    response = client.get("/api/event/")

    # Debugging output
    print(f"Event list response: {response.content}")

    # Assert the response
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Expected status code 200 for the event list"
    assert response.content, "Expected one event in the response"


@pytest.mark.django_db
def test_top_3_events_by_tickets_sold():
    # Create test data
    Event.objects.create(
        name="Event A",
        date="2024-12-01",
        total_tickets=200,
        tickets_sold=50,
    )
    Event.objects.create(
        name="Event B",
        date="2024-12-02",
        total_tickets=300,
        tickets_sold=150,
    )
    Event.objects.create(
        name="Event C",
        date="2024-12-03",
        total_tickets=400,
        tickets_sold=250,
    )
    Event.objects.create(
        name="Event D",
        date="2024-12-04",
        total_tickets=500,
        tickets_sold=100,
    )
    Event.objects.create(
        name="Event E",
        date="2024-12-05",
        total_tickets=600,
        tickets_sold=300,
    )

    # Call the function
    result = top_3_events_by_tickets_sold()

    # Assert the results
    # assert len(result) == 3  # Ensure only top 3 events are returned
    assert result[0]["name"] == "Event E"  # Most tickets sold
    assert result[1]["name"] == "Event C"
    assert result[2]["name"] == "Event B"

    # Assert tickets sold are in descending order
    tickets_sold = [event["tickets_sold"] for event in result]
    assert tickets_sold == sorted(tickets_sold, reverse=True)


@pytest.mark.django_db
def test_get_lazy_loading(client):
    # Create test data
    user = User.objects.create(username="testuser", role="admin", password="testpass")
    event = Event.objects.create(
        name="Test Event",
        date="2024-12-01",
        total_tickets=100,
        tickets_sold=50,
    )
    Ticket.objects.create(
        user=user,
        event=event,
        quantity=2,
        purchase_date="2024-11-30",
    )

    # Call the lazy-loading view
    response = client.get(
        reverse("lazy_loading_view"),
    )  # Replace with the actual name of the URL route
    assert response.status_code == 200
    assert response.content == b"hello"


@pytest.mark.django_db
def test_get_select_related(client):
    # Create test data
    user = User.objects.create(username="testuser", role="admin", password="testpass")
    event = Event.objects.create(
        name="Test Event",
        date="2024-12-01",
        total_tickets=100,
        tickets_sold=50,
    )
    Ticket.objects.create(
        user=user,
        event=event,
        quantity=2,
        purchase_date="2024-11-30",
    )

    # Call the view
    response = client.get(reverse("select_related_view"))

    # Debugging response content
    print(f"Response content:\n{response.content.decode()}")

    # Verify the response
    assert response.status_code == 200
    assert response.content
