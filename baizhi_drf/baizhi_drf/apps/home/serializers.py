from rest_framework.serializers import ModelSerializer

from home.models import Banner, Navigation


class BnnerModelSerializer(ModelSerializer):
    class Meta:
        model = Banner
        # fiels = ('image','title','link')
        fields = '__all__'

class NavModelSerializer(ModelSerializer):
    class Meta:
        model = Navigation
        fields = ('title','link','position')