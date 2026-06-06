from django.contrib import admin
from .models import CertificateTemplate, EditableField, GeneratedCertificate


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EditableField)
class EditableFieldAdmin(admin.ModelAdmin):
    list_display = ['field_name', 'template', 'x', 'y', 'width', 'height', 'font_size', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['field_name', 'template__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GeneratedCertificate)
class GeneratedCertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['template__name']
    readonly_fields = ['created_at', 'filled_data']
