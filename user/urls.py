from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_get, name="register"),
    path('register/treat-data/', views.register_post, name="treat_data"),
    path('my-profile/', views.my_profile, name="my-profile"),
    path('login/', views.login_user, name="login"),
    path('login/treat-data', views.treat_post_login, name="treat-login"),
    path('logout/', views.logout_user, name="logout"),
]
