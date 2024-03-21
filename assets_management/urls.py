from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('assetslist/', list_assets, name='assets'),
    path('add-assets/', add_asset, name='addassets'),

    path('update_data/<int:pk>/', update_data, name='asset_update_data'),

    path('delete_data/<id>/', delete_data, name='asset_delete_data'),

    
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)