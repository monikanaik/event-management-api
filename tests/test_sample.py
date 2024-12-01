import pytest
from rest_framework import status
from api.models import User
from api.views import get_lazy_loading
from eventapi.settings import local


@pytest.fixture(scope="session")
def django_db_setup():
    local.DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "db.example.com",
        "NAME": "external_db",
    }


@pytest.mark.django_db
def test_my_user():
    user = User.objects.create_superuser("Mouni@12")
    me = User.objects.get(username=user)
    assert me.is_superuser
