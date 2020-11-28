from admin_totals.admin import ModelAdminTotals
from django.contrib import admin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from .models import *


@admin.register(IQIndex)
class IQIndexAdmin(ModelAdminTotals):
    list_display = [field.name for field in IQIndex._meta.get_fields()]
    list_totals = [('iq_index', lambda field: Coalesce(Avg(field), 0)),
                   ('digital', lambda field: Coalesce(Avg(field), 0)),
                   ('social', lambda field: Coalesce(Avg(field), 0)),
                   ('utility', lambda field: Coalesce(Avg(field), 0)),
                   ('area', lambda field: Coalesce(Sum(field), 0)),
                   ('population', lambda field: Coalesce(Sum(field), 0)),
                   ('vvp', lambda field: Coalesce(Sum(field), 0))]
    readonly_fields = list_display


# Register your models here.
admin.site.enable_nav_sidebar = False