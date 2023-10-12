from django.contrib import admin
from . import models

class InformationAdmin(admin.StackedInline):
    model=models.Information

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("title","price")
    inlines=(InformationAdmin,)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    mptt_indent_field = "title"
    list_display = ('title', 'parent')
    search_fields = ['title', 'parent__title']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Size)
admin.site.register(models.Color)
