from django import forms
from .models import Workout, SetExerciseRelationship


class SetExerciseRelationshipForm(forms.ModelForm):
    class Meta:
        model = SetExerciseRelationship
        exclude = ('user',)


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        exclude = ('user', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['set_exercise_relationships'].widget.attrs.update({'class': 'hidden'})
