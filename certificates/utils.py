"""
PDF Generation Utility for Nepali Government Certificates
Uses PyPDF2 + ReportLab to overlay text on original PDF template
Supports both English and Nepali Unicode text
"""

import os
import re
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from django.conf import settings


# Certificate field placeholders
CERTIFICATE_FIELDS = {
    'full_name': 'Full Name',
    'sex': 'Sex',
    'dob_year': 'Year of Birth',
    'dob_month': 'Month of Birth',
    'dob_day': 'Day of Birth',
    'birth_district': 'Birth District',
    'birth_vdc': 'Birth VDC/Municipality',
    'birth_ward': 'Birth Ward Number',
    'permanent_district': 'Permanent District',
    'permanent_municipality': 'Permanent Municipality/VDC',
    'permanent_ward': 'Permanent Ward Number',
    'father_name': "Father's Name",
    'father_address': "Father's Address",
    'mother_name': "Mother's Name",
    'mother_address': "Mother's Address",
    'type_of_citizenship': 'Type of Citizenship',
    'issued_date': 'Issued Date',
    'issuing_officer_name': 'Issuing Officer Name',
    'issuing_officer_designation': 'Issuing Officer Designation',
    'certificate_number': 'Certificate Number',
    'remarks': 'Remarks',
}

# Default coordinate mapping for certificate fields
# These coordinates are in points (1 point = 1/72 inch)
# Adjust these based on your specific certificate template
DEFAULT_COORDINATES = {
    'full_name': {'x': 150, 'y': 700, 'font_size': 12},
    'sex': {'x': 150, 'y': 680, 'font_size': 12},
    'dob_year': {'x': 150, 'y': 660, 'font_size': 12},
    'dob_month': {'x': 250, 'y': 660, 'font_size': 12},
    'dob_day': {'x': 350, 'y': 660, 'font_size': 12},
    'birth_district': {'x': 150, 'y': 620, 'font_size': 12},
    'birth_vdc': {'x': 150, 'y': 600, 'font_size': 12},
    'birth_ward': {'x': 150, 'y': 580, 'font_size': 12},
    'permanent_district': {'x': 150, 'y': 540, 'font_size': 12},
    'permanent_municipality': {'x': 150, 'y': 520, 'font_size': 12},
    'permanent_ward': {'x': 150, 'y': 500, 'font_size': 12},
    'father_name': {'x': 150, 'y': 460, 'font_size': 12},
    'father_address': {'x': 150, 'y': 440, 'font_size': 12},
    'mother_name': {'x': 150, 'y': 400, 'font_size': 12},
    'mother_address': {'x': 150, 'y': 380, 'font_size': 12},
    'type_of_citizenship': {'x': 150, 'y': 340, 'font_size': 12},
    'certificate_number': {'x': 150, 'y': 320, 'font_size': 12},
    'issued_date': {'x': 150, 'y': 300, 'font_size': 12},
    'issuing_officer_name': {'x': 150, 'y': 260, 'font_size': 12},
    'issuing_officer_designation': {'x': 150, 'y': 240, 'font_size': 12},
    'remarks': {'x': 150, 'y': 200, 'font_size': 10},
}


def get_nepali_font_path():
    """Get the path to Nepali font file"""
    # Try to find Nepali font in static directory
    font_paths = [
        os.path.join(settings.STATIC_ROOT, 'fonts', 'Mangal.ttf'),
        os.path.join(settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else '', 'fonts', 'Mangal.ttf'),
        os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Mangal.ttf'),
    ]
    
    for path in font_paths:
        if path and os.path.exists(path):
            return path
    
    # Return None if no font found (will use default font)
    return None


def register_nepali_font():
    """Register Nepali Unicode font with ReportLab"""
    font_path = get_nepali_font_path()
    
    if font_path:
        try:
            pdfmetrics.registerFont(TTFont('NepaliFont', font_path))
            return 'NepaliFont'
        except Exception as e:
            print(f"Warning: Could not register Nepali font: {e}")
    
    # Fallback to default font
    return 'Helvetica'


def extract_placeholders(template_content):
    """Extract all placeholders from template content"""
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, template_content)


def replace_placeholders(text, data):
    """Replace placeholders in text with actual data"""
    for key, value in data.items():
        placeholder = '{{' + key + '}}'
        text = text.replace(placeholder, str(value))
    return text


def generate_certificate_pdf(data, template_path=None, output_path=None, coordinates=None):
    """
    Generate a PDF certificate by overlaying text on original template
    
    Args:
        data: Dictionary containing certificate field values
        template_path: Path to template PDF (required for overlay approach)
        output_path: Path to save generated PDF
        coordinates: Dictionary mapping field names to {x, y, font_size} coordinates
    
    Returns:
        BytesIO object containing PDF data if output_path is None
        None if output_path is provided (saves to file)
    """
    if not template_path:
        raise ValueError("Template path is required for overlay-based PDF generation")
    
    # Use provided coordinates or defaults
    if coordinates is None:
        coordinates = DEFAULT_COORDINATES
    
    # Register Nepali font
    font_name = register_nepali_font()
    
    # Read the original PDF template
    template_pdf = PdfReader(template_path)
    writer = PdfWriter()
    
    # Process each page of the template
    for page_number, page in enumerate(template_pdf.pages):
        # Create overlay PDF with text
        packet = BytesIO()
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Create canvas with same dimensions as template page
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Set font
        can.setFont(font_name, 12)
        
        # Overlay text at exact coordinates
        for field_key, field_value in data.items():
            if field_key in coordinates:
                coord = coordinates[field_key]
                x = coord.get('x', 150)
                y = coord.get('y', 700)
                font_size = coord.get('font_size', 12)
                
                # Set font size for this field
                can.setFont(font_name, font_size)
                
                # Draw the text value
                can.drawString(x, y, str(field_value))
        
        can.save()
        
        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        
        # Read the overlay PDF
        overlay_pdf = PdfReader(packet)
        
        # Merge the overlay with the template page
        page.merge_page(overlay_pdf.pages[0])
        
        # Add the merged page to the writer
        writer.add_page(page)
    
    # Save or return the final PDF
    if output_path:
        with open(output_path, "wb") as f:
            writer.write(f)
        return None
    else:
        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        return buffer


def generate_certificate_from_template(template_file, data, output_path=None, coordinates=None):
    """
    Generate certificate by overlaying data on template PDF
    
    Args:
        template_file: Template PDF file object or path
        data: Dictionary containing certificate field values
        output_path: Path to save generated PDF
        coordinates: Dictionary mapping field names to coordinates
    
    Returns:
        BytesIO object containing PDF data if output_path is None
        None if output_path is provided (saves to file)
    """
    return generate_certificate_pdf(
        data, 
        template_path=template_file, 
        output_path=output_path,
        coordinates=coordinates
    )


def get_coordinate_mapping():
    """
    Get the default coordinate mapping for certificate fields
    This can be customized per template in the future
    """
    return DEFAULT_COORDINATES.copy()


def update_coordinate_mapping(template_id, new_coordinates):
    """
    Update coordinate mapping for a specific template
    This allows customization of text placement per template
    
    Args:
        template_id: ID of the template
        new_coordinates: Dictionary mapping field names to coordinates
    """
    # This could be stored in the database in a more advanced implementation
    # For now, we'll just return the new coordinates
    return new_coordinates
