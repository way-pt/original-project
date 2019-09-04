from rest_framework import serializers

from core.models import Map

class MapSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    class Meta:
        model = Map
        fields = ['name', 'user_username', 'user', 'data', 'image', 'pk']
 
    def get_user_username(self, obj):
        return obj.user.get_username()
