from typing import Union
from django.views.generic import ListView
from django.http import JsonResponse
from workout.models import Bone, Joint, MuscleGroup, Exercise
from django.forms.models import model_to_dict


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


class BonesViewApi(ListView):
    model = Bone
    context_object_name = 'bones'

    def get_queryset(self):
        return Bone.objects.all()
    
    def get_queryset_as_dict(self):
        objects = [model_to_dict(obj) for obj in self.get_queryset()]
        for obj_dict in objects:
            obj_dict.pop('id', None)
            obj_dict.pop('cover', None)
            obj_dict.pop('slug', None)
        return objects
    

    def render_to_response(self, context, **response_kwargs):
        bones = self.get_context_data()[self.context_object_name]
        bone_data = []

        for bone in bones:
            bone_dict = {
                'name': bone.name,
                'description': bone.description,
                'muscles': iterate_m2m_items(bone, 'muscles', 'name'),
                'is_spine_bone': bone.is_spine_bone,
                'is_skull_bone': bone.is_skull_bone,
            }
            bone_data.append(bone_dict)

        self.bone_data = bone_data

        return JsonResponse(
            list(bone_data),
            safe=False
        )


class JointsViewApi(ListView):
    model = Joint
    context_object_name = 'joints'

    def get_queryset(self):
        return Joint.objects.all()
    
    def get_queryset_as_dict(self):
        objects = [model_to_dict(obj) for obj in self.get_queryset()]
        for obj_dict in objects:
            obj_dict.pop('id', None)
            obj_dict.pop('cover', None)
            obj_dict.pop('slug', None)
        return objects
    

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

        self.joint_data = joint_data

        return JsonResponse(
            list(joint_data),
            safe=False
        )


class MusclesViewApi(ListView):
    model = MuscleGroup
    context_object_name = 'muscles'

    def get_queryset(self):
        return MuscleGroup.objects.all()

    def render_to_response(self, context, **response_kwargs):
        muscles = self.get_context_data()[self.context_object_name]
        muscle_data = []

        for muscle in muscles:
            muscle_dict = {
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
            muscle_data.append(muscle_dict)

        return JsonResponse(
            list(muscle_data),
            safe=False
        )


class ExercisesViewApi(ListView):
    model = Exercise
    context_object_name = 'exercises'

    def get_queryset(self):
        return Exercise.objects.all()

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
