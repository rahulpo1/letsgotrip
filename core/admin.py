from django.contrib import admin
from .models import CustomUser, TourPackage
from django.contrib.auth.admin import UserAdmin

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'is_approved', 'expiry_date')
    list_filter = ('is_approved',)
    search_fields = ('title', 'vendor__username')
    list_editable = ('is_approved',)

admin.site.register(CustomUser, UserAdmin)
