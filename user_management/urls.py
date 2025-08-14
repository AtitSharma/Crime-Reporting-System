from django.urls import path
from user_management.views import LogOutView, UserRegisterView,LoginUserView


app_name = "ums"



urlpatterns = [
    path("register/",UserRegisterView.as_view(),name="register"),
    # path("login/",LoginUserView.as_view(),name="login"),
    path("logout/",LogOutView.as_view(),name="logout")
]
