from django.contrib import admin
from statistics.models import ProfessionalCategory


class ProfessionalCategoryAdmin(admin.ModelAdmin):
    model = ProfessionalCategory


admin.site.register(ProfessionalCategory, ProfessionalCategoryAdmin)
