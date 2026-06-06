from django.urls import path
from . import views

urlpatterns = [
    # Template management
    path('', views.template_list, name='template_list'),
    path('templates/upload/', views.template_upload, name='template_upload'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # PDF Editor (manual field placement)
    path('templates/<int:template_id>/editor/', views.pdf_editor, name='pdf_editor'),
    path('templates/<int:template_id>/save-fields/', views.save_editable_fields, name='save_editable_fields'),
    path('templates/<int:template_id>/generate-from-editor/', views.generate_from_editor, name='generate_from_editor'),
    
    # Certificate generation (form-based)
    path('templates/<int:template_id>/fill/', views.certificate_fill, name='certificate_fill'),
    path('templates/<int:template_id>/generate/', views.certificate_generate, name='certificate_generate'),
    
    # Coordinate configuration
    path('templates/<int:template_id>/coordinates/', views.coordinate_config, name='coordinate_config'),
    
    # Generated certificates
    path('certificates/<int:pk>/download/', views.certificate_download, name='certificate_download'),
    path('certificates/<int:pk>/preview/', views.certificate_preview_data, name='certificate_preview_data'),
    path('history/', views.certificate_history, name='certificate_history'),
]
