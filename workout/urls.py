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
    path('search/', views.search, name="search"),
    path('add-setexerciserelationship/',
         views.add_set_exercise_relationship,
         name="add-set_exercise_relationship"),
    path('change-setexerciserelationship/<id>/',
         views.edit_set_exercise_relationship,
         name="change-set_exercise_relationship"),
    path('delete-setexerciserelationship/<id>/',
         views.delete_set_exercise_relationship,
         name="delete-set_exercise_relationship"),

    path('add-workout/', views.add_workout, name="add-workout"),
    path('myworkout/<slug>', views.view_myworkout, name="myworkout"),
    path('change-myworkout/<slug>', views.edit_myworkout, name="change-myworkout"),
    path('delete-myworkout/<slug>', views.delete_myworkout, name="delete-myworkout"),

    # Downloads:
    path('download-xlx/myworkout/<slug>', views.download_myworkout_as_xls, name="download-xls"),
    path('download-pdf/myworkout/<slug>', views.download_myworkout_as_pdf, name="download-pdf"),
]
