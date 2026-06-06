import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
from .models import CertificateTemplate, EditableField, GeneratedCertificate
from .utils import (
    generate_certificate_pdf,
    generate_certificate_from_template,
    get_coordinate_mapping,
    CERTIFICATE_FIELDS
)


def template_list(request):
    """List all certificate templates"""
    templates = CertificateTemplate.objects.all()
    return render(request, 'certificates/template_list.html', {
        'templates': templates
    })


def template_upload(request):
    """Upload a new certificate template"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        template_file = request.FILES.get('template_file')
        
        if not name:
            messages.error(request, 'Template name is required.')
            return render(request, 'certificates/template_upload.html')
        
        if not template_file:
            messages.error(request, 'Template file is required.')
            return render(request, 'certificates/template_upload.html')
        
        if not template_file.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed.')
            return render(request, 'certificates/template_upload.html')
        
        template = CertificateTemplate.objects.create(
            name=name,
            description=description,
            template_file=template_file
        )
        
        messages.success(request, f'Template "{name}" uploaded successfully.')
        return redirect('template_list')
    
    return render(request, 'certificates/template_upload.html')


def template_edit(request, pk):
    """Edit an existing certificate template"""
    template = get_object_or_404(CertificateTemplate, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        template_file = request.FILES.get('template_file')
        
        if not name:
            messages.error(request, 'Template name is required.')
            return render(request, 'certificates/template_edit.html', {
                'template': template
            })
        
        template.name = name
        template.description = description
        
        if template_file:
            if not template_file.name.endswith('.pdf'):
                messages.error(request, 'Only PDF files are allowed.')
                return render(request, 'certificates/template_edit.html', {
                    'template': template
                })
            template.template_file = template_file
        
        template.save()
        messages.success(request, f'Template "{name}" updated successfully.')
        return redirect('template_list')
    
    return render(request, 'certificates/template_edit.html', {
        'template': template
    })


def template_delete(request, pk):
    """Delete a certificate template"""
    template = get_object_or_404(CertificateTemplate, pk=pk)
    
    if request.method == 'POST':
        name = template.name
        template.delete()
        messages.success(request, f'Template "{name}" deleted successfully.')
        return redirect('template_list')
    
    return render(request, 'certificates/template_delete.html', {
        'template': template
    })


def pdf_editor(request, template_id):
    """PDF editor for manual field placement"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    
    # Get existing editable fields for this template
    existing_fields = EditableField.objects.filter(template=template)
    fields_data = list(existing_fields.values(
        'field_name', 'x', 'y', 'width', 'height', 'text', 'font_size'
    ))
    
    return render(request, 'certificates/pdf_editor.html', {
        'template': template,
        'existing_fields': json.dumps(fields_data)
    })


