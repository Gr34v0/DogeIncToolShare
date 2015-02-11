from django.db import models


class Community(models.Model):
    class Meta:
        verbose_name_plural = "Communities"

    name = models.CharField('Community Name', max_length=200)
