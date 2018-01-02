from django.contrib import admin

from import_export.widgets import ForeignKeyWidget
from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin
from import_export import fields

from .models import Category, Career, Task

class CareerResource(ModelResource):
	category = fields.Field(
		        column_name='category',
		        attribute='category',
		        widget=ForeignKeyWidget(Category, 'id'))
	class Meta:
		model = Career

	def for_delete(self, row, instance):
		return self.fields['name'].clean(row) == ''
	
class TaskResource(ModelResource):
	career = fields.Field(
		        column_name='career',
		        attribute='career',
		        widget=ForeignKeyWidget(Career, 'id'))
	class Meta:
		model = Task

	def for_delete(self, row, instance):
		return self.fields['task'].clean(row) == ''

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Category, CategoryAdmin)

class CareerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'slug']
    resource_class = CareerResource
admin.site.register(Career, CareerAdmin)    

class TaskAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['task', 'task_type']
    resource_class = TaskResource
admin.site.register(Task, TaskAdmin)   