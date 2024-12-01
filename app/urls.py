from django.urls import path

from app.views import (
    CreateAPIView,
    UserRetrieveUpdateDeleteView,
    EventAPIViews,
    EventRetrieveUpdateDeleteView,
    EventAPIViewAdmin,
)

urlpatterns = [
    path("user_register/", CreateAPIView.as_view(), name="user_register"),
    path("user/<int:pk>/", UserRetrieveUpdateDeleteView.as_view(), name="user-detail"),
    path("event/", EventAPIViews.as_view(), name="event"),
    path(
        "event/<int:pk>/",
        EventRetrieveUpdateDeleteView.as_view(),
        name="event-detail",
    ),
    path("events/", EventAPIViewAdmin.as_view(), name="events"),
]
