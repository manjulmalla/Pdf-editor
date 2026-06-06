from django.db import models
import json


class CertificateTemplate(models.Model):
    """Model for storing certificate template PDFs"""
    name = models.CharField(max_length=255, help_text="Name of the certificate template")
    description = models.TextField(blank=True, help_text="Description of the template")
    template_file = models.FileField(
        upload_to="certificate_templates/",
        help_text="Upload PDF template for manual field placement"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Certificate Template"
        verbose_name_plural = "Certificate Templates"

    def __str__(self):
        return self.name


class EditableField(models.Model):
    """Model for storing editable text fields on a certificate template"""
    template = models.ForeignKey(
        CertificateTemplate,
        on_delete=models.CASCADE,
        related_name="editable_fields"
    )
    field_name = models.CharField(
        max_length=255,
        help_text="Name of the field (e.g., full_name, sex, dob)"
    )
    x = models.FloatField(help_text="X coordinate in points")
    y = models.FloatField(help_text="Y coordinate in points")
    width = models.FloatField(help_text="Width of the text box in points")
    height = models.FloatField(help_text="Height of the text box in points")
    text = models.TextField(
        blank=True,
        default="",
        help_text="Text content for this field"
    )
    font_size = models.IntegerField(default=12, help_text="Font size in points")
    font_name = models.CharField(
        max_length=255,
        default="Mangal.ttf",
        help_text="Font name for rendering"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['field_name']
        verbose_name = "Editable Field"
        verbose_name_plural = "Editable Fields"

    def __str__(self):
        return f"{self.field_name} - {self.template.name}"


class GeneratedCertificate(models.Model):
    """Model for storing generated certificates"""
    template = models.ForeignKey(
        CertificateTemplate,
        on_delete=models.CASCADE,
        related_name="generated_certificates"
    )
    filled_data = models.JSONField(
        help_text="JSON data containing all filled certificate fields"
    )
    output_file = models.FileField(
        upload_to="generated_certificates/",
        help_text="Generated PDF certificate file"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Generated Certificate"
        verbose_name_plural = "Generated Certificates"

    def __str__(self):
        return f"Certificate {self.id} - {self.template.name}"

    def get_filled_data_dict(self):
        """Return filled data as a dictionary"""
        if isinstance(self.filled_data, str):
            return json.loads(self.filled_data)
        return self.filled_data
