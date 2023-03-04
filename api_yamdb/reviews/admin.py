from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Genre, Title, User


class TitleInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    search_fields = ('description',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    list_editable = ('category',)
    model = Genre
    inlines = [TitleInline, ]


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
