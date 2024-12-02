from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    RegisterUserView,
    EventListCreateView,
    TicketPurchaseView,
    get_lazy_loading,
    get_select_related,
)

urlpatterns = [
    # User registration
    path("register/", RegisterUserView.as_view(), name="register"),
    # Event management
    path("event/", EventListCreateView.as_view(), name="event"),
    path(
        "event/<int:id>/purchase/",
        TicketPurchaseView.as_view(),
        name="event_purchase",
    ),
    # JWT authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("lazy-loading/", get_lazy_loading, name="lazy_loading_view"),
    path("select-related/", get_select_related, name="select_related_view"),
]
