from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_get, name="register"),
    path('register/treat-data/', views.register_post, name="treat_data"),
    path('my-profile/', views.my_profile, name="my-profile"),
]
