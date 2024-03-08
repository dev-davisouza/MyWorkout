from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse


# Human body section:

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
    ], blank=True)
    description = models.TextField("Some description of the bone")
    muscles = models.ManyToManyField("Muscle", blank=True)
    slug = models.CharField(blank=True, max_length=50)
    is_spine_bone = models.BooleanField(blank=True, default=False)
    is_skull_bone = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('workout:bone', kwargs={"slug": self.slug})


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

    def get_absolute_url(self):
        return reverse('workout:joint', kwargs={"slug": self.slug})


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
    related_exercises = models.ManyToManyField("Exercise")

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

    def get_absolute_url(self):
        return reverse('workout:muscle', kwargs={"slug": self.slug})


class BioMovimentType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']


# Workout section:

class Exercise(models.Model):
    EXERCISE_DIFFICULTY = (
        ("E", "Easy"),
        ("M", "Medium"),
        ("H", "Hard",),
    )

    RES_PROFILE = (
        ("Unk", "Unknown"),
        ("Asc", "Ascending"),
        ("Dow", "Downward"),
    )

    cover = models.FileField(upload_to="images/exercises/%Y/%m/%d/",
                             validators=[FileExtensionValidator(['svg'])])
    name = models.CharField("Exercise name", max_length=120)
    description = models.TextField("Exercise description")
    difficulty = models.CharField("Select the difficulty", max_length=1,
                                  choices=EXERCISE_DIFFICULTY)
    muscles = models.ManyToManyField("Muscle", related_name="Muscle", blank=True)
    muscle_group = models.ManyToManyField("MuscleGroup", related_name="MuscleGroup")
    slug = models.SlugField(unique=True, default="")
    resistance_profile = models.CharField("Resistance profile",
                                          choices=RES_PROFILE,
                                          max_length=3,
                                          blank=True)
    is_dumbell = models.BooleanField(default=False)
    is_barbell = models.BooleanField(default=False)
    is_cable = models.BooleanField(default=False)
    is_machine = models.BooleanField(default=False)
    sets = models.IntegerField("Number of sets", blank=True, default=0)
    steps = models.TextField("Steps", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workout:exercise', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']


"""class Set(models.Model):
    class SetTypeChoice(models.TextChoices):
        UND = ('Undefined', "It's just a set without classification")

        WUS = ('Warm Up', f'Warm up sets are responsible for lubricating the joints, '
               f'stimulating the bursae to release synovial fluid that will prevent the '
               f'bones from rubbing against the cartilage, preserving not only the cartilage '
               f'but also the joint capsule, and consequently, preventing possible osteoarthritis '
               f'and bone wear as a result. of physical effort. These sets are also responsible for '
               f'sending the stimulus to the central nervous system, indicating that the muscle is '
               f'working, which will make the brain understand the moment and prepare the body for '
               f'more efficient work. The Warm up set also serves to irrigate the muscle with blood, '
               f'bringing oxygen and nutrients, especially sodium, calcium and carbohydrates, allowing '
               f'the muscle to produce force more efficiently and preserving the tendons, brutally reducing '
               f'the chance of an injury during training. by mechanical tension.')

        FS = ('Feeder', f"Feeder sets are useful for progressing loads during an exercise in a safe and effective way. "
              f"For example, assuming that your PR in the Bench Press is 100kg off the bar, it is completely contraindicated "
              f"for you to warm up with 20kg and then go straight to 100kg! You probably won't perform well even if you warm up. " 
              f"Furthermore, you will greatly increase your chance of injuring your muscle, as it and the central nervous system " 
              f"are not yet ready for a high load. Therefore, the feeders serve to stimulate your muscles and your brain, in order " 
              f"to prepare them for greater loads with each feeder set, so that in the end you can reach an execution with a maximum " 
              f"load previously done, and possibly, progress this weight.")

        WS = ('Work', f"Work sets are sets where you already notice a high degree of mechanical tension during execution; "
              f"Despite this, in these sets you do not reach your muscle's maximum strength production. The objective of "
              f"these series can vary from - being a preparation for the set where you will actually try your best, or it "
              f"can also be a set just with the aim of providing stimulus to a specific muscle.")

        TOP = ('Top', f"The top set is the heaviest set of the workout, where one typically aims to increase "
               f"the load or the number of repetitions. This is necessary to stress the mechanoreceptors to "
               f"the maximum, which are neurons present in the muscles that detect all the mechanical tension "
               f"placed on the muscle. Therefore, when aligning high loads to bring the muscle to concentric "
               f"failure with good execution technique, you are likely to stimulate the growth and recovery "
               f"mechanism of your body, which is what you are seeking in your training, as this will generate "
               f"hypertrophy in the target muscle of the exercise!")

    count_reps = models.IntegerField(blank=True)
    intial_margin_expected_reps = models.IntegerField("Min. of reps:")
    final_margin_expected_reps = models.IntegerField("Max. of reps:")

    set_type = models.CharField(choices=SetTypeChoice.choices,
                                default=SetTypeChoice.UND,
                                max_length=10)
    is_valid_set = models.BooleanField("This set is valid?",
                                       blank=False, null=False)

    def __str__(self):
        return self.set_type

    def get_set_type_description(self):
        return self.SetTypeChoice(self.set_type).label"""
