from django.contrib import admin
from django.db.models import Count, Q
from django.core import serializers
from django.http import HttpResponse
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter)
from admin_decorators import short_description, order_field
from .models import(
Brand,
GroupProduct, Product,
Feature, FeatureValue,
ProductFeature,
ProductGallery
)

# Brand Admin Configuration
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for Brand model."""
    list_display = ('brand_name', 'slug')
    list_filter = ('brand_name',)
    search_fields = ('brand_name',)
    ordering = ('brand_name',)


# Product Group Admin Actions
def deactive_product_group(modeladmin, request, queryset):
    """Deactivate selected product groups."""
    res = queryset.update(is_active=False)
    modeladmin.message_user(request, f'تعداد {res} غیر فعال شد')


def active_product_group(modeladmin, request, queryset):
    """Activate selected product groups."""
    res = queryset.update(is_active=True)
    modeladmin.message_user(request, f'تعداد {res} فعال شد')


def export_json(modeladmin, request, queryset):
    """Export selected groups to JSON."""
    response = HttpResponse(content_type='application/json')
    serializers.serialize("json", queryset, stream=response)
    return response


class ProductGroupInstanceInline(admin.TabularInline):
    """Inline for displaying group products."""
    model = GroupProduct
    extra = 1


class GroupFilter(admin.SimpleListFilter):
    """Filter for GroupProduct by parent group."""
    title = 'گروه محصولات'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        sub_groups = GroupProduct.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_name) for item in groups]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(group_parent=self.value()))
        return queryset


@admin.register(GroupProduct)
class ProductGroupAdmin(admin.ModelAdmin):
    """Admin configuration for GroupProduct model."""
    list_display = (
        'group_name', 'group_parent', 'is_active', 'slug',
        'count_sub_group', 'count_product_of_group'
    )
    list_filter = (GroupFilter, 'is_active')
    search_fields = ('group_name',)
    ordering = ('group_name',)
    actions = [deactive_product_group, active_product_group, export_json]
    inlines = [ProductGroupInstanceInline]

    def get_queryset(self, request):
        """Get queryset with sub group count annotated."""
        qs = super().get_queryset(request)
        return qs.annotate(sub_group=Count('product_of_groups'))

    @short_description('تعداد کالاهای گروه')
    @order_field('product_of_groups')
    def count_product_of_group(self, obj):
        """Count products in group."""
        return obj.product_of_groups

    @short_description('تعداد زیرگروه‌ها')
    @order_field('sub_group')
    def count_sub_group(self, obj):
        """Count subgroups in group."""
        return obj.sub_group


class FeatureValueInline(admin.TabularInline):
    """Inline for displaying feature values."""
    model = FeatureValue
    extra = 1


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """Admin configuration for Feature model."""
    list_display = ('feature_name',)
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline]


# Product Admin Actions
def deactive_product(modeladmin, request, queryset):
    """Deactivate selected products."""
    res = queryset.update(is_active=False)
    modeladmin.message_user(request, f'تعداد {res} غیر فعال شد')


def active_product(modeladmin, request, queryset):
    """Activate selected products."""
    res = queryset.update(is_active=True)
    modeladmin.message_user(request, f'تعداد {res} فعال شد')


def export_json_products(modeladmin, request, queryset):
    """Export selected products to JSON."""
    response = HttpResponse(content_type='application/json')
    serializers.serialize("json", queryset, stream=response)
    return response


class ProductFeatureAdmin(admin.TabularInline):
    """Inline for displaying product features."""
    model = ProductFeature
    extra = 1

    class Media:
        css = {'all': ('css/admin_style.css',)}
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'assets/scripts/admin_script.js',
        )


class GalleryProductInline(admin.TabularInline):
    """Inline for displaying product gallery."""
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = (
        'product_name', 'brand', 'is_active', 'slug', 'price',
        'display_product_group',
    )
    list_filter = ('brand', 'product_group',)
    search_fields = ('product_name',)
    actions = [deactive_product, active_product, export_json_products]
    inlines = [ProductFeatureAdmin, GalleryProductInline]

    def display_product_group(self, obj):
        """Display product groups associated with the product."""
        return ', '.join([item.group_name for item in obj.product_group.all()])
    display_product_group.short_description = 'گروه‌های کالا'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter product group choices to exclude root groups."""
        if db_field.name == 'product_group':
            kwargs['queryset'] = GroupProduct.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
