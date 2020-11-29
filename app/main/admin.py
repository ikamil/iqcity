from django.contrib import admin
from django.utils import timezone
from datetime import datetime
from .models import *
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.urls import resolve
from admin_auto_filters.filters import AutocompleteFilter


def fnow():
    return timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.get_default_timezone())


class IndicatorFilter(AutocompleteFilter):
    title = 'Индикатор' # display title
    field_name = 'indicator' # name of the foreign key field


class IndicatorGroupFilter(AutocompleteFilter):
    title = 'Группа индикаторов' # display title
    field_name = 'indicatorgroup' # name of the foreign key field


class InIndicatorGroupFilter(AutocompleteFilter):
    title = 'Группа индикаторов' # display title
    field_name = 'indicator__indicatorgroup' # name of the foreign key field


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description', 'modified']
    save_as = True
    readonly_fields = ['creator', 'created', 'modifier', 'modified', 'deleted', 'deleter']

    def get_queryset(self, request):
        qs = super(BaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(deleted__isnull=True)
        else:
            return qs.filter(Q(deleted__isnull=True) & Q(creator=request.user))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "brand":
        #     if request.user.is_superuser:
        #         kwargs["queryset"] = Brands.objects.filter(deleted__isnull=True)
        #     else:
        #         kwargs["queryset"] = Brands.objects.filter(Q(deleted__isnull=True) & Q(pk__in=BrandUser.objects.filter(Q(user=request.user) & Q(deleted__isnull=True)).values('brand')))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_model(self, request, obj):
        obj.deleter = request.user
        obj.deleted = fnow()
        obj.save()

    def delete_queryset(self, request, queryset):
        for dl in queryset:
            self.delete_model(request, dl)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user if not getattr(obj, 'creator') else getattr(obj, 'creator')
        obj.created = fnow() if not getattr(obj, 'created') else getattr(obj, 'created')
        if hasattr(obj, 'modifier'):
            obj.modifier = request.user
        if hasattr(obj, 'changer'):
            obj.changer = request.user
        return super(BaseAdmin, self).save_model(request, obj, form, change)

    # def save_related(self, request, form, formsets, change):
        # raise Exception([dict(form) for form in formsets])
        # return super(BaseInline, self.save_related(request, form, formsets, change))

    def has_delete_permission(self, request, obj=None):
        if '/change/' in request.__str__() and request.__str__() != getattr(request, '_editing_document', False):  # query attribute
            return False
        return super(BaseAdmin, self).has_delete_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        if '/change/' in request.__str__() and type(self) != getattr(request, '_editing_document', False):  # query attribute
            return False
        return super(BaseAdmin, self).has_change_permission(request, obj=obj)

    def _changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        request._editing_document = type(self)
        return super(BaseAdmin, self)._changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class ImageBaseAdmin(BaseAdmin):
    def img(self, obj):
        return mark_safe("""<img width="100px" src="%s">""" % ((str(obj.image) if str(obj.image).startswith('http') else obj.image.url) if obj.image else ''))

    list_display = ['name', 'description', 'image']
    fields = ['name', 'description', 'image', 'img']
    readonly_fields = ['img', 'modifier', 'deleted']


class IndicatorBaseAdmin(BaseAdmin):
    list_display = ['name', 'description', 'weight_default']
    fields = ['name', 'description', 'weight_default', 'modified']
    readonly_fields = ['modified']


class ImageOwnAdmin(ImageBaseAdmin):

    def get_queryset(self, request):
        qs = super(BaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(deleted__isnull=True)
        else:
            return qs.filter(Q(deleted__isnull=True) & Q(changer=request.user))


class BaseInline(admin.TabularInline):

    def get_queryset(self, request):
        qs = super(BaseInline, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(deleted__isnull=True)
        else:
            return qs.filter(Q(deleted__isnull=True) & Q(modifier=request.user))


admin.site.enable_nav_sidebar = False


@admin.register(Region)
class RegionAdmin(ImageBaseAdmin):
    pass


@admin.register(SubIndex)
class SubIndexAdmin(IndicatorBaseAdmin):
    pass


@admin.register(IndicatorGroup)
class IndicatorGroupAdmin(IndicatorBaseAdmin):
    search_fields = ['name', 'description']


@admin.register(IndicatorType)
class IndicatorTypeAdmin(IndicatorBaseAdmin):
    list_display = ['id', 'name', 'description', 'weight_default']
    fields = ['id', 'name', 'description', 'weight_default', 'modified']


@admin.register(Indicator)
class IndicatorAdmin(IndicatorBaseAdmin):
    search_fields =  ['name', 'description', 'indicatorgroup__name']
    list_display = ['name', 'subindex', 'indicatorgroup', 'indicatortype', 'description', 'weight_default']
    fields = ['name', 'subindex', 'indicatorgroup', 'indicatortype', 'description', 'weight_default']
    list_filter = [IndicatorGroupFilter]


@admin.register(IndicatorData)
class IndicatorDataAdmin(BaseAdmin):
    list_display = ['city', 'indicator', 'value']
    fields = ['city', 'indicator', 'value']
    list_filter = ['city', IndicatorFilter]


class IndicatorDataInline(BaseInline):
    model = IndicatorData
    fields = ['indicator', 'value']
    autocomplete_fields = ['indicator']


@admin.register(City)
class CityAdmin(ImageBaseAdmin):
    fields = ['name', 'description', 'region', 'population', 'area', 'vvp']
    list_display = ['name', 'region', 'population', 'area', 'vvp']
    inlines = [IndicatorDataInline]


@admin.register(IQIndexHistory)
class IQIndexHistoryAdmin(BaseAdmin):
    list_display = ['city', 'iq_index', 'created']
    fields = ['city', 'iq_index', 'created']
    readonly_fields = fields
    list_filter = ['city', 'created']


@admin.register(RawData)
class RawDataAdmin(BaseAdmin):
    list_display = ['city', 'indicator', 'name', 'param', 'value', 'weight_default']
    fields = ['city', 'indicator', 'name', 'param', 'value', 'weight_default']
    list_filter = ['city', IndicatorFilter]


@admin.register(ApiMethod)
class ApiMethodAdmin(BaseAdmin):
    list_display = ['name', 'url', 'headers', 'city', 'indicator']
    fields = ['name', 'url', 'headers', 'city', 'indicator']
    list_filter = ['city', IndicatorFilter]















#
# class BrandsAdmin(ImageBaseAdmin):
#     fields = ['brand_name', 'category', 'created', 'changed', 'changer', 'status', 'img', 'image']
#     list_display = fields[:-1]
#     list_filter = ['category']
#     list_search = ['brand_name', 'category__name']
#     inlines = [BrandUserInline]
#
#     def get_queryset(self, request):
#         qs = super(BaseAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs.filter(deleted__isnull=True)
#         else:
#             return qs.filter(Q(deleted__isnull=True) & Q(changer=request.user) & Q(pk__in = BrandUser.objects.filter(Q(user=request.user) & Q(deleted__isnull=True))))


class VendorsAdmin(BaseAdmin):
    fields = ['vendor_name', 'created', 'changed', 'changer', 'status']
    list_display = fields


class WarehousesAdmin(BaseAdmin):
    fields = ['warehouse_name', 'created', 'changed', 'changer', 'status']
    list_display = fields


class MarketplaceAdmin(ImageBaseAdmin):
    fields = ['name', 'img', 'image', 'description', 'changed']
    list_display = [x for x in fields if x != 'image']


class PacktypessAdmin(BaseAdmin):
    fields = ['packtype_name', 'created', 'changed', 'changer', 'status']
    list_display = fields


class StatusesAdmin(BaseAdmin):
    fields = ['status_name', 'created', 'changed', 'changer', 'status']
    list_display = fields


class ColorsAdmin(BaseAdmin):
    def color_html(self, obj):
        return mark_safe("""<div style="-webkit-appearance: square-button; width: 44px; height: 23px; border-width: 1px; border-style: solid; border-color: rgb(169, 169, 169); background-color: %s;"></div>""" % obj.color)

    fields = ['color_name', 'color', 'created', 'changed', 'changer',  'status']
    list_display = ['color_name', 'color_html', 'created', 'changed', 'changer', 'status']


class SizeAdmin(BaseAdmin):
    fields = ['name', 'width', 'height', 'depth', 'created', 'changed', 'changer', 'status']
    list_display = fields


class CategoryAdmin(ImageBaseAdmin):
    search_fields = ['name']
    list_display = ['name', 'parent', 'description', 'img']
    fields = ['name', 'parent', 'description', 'image', 'img']
    list_filter = [('parent', admin.RelatedOnlyFieldListFilter)]


class UnitAdmin(ImageBaseAdmin):
    fields = ['name', 'code', 'valuetype', 'description', 'image', 'img']
    list_display = ['name', 'code', 'valuetype', 'description', 'img']


# class AttributeCategoryInline(BaseInline):
#     model = AttributeCategory
#     fields = ['category', 'comments']
#     autocomplete_fields = ['category']
#
#
# class AttributeValueInline(BaseInline):
#     model = AttributeValue
#     fields = ['value', 'category', 'wb_value', 'description']
#     autocomplete_fields = ['category']
#     raw_id_fields = ['wb_value']
#
#
# class AttributeAdmin(ImageBaseAdmin):
#     list_per_page = settings.LIST_PER_PAGE
#     list_display = ['name', 'unit', 'attributegroup', 'category', 'db_field', 'wb_field', 'img']
#     fields = ['name', 'unit', 'attributegroup', 'category', 'description', 'img', 'db_field', 'wb_field']
#     list_filter = [('wb_field__marketplace', admin.RelatedOnlyFieldListFilter), ('unit', admin.RelatedOnlyFieldListFilter), ('attributegroup', admin.RelatedOnlyFieldListFilter), ('category', admin.RelatedOnlyFieldListFilter)]
#     inlines = [AttributeValueInline, AttributeCategoryInline]
#     raw_id_fields = ['wb_field']
#     search_fields = ['name']


class AttributeValueAdmin(ImageBaseAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ['attribute', 'value', 'category', 'description', 'wb_value']
    fields = ['attribute', 'value', 'category', 'description', 'wb_value']
    list_filter = [('wb_value__marketplace', admin.RelatedOnlyFieldListFilter), ('category', admin.RelatedOnlyFieldListFilter)]
    raw_id_fields = ['wb_value']


class MarketplaceFieldAdmin(BaseAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ['name', 'marketplace', 'field_id']
    fields = ['name', 'marketplace', 'field_id']
    list_filter = [('marketplace', admin.RelatedOnlyFieldListFilter)]


class MarketplaceValueAdmin(BaseAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ['item_number', 'marketplace', 'field', 'value', 'fieldid']
    fields = ['item_number', 'marketplace', 'field', 'value', 'fieldid']
    list_filter = [('marketplace', admin.RelatedOnlyFieldListFilter)]

#
# @admin.register(ScrapyItem)
# class ScrapyItemAdmin(admin.ModelAdmin):
#     list_per_page = settings.LIST_PER_PAGE
#     list_display = ['type', 'item', 'created', 'spider']
#     readonly_fields = ['created']
#     list_filter = ['type']
