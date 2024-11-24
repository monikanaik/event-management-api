from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    RegisterUserView,
    EventListCreateView,
    TicketPurchaseView,
)

urlpatterns = [
    # User registration
    path("register/", RegisterUserView.as_view(), name="register"),
    # Event management
    path("event/", EventListCreateView.as_view(), name="event"),
    path(
        "event/<int:id>/purchase/", TicketPurchaseView.as_view(), name="event_purchase"
    ),
    # JWT authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
