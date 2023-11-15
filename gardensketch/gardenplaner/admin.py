from django.contrib import admin
from . import models, forms


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_lt', 'description_en', 'description_lt')
    list_filter = ('name_en', 'name_lt')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_lt', 'description_en', 'description_lt')
    list_filter = ('name_en', 'name_lt')


class PlantTimeAdmin(admin.ModelAdmin):
    list_display = ('month_en', 'month_lt', 'first_day', 'last_day')
    list_filter = ('month_en', 'month_lt')


class PlantAdmin(admin.ModelAdmin):
    list_display = (
        'name_en', 'name_lt', 'description_en', 'description_lt',
        'type', 'planting_time', 'display_colors'
        )
    list_filter = ('name_en', 'name_lt', 'type')

    def display_colors(self, obj):
        return ', '.join([color.name_en for color in obj.colors.all()])

# class SelectedPlantAdmin(admin.ModelAdmin):
#     form = forms.ZonePlantForm



# admin.site.register(models.ZonePlant, SelectedPlantAdmin)
admin.site.register(models.Type, TypeAdmin)
admin.site.register(models.Color, ColorAdmin)
admin.site.register(models.PlantTime, PlantTimeAdmin)
admin.site.register(models.Plant, PlantAdmin)
