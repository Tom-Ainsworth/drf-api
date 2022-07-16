from django.db import IntegrityError
from .models import Follower
from rest_framework import serializers


class FollowerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = [
            "id",
            "owner",
            "created_at",
            "followed",
            "followed_name",
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "possible duplicate"})