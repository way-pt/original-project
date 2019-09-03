from rest_framework import serializers

from core.models import Map

class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ['name', 'user', 'data', 'image']
 
