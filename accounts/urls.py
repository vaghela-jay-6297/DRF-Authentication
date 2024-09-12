from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import RegisterAPIView, LoginAPIView, MyProfileAPIView, UserViewSet, ChangePasswordAPIView

router = DefaultRouter()
router.register('user', UserViewSet, basename="user_update")  # list of all users

urlpatterns = [
    # JWT token authentication.
    # path('auth-jwt/', TokenObtainPairView.as_view(), name='token_obtain'), # get jwt token with passing username & password.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # get refresh token or get new updated access token
    # path('token-verify/', TokenVerifyView.as_view(), name='token_verify'), # to verify token

    path('register/', RegisterAPIView.as_view(), name='RegisterView'),
    path('login/', LoginAPIView.as_view(), name='LoginView'),
    path('me/', MyProfileAPIView.as_view(), name='MyProfileView'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='ChangePasswordAPIView'),
    path('', include(router.urls)),
]
