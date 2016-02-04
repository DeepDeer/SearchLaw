from __future__ import unicode_literals

from django.db import models

class Results(models.Model):
    fy = models.CharField(max_length=10)
    nr = models.CharField(max_length=10)
    gbrq = models.CharField(max_length=10)
    lx = models.CharField(max_length=10)
    dq = models.CharField(max_length=10)
    ID = models.CharField(max_length=10)
    link = models.URLField()
