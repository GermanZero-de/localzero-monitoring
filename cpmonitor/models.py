from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Note PEP-8 naming convetions for class names apply. So use the singular and CamelCase


### Lookup-entities (shared among all cities, entered by admins)

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ord = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return self.name


class TaskCategory(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True)
    info = models.TextField()
    ord = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return self.name


### data-entities (entered by users)

class City(models.Model):
    name = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5)
    info = models.TextField(blank=True)  
    url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.zipcode + " " + self.name


class Task(models.Model):

    class States(models.IntegerChoices):
        UNKNOWN = 0
        SUGGESTED = 1
        PLANNED = 2
        WAITING = 3
        IN_PROGRESS = 4
        DONE = 5
        REJECTED =6

    class Severities(models.IntegerChoices):
        CRITICAL = 5
        HIGH = 4
        STANDARD=3
        LOW = 2
        VERY_LOW = 1

    city = models.ForeignKey(City, on_delete=models.PROTECT)
    category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    info = models.TextField()

    state = models.IntegerField(choices=States.choices,default=States.UNKNOWN)
    severity = models.IntegerField(choices=Severities.choices, default=Severities.STANDARD)
    completion = models.IntegerField(
                    default=0, 
                    validators=[
                        MinValueValidator(0),
                        MaxValueValidator(100)
                    ]
                )

    def __str__(self) -> str:
        return self.name
