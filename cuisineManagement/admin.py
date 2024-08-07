from django.contrib import admin
from .models import *

# Register your models here.
class MenuItemImageInline(admin.TabularInline):
    model = MenuItemImage
    extra = 0

class MenuItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category', 'sub_category', 'type']
    inlines = [MenuItemImageInline]
    list_display = ('name', 'category', 'sub_category', 'type', 'price')
    search_fields = ('name', 'description', 'category__name', 'sub_category__name', 'type__name')
    list_filter = ('category', 'sub_category', 'type')

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CuisineTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(CuisineType, CuisineTypeAdmin)
admin.site.register(Ingredient)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuItemImage)