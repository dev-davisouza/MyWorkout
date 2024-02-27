from django.urls import path
from . import views

app_name = "workout"

urlpatterns = [
    path('bones/', views.bones, name="list-bones"),
    path('joints/', views.joints, name="list-joints"),
    path('muscles/', views.muscles, name="list-muscles"),
    path('exercises/', views.exercises, name="list-exercises"),

    path('muscles/<slug>/', views.know_muscle, name="muscle"),
    path('bones/<slug>/', views.know_bone, name="bone"),
    path('joints/<slug>/', views.know_joint, name="joint"),
    path('exercises/<slug>/', views.know_exercise, name="exercise"),
]
