from django.contrib import admin
from statistics.models import ProfessionalCategory


class ProfessionalCategoryAdmin(admin.ModelAdmin):
    model = ProfessionalCategory
    list_display = ('code', 'name', 'is_cvn_required',)
    readonly_fields = ('code', 'name',)
    ordering = ('name',)

admin.site.register(ProfessionalCategory, ProfessionalCategoryAdmin)
