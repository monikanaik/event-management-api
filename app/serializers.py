from rest_framework.serializers import ModelSerializer

from app.models import User, Event


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        return user


class EventSerializers(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
