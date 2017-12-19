from django.contrib import admin
from .models import Category, Career

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Category, CategoryAdmin)

class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Career, CareerAdmin)    


