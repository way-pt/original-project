from rest_framework import serializers

from core.models import Map

class MapSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    # data_url = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ['name', 'user_username', 'user', 'img_url', 'date', 'pk']
 
    def get_user_username(self, obj):
        return obj.user.get_username()

    def get_img_url(self, obj):
        return obj.image.url

    # def get_data_url(self, obj):
    #     return obj.data.url
