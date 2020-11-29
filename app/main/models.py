from django.db import models
from django.conf import settings
from django.utils import timezone
import random, string
from datetime import datetime
from django.db import connection
from colorful.fields import RGBColorField
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField


def fnow():
    return timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.get_default_timezone())


def nvl(pval, pdefault = None):
    return pval if pval else pdefault if pdefault else ''


def random_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class Region(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(max_length=500, blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Наименование')
    created = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tregion'
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    region = models.ForeignKey(Region, models.DO_NOTHING, verbose_name='Регион')
    image = models.ImageField(max_length=500, blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    vvp = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tcity'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class SubIndex(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(max_length=500, blank=True, null=True,  verbose_name='Изображение')
    description = models.TextField(blank=True, null=True)
    weight_default = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tsubindex'
        verbose_name = 'СубИндекс'
        verbose_name_plural = 'СубИндексы'

    def __str__(self):
        return self.name


class IndicatorGroup(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(max_length=500, blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True)
    weight_default = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tindicatorgroup'
        verbose_name = 'Группа индикаторов'
        verbose_name_plural = 'Группы индикаторов'

    def __str__(self):
        return self.name


class IndicatorType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(max_length=500, blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True)
    weight_default = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tindicatortype'
        verbose_name = 'Тип индикатора'
        verbose_name_plural = 'Типы индикаторов'

    def __str__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    image = models.ImageField(max_length=500, blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True)
    weight_default = models.FloatField(blank=True, null=True)
    subindex = models.ForeignKey(SubIndex, models.DO_NOTHING)
    indicatorgroup = models.ForeignKey(IndicatorGroup, models.DO_NOTHING)
    indicatortype = models.ForeignKey(IndicatorType, models.DO_NOTHING)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tindicator'
        verbose_name = 'Индикатор'
        verbose_name_plural = 'Индикаторы'

    def __str__(self):
        return self.name


class IndicatorData(models.Model):
    value = models.FloatField(blank=True, null=True, verbose_name='Значение')
    city = models.ForeignKey(City, models.DO_NOTHING, verbose_name='Город')
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING, verbose_name='Индикатор')
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tindicatordata'
        verbose_name = 'Значение индикатора'
        verbose_name_plural = 'Значения индикаторов'

    def __str__(self):
        return self.indicator.name

class IQIndexHistory(models.Model):
    iq_index = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, verbose_name='Город')
    created = models.DateTimeField(blank=True, null=True, default=now, verbose_name='Дата вычисления')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tiqindex_history'
        verbose_name = 'История IQ индекса'
        verbose_name_plural = 'История IQ индексов'


class RawData(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    weight_default = models.FloatField(blank=True, null=True, verbose_name='Вес показателя')
    param = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING)
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING)
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trawdata'
        verbose_name = 'Блок загруженных данных'
        verbose_name_plural = 'Загруженные данные'

    def __str__(self):
        return self.name


class ApiMethod(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    url = models.CharField(max_length=2000, verbose_name='URL для вызова')
    headers = models.TextField(max_length=2000, blank=True, null=True, verbose_name='HTTP заголовки')
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True, verbose_name='Город')
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING, blank=True, null=True, verbose_name='Индикатор')
    created = models.DateTimeField(blank=True, null=True, default=now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True, default=now)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tapimethod'
        verbose_name = 'API для импорта данных'
        verbose_name_plural = 'API для импорта данных'

    def __str__(self):
        return self.indicator.name