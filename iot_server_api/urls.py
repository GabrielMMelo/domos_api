from rest_framework import routers

from django.contrib import admin
from django.urls import include, path

from device.viewsets import DeviceViewSet
from place.viewsets import PlaceViewSet

router = routers.DefaultRouter()
router.register('device', DeviceViewSet, base_name='Device')
router.register('place', PlaceViewSet, base_name='Place')
"""
rest_auth = [
    path('login', LoginViewAdapter.as_view(), name="user-login"),
    path('logout', LogoutView.as_view(), name='user-logout'),
    path('password/change',
         PasswordChangeView.as_view(),
         name='rest_password_change'),
    path('password/reset',
         PasswordResetView.as_view(),
         name='rest_password_reset'),
    path('password/reset/confirm',
         PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
]
"""

api_v1 = [
    path('', include((router.urls, 'api'))),
    path('auth/', include('rest_auth.urls'))
]

urlpatterns = [
    path('api/v1/', include(api_v1)),
    path('admin/', admin.site.urls),
]
