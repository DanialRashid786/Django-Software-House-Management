from django.contrib import admin

from django.contrib.admin.sites import site
from assets_management.models import Asset

# Register your models here.

class assets_management(admin.ModelAdmin):
    list_display=('asset_name','asset_type', 'purchase_date','purchase_price','serial_number','date_created')

admin.site.register(Asset, assets_management)   


