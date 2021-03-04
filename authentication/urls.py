from django.urls import path
from .views import RegisterView, LoginView, VerifyEmail, LogoutAPIView, PasswordTokenCheckAPI, ShowUsersAPIView, \
    SetNewPasswordAPIView, RequestPasswordResetEmail

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset',
         PasswordTokenCheckAPI.as_view(), name='password-reset'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('users/', ShowUsersAPIView.as_view(), name='users'),
]
