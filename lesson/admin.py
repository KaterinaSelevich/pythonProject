from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Team)

admin.site.register(models.Comment)
admin.site.register(models.Profile)

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'team_type', 'publish')
    list_filter = ('team_type', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields  = {'slug': ('title', )}
    ordering = ('team_type', 'title')
