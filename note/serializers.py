from rest_framework import serializers
from users import serializers as user_serializer
from . import services


class NoteSeralizer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateTimeField()
    priority = serializers.IntegerField()
    is_complete = serializers.BooleanField()
    is_email_send = serializers.BooleanField()
    user = user_serializer.UserSerializer(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.NoteDataClass(**data)
