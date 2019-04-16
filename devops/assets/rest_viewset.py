from rest_framework import viewsets
from assets import models
from assets import rest_searializer
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = rest_searializer.UserSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = rest_searializer.AssetSerializer