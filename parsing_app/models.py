from django.db import models

class Skill(models.Model):
    skill_name = models.CharField(max_length=250,default='')

    def __str__(self):
        return self.skill_name
