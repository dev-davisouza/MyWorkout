from django.contrib import admin
from . import models

admin.site.register(models.Bone)
admin.site.register(models.Joint)
admin.site.register(models.JointType)
admin.site.register(models.Exercise)
admin.site.register(models.MovimentType)
admin.site.register(models.Muscle)
admin.site.register(models.BioMovimentType)
admin.site.register(models.MuscleGroup)