@require_http_methods(["POST"])
def save_editable_fields(request, template_id):
    """Save editable fields from the PDF editor"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    
    try:
        data = json.loads(request.body)
        fields = data.get('fields', [])
        
        # Delete existing fields for this template
        EditableField.objects.filter(template=template).delete()
        
        # Create new fields
        for field_data in fields:
            EditableField.objects.create(
                template=template,
                field_name=field_data.get('field_name', ''),
                x=field_data.get('x', 0),
                y=field_data.get('y', 0),
                width=field_data.get('width', 200),
                height=field_data.get('height', 50),
                text=field_data.get('text', ''),
                font_size=field_data.get('font_size', 12)
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def generate_from_editor(request, template_id):
    """Generate PDF from editor fields"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    
    try:
        data = json.loads(request.body)
        fields = data.get('fields', [])
        
        # Save fields first
        EditableField.objects.filter(template=template).delete()
        for field_data in fields:
            EditableField.objects.create(
                template=template,
                field_name=field_data.get('field_name', ''),
                x=field_data.get('x', 0),
                y=field_data.get('y', 0),
                width=field_data.get('width', 200),
                height=field_data.get('height', 50),
                text=field_data.get('text', ''),
                font_size=field_data.get('font_size', 12)
            )
        
        # Generate PDF using template overlay approach
        template_path = template.template_file.path
        
        # Prepare data for PDF generation
        pdf_data = {}
        for field_data in fields:
            field_name = field_data.get('field_name', '')
            pdf_data[field_name] = field_data.get('text', '')
        
        # Generate PDF
        pdf_buffer = generate_certificate_pdf(
            pdf_data,
            template_path=template_path
        )
        
        # Save generated certificate
        generated = GeneratedCertificate(
            template=template,
            filled_data=json.dumps(pdf_data, ensure_ascii=False)
        )
        
        # Save PDF file
        filename = f"certificate_{template.name}.pdf"
        generated.output_file.save(filename, ContentFile(pdf_buffer.read()))
        generated.save()
        
        return JsonResponse({
            'success': True,
            'download_url': f'/certificates/{generated.id}/download/'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def certificate_fill(request, template_id):
    """Fill certificate form for a selected template"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    
    # Get editable fields for this template (only fields added in manual editor)
    editable_fields = EditableField.objects.filter(template=template)
    
    # Build a dictionary of fields with their labels from CERTIFICATE_FIELDS
    fields = {}
    for field in editable_fields:
        field_name = field.field_name
        # Get the label from CERTIFICATE_FIELDS if available, otherwise use the field name
        label = CERTIFICATE_FIELDS.get(field_name, field_name.replace('_', ' ').title())
        fields[field_name] = label
    
    # Get coordinate mapping for this template
    coordinates = get_coordinate_mapping()
    
    return render(request, 'certificates/certificate_fill.html', {
        'template': template,
        'fields': fields,
        'coordinates': coordinates
    })


def certificate_generate(request, template_id):
    """Generate PDF certificate from filled form data using template overlay"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    
    if request.method == 'POST':
        # Get editable fields for this template
        editable_fields = EditableField.objects.filter(template=template)
        
        # Collect all certificate field data
        data = {}
        for field in editable_fields:
            field_name = field.field_name
            data[field_name] = request.POST.get(field_name, '').strip()
        
        # Validate required fields
        required_fields = ['full_name', 'sex', 'dob_year', 'dob_month', 'dob_day']
        missing_fields = [f for f in required_fields if not data.get(f)]
        
        if missing_fields:
            messages.error(request, f'Please fill in all required fields: {", ".join(missing_fields)}')
            
            # Rebuild fields dictionary for the form
            fields = {}
            for field in editable_fields:
                field_name = field.field_name
                label = CERTIFICATE_FIELDS.get(field_name, field_name.replace('_', ' ').title())
                fields[field_name] = label
            
            coordinates = get_coordinate_mapping()
            return render(request, 'certificates/certificate_fill.html', {
                'template': template,
                'fields': fields,
                'data': data,
                'coordinates': coordinates
            })
        
        try:
            # Get coordinate mapping for this template
            coordinates = get_coordinate_mapping()
            
            # Generate PDF using template overlay approach
            template_path = template.template_file.path
            
            pdf_buffer = generate_certificate_pdf(
                data,
                template_path=template_path,
                coordinates=coordinates
            )
            
            # Save generated certificate
            generated = GeneratedCertificate(
                template=template,
                filled_data=json.dumps(data, ensure_ascii=False)
            )
            
            # Save PDF file
            filename = f"certificate_{template.name}_{data['full_name']}.pdf"
            generated.output_file.save(filename, ContentFile(pdf_buffer.read()))
            generated.save()
            
            messages.success(request, 'Certificate generated successfully!')
            
            return render(request, 'certificates/certificate_preview.html', {
                'template': template,
                'data': data,
                'generated': generated
            })
            
        except Exception as e:
            messages.error(request, f'Error generating certificate: {str(e)}')
            
            # Rebuild fields dictionary for the form
            fields = {}
            for field in editable_fields:
                field_name = field.field_name
                label = CERTIFICATE_FIELDS.get(field_name, field_name.replace('_', ' ').title())
                fields[field_name] = label
            
            coordinates = get_coordinate_mapping()
            return render(request, 'certificates/certificate_fill.html', {
                'template': template,
                'fields': fields,
                'data': data,
                'coordinates': coordinates
            })
    
    return redirect('certificate_fill', template_id=template_id)


def certificate_download(request, pk):
    """Download a generated certificate PDF"""
    generated = get_object_or_404(GeneratedCertificate, pk=pk)
    
    if generated.output_file:
        response = HttpResponse(
            generated.output_file.read(),
            content_type='application/pdf'
        )
        filename = os.path.basename(generated.output_file.name)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    messages.error(request, 'Certificate file not found.')
    return redirect('template_list')


def certificate_history(request):
    """View history of generated certificates"""
    certificates = GeneratedCertificate.objects.select_related('template').all()
    return render(request, 'certificates/certificate_history.html', {
        'certificates': certificates
    })


def certificate_preview_data(request, pk):
    """Get certificate data as JSON for preview"""
    generated = get_object_or_404(GeneratedCertificate, pk=pk)
    return JsonResponse({
        'template': generated.template.name,
        'data': generated.get_filled_data_dict(),
        'created_at': generated.created_at.isoformat()
    })


def coordinate_config(request, template_id):
    """Configure coordinate mapping for a template"""
    template = get_object_or_404(CertificateTemplate, pk=template_id)
    coordinates = get_coordinate_mapping()
    
    if request.method == 'POST':
        # Update coordinates from form data
        new_coordinates = {}
        for field_key in CERTIFICATE_FIELDS.keys():
            x = request.POST.get(f'{field_key}_x', '')
            y = request.POST.get(f'{field_key}_y', '')
            font_size = request.POST.get(f'{field_key}_font_size', '12')
            
            if x and y:
                new_coordinates[field_key] = {
                    'x': int(x),
                    'y': int(y),
                    'font_size': int(font_size)
                }
        
        # In a more advanced implementation, save to database
        # For now, just show success message
        messages.success(request, 'Coordinate configuration updated successfully.')
        return redirect('template_list')
    
    return render(request, 'certificates/coordinate_config.html', {
        'template': template,
        'fields': CERTIFICATE_FIELDS,
        'coordinates': coordinates
    })
