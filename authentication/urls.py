from django.urls import path
from authentication import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="auth_login"),
    path("userinfo/", views.UserInfoView.as_view(), name="auth_userinfo"),
]
