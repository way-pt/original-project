from rest_framework import serializers

from core.models import Map

class MapSerializer(serializers.Serializer):

    class Meta:
        model = Map
        fields = ['name', 'user', 'data', 'image']

    def get_user_username(self, obj):
        return obj.user.get_username()
