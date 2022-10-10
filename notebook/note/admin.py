from django.contrib import admin
from .models import Inscription, Category

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'reader',)
    search_fields = ('title','category__name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_inscriptions',)

admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Category, CategoryAdmin)

