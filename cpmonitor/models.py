from django.db import models

# Note PEP-8 naming convetions for class names apply. So use the singular and CamelCase


class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
