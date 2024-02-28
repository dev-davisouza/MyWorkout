from django.db import models
from django.core.validators import FileExtensionValidator


class MovimentType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name
    
    class Meta:
        ordering = ['type_name']


class Bone(models.Model):
    name = models.CharField("Bone name", max_length=50)
    cover = models.FileField(upload_to="images/bones/%Y/%m/%d/", validators=[
        FileExtensionValidator(['svg'])
    ])
    description = models.TextField("Some description of the bone")
    muscles = models.ManyToManyField("Muscle", blank=True)
    slug = models.CharField(blank=True, max_length=50)
    is_spine_bone = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class JointType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Joint(models.Model):
    name = models.CharField("Joint name", max_length=50)
    cover = models.FileField(upload_to="images/joints/%Y/%m/%d/", validators=[
        FileExtensionValidator(['svg'])
    ])
    bones = models.ManyToManyField("Bone")
    allowed_movements = models.ManyToManyField("MovimentType")

    joint_type = models.ManyToManyField("JointType")
    description = models.TextField("Some description of the joint",
                                   blank=True)
    slug = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ['name']


class Muscle(models.Model):
    name = models.CharField("Muscle name", max_length=50)
    scientific_name = models.CharField("Correct name", max_length=100,
                                       default="", blank=True)
    action = models.ManyToManyField("BioMovimentType")
    joints = models.ManyToManyField("Joint")
    origin = models.ManyToManyField("Bone", related_name="bone_origin")
    insertion = models.ManyToManyField("Bone", related_name="bone_insertions")
    cover = models.FileField(upload_to="images/muscles/%Y/%m/%d/", validators=[
        FileExtensionValidator(['svg'])
    ], blank=True)
    description = models.TextField("Some description of the muscle",
                                   blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MuscleGroup(Muscle):
    origins = models.ManyToManyField("Muscle", verbose_name="Heads (origins)",
                                     related_name="muscle_origins", blank=True)
    slug = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BioMovimentType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']


class Exercise(models.Model):
    EXERCISE_DIFFICULTY = (
        ("E", "Easy"),
        ("M", "Medium"),
        ("H", "Hard",),
    )

    cover = models.FileField(upload_to="images/exercises/%Y/%m/%d/",
                             validators=[FileExtensionValidator(['svg'])])
    name = models.CharField("Exercise name", max_length=120)
    description = models.TextField("Exercise description")
    difficulty = models.CharField("Select the difficulty", max_length=1,
                                  choices=EXERCISE_DIFFICULTY)
    muscles = models.ManyToManyField("Muscle")
    slug = models.SlugField(unique=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
