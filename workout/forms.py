from django import forms
from .models import Workout, SetExerciseRelationship


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        exclude = ('user',)


class SetExerciseRelationshipForm(forms.ModelForm):
    class Meta:
        model = SetExerciseRelationship
        exclude = ('user',)
