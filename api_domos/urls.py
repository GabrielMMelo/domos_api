from rest_framework import routers

from rest_auth.registration.views import VerifyEmailView, RegisterView
from allauth.account.views import confirm_email

from django.contrib import admin
from django.urls import include, path, re_path

from device.viewsets import DeviceViewSet
from place.viewsets import PlaceViewSet

from core.views import ConfirmEmailView

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
auth = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]

api_v1 = [
    path('', include((router.urls, 'api'))),
    path('auth/', include(auth))
]

urlpatterns = [
    path('api/v1/', include(api_v1)),
    path('admin/', admin.site.urls),
    #TODO: change the route in email template
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
        name='account_email_verification_sent'),
]
