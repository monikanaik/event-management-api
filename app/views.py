from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.models import User, Event
from app.serializers import UserSerializers, EventSerializers
from rest_framework.views import APIView

# Create your views here.
"""
class CreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow anyone to access

"""


class CreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow anyone to access

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetrieveUpdateDeleteView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow anyone to access

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""
Event Management (Admin Only):
POST /api/events/ - Create a new event (Admin only).
GET /api/events/ - Fetch all events (Admin and User)
"""


class EventAPIViews(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow anyone to access

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventRetrieveUpdateDeleteView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventAPIViewAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admins can create events."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EventSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
