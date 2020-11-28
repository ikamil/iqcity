from django.db import models
from main.models import *


class IQIndex(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    city = models.OneToOneField(City, primary_key=True, on_delete=models.PROTECT)
    population = models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    vvp = models.FloatField(blank=True, null=True)
    digital = models.FloatField(blank=True, null=True)
    social = models.FloatField(blank=True, null=True)
    utility = models.FloatField(blank=True, null=True)
    iq_index = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vr_iq_index'
        verbose_name_plural = 'IQ Индексы'
        verbose_name = 'IQ Индекс'

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        pass