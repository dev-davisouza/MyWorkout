from typing import Union
from django.views.generic import ListView
from django.http import JsonResponse
from workout.models import Bone, Joint, MuscleGroup, Exercise


def iterate_m2m_items(model_object: Union[Bone, Joint, MuscleGroup, Exercise],
                      mtm_field,
                      parameter):
    objects_list = []
    for obj in getattr(model_object, mtm_field).all():
        objects_list.append(getattr(obj, parameter))
    if len(objects_list) == 1:
        for _ in objects_list:
            return _
    else:
        return objects_list


def bonesApi(request):
    objects = Bone.objects.all().values('name', 'description',
                                        'is_spine_bone', 'is_skull_bone')
    return JsonResponse(
            list(objects),
            safe=False
        )


class JointsViewApi(ListView):
    model = Joint
    context_object_name = 'joints'

    def render_to_response(self, context, **response_kwargs):
        joints = self.get_context_data()[self.context_object_name]
        joint_data = []

        for joint in joints:
            joint_dict = {
                'name': joint.name,
                'description': joint.description,
                'bones': iterate_m2m_items(joint, 'bones', 'name'),
                'allowed_movements': iterate_m2m_items(joint,
                                                       'allowed_movements',
                                                       'type_name'),
                'joint_type': iterate_m2m_items(joint, 'joint_type',
                                                'type_name'),
            }
            joint_data.append(joint_dict)

        return JsonResponse(
            list(joint_data),
            safe=False
        )


class MusclesViewApi(ListView):
    model = MuscleGroup
    context_object_name = 'muscles'

    def render_to_response(self, context, **response_kwargs):
        muscles = self.get_context_data()[self.context_object_name]
        muscle_data = []

        for muscle in muscles:
            joint_dict = {
                'name': muscle.name,
                'description': muscle.description,
                'scientific_name': muscle.scientific_name,
                'action': iterate_m2m_items(muscle, "action", "type_name"),
                'joints': iterate_m2m_items(muscle, "joints", "name"),
                'origin': iterate_m2m_items(muscle, "origin", "name"),
                'insertion': iterate_m2m_items(muscle, "insertion", "name"),
                'related_exercises': iterate_m2m_items(
                    muscle, "related_exercises", "name"),
            }
            muscle_data.append(joint_dict)

        return JsonResponse(
            list(muscle_data),
            safe=False
        )


class ExercisesViewApi(ListView):
    model = Exercise
    context_object_name = 'exercises'

    def render_to_response(self, context, **response_kwargs):
        exercises = self.get_context_data()[self.context_object_name]
        exercises_data = []

        for exercise in exercises:
            exercise_dict = {
                'name': exercise.name,
                'description': exercise.description,
                'difficulty': exercise.difficulty,
                'muscles': iterate_m2m_items(exercise, 'muscles', 'name'),
                'muscles_group': iterate_m2m_items(exercise, 'muscle_group',
                                                   'name'),
                'resistance_profile': exercise.resistance_profile,
                'is_dumbell': exercise.is_dumbell,
                'is_barbell': exercise.is_barbell,
                'is_cable': exercise.is_cable,
                'is_machine': exercise.is_machine,
                'steps': exercise.steps,
            }
            exercises_data.append(exercise_dict)

        return JsonResponse(
            list(exercises_data),
            safe=False
        )
