from django.conf.urls import url, include
from assets import models
from rest_framework import routers, serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('name', 'username', 'email', 'is_staff')


# class AssetSerializer(serializers.HyperlinkedModelSerializer):
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = ('id', 'asset_type', 'sn', 'business_unit','management_ip')

