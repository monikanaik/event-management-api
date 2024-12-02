from rest_framework.serializers import ModelSerializer
from api.models import User, Event, Ticket


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
