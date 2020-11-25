from django.db import models

# Create your models here.
class Postdb(models.Model):
    name = models.TextField(max_length=500)

    # def __unicode__(self):
    #     return self.name

    # def __str__(self):
    #     return self.name