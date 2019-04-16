from rest_framework import routers
from assets import rest_viewset
from django.conf.urls import url,include


router=routers.DefaultRouter()
router.register(r'users',rest_viewset.UserViewSet)
router.register(r'assets',rest_viewset.AssetViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]