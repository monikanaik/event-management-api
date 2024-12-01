from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    RegisterUserView,
    EventListCreateView,
    TicketPurchaseView,
    even_list,
    event_user_detail,
    # customers,
    CustomersView,
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
    path("test/", even_list),
    path(
        "event/<int:event_id>/user/<str:username>/",
        event_user_detail,
        name="event_user_detail",
    ),
    path("name/", CustomersView.as_view()),
    path("lazy/", get_lazy_loading),
    path("select_related/", get_select_related),
]
