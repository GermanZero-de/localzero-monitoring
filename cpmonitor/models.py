from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from treebeard.mp_tree import MP_Node

# Note PEP-8 naming conventions for class names apply. So use the singular and CamelCase


class City(models.Model):
    name = models.CharField("Name", max_length=255)
    zipcode = models.CharField("PLZ", max_length=5)
    url = models.URLField("Homepage", blank=True)

    introduction = models.TextField("Einleitung", blank=True)

    budget = models.IntegerField("CO2 Budget [Mio Tonnen]", default=0)

    def __str__(self) -> str:
        return self.zipcode + " " + self.name


class Task(MP_Node):
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Stadt")

    title = models.CharField("Titel", max_length=255)

    description = models.TextField("Beschreibung", blank=True, default="")

    planned_start = models.DateTimeField("Geplanter Start", blank=True, null=True)

    planned_completion = models.DateTimeField("Geplantes Ende", blank=True, null=True)

    class States(models.IntegerChoices):
        UNKNOWN = 0
        SUGGESTED = 1
        PLANNED = 2
        WAITING = 3
        IN_PROGRESS = 4
        DELAYED = 5
        SUCCEEDED = 6
        FAILED = 7
        REJECTED = 8

    state = models.IntegerField(
        "Zustand", choices=States.choices, default=States.UNKNOWN
    )

    justification = models.TextField("Begründung Zustand", blank=True, default="")

    # Maybe later. Not part of the MVP:

    # class Severities(models.IntegerChoices):
    #     CRITICAL = 5
    #     HIGH = 4
    #     STANDARD = 3
    #     LOW = 2
    #     VERY_LOW = 1
    # severity = models.IntegerField(
    #     "Schweregrad",
    #     choices=Severities.choices,
    #     default=Severities.STANDARD)

    # weight = models.IntegerField(
    #     "Gewicht",
    #     default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(3)
    #     ]
    # )

    completion = models.IntegerField(
        "Vervollständigungsgrad",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self) -> str:
        return self.title


# Tables for comparing and connecting the plans of all cities
# Lookup-entities (shared among all cities, entered by admins)

# This is currently kept out of the above city-specific data, since
# it might not be part of the MVP.

# Thoughts:
# - It might be better placed in a separate Django app, to keep it apart from the city stuff in the admin interface.
# - Sector / TaskCategory might be one table with recursive reference. Lets see, how that works out with the Tasks table.

# class Sector(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     ord = models.IntegerField(unique=True)

#     def __str__(self) -> str:
#         return self.name


# class TaskCategory(models.Model):
#     sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
#     name = models.CharField(max_length=200, unique=True)
#     info = models.TextField()
#     ord = models.IntegerField(unique=True)

#     def __str__(self) -> str:
#         return self.name


# class TaskToCategory(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.PROTECT)
#     category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)

#     def __str__(self) -> str:
#         return self.category.name + " - " + self.task.title
