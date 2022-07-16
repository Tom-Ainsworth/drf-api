from django.db import IntegrityError
from .models import Like
from rest_framework import serializers


class LikeSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Like
        fields = [
            "id",
            "owner",
            "post",
            "created_at",
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "possible duplicate"})
