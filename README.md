# Nepali Government Certificate Editor

A Django web application for managing, editing, and generating Nepali government certificates (like citizenship certificates) with full support for both English and Nepali Unicode text.

## Key Features

### Manual PDF Editor (NEW!)
- **Visual PDF Editor** - Display PDF as background image
- **Drag & Drop Text Boxes** - Add, move, resize text boxes directly on PDF
- **Real-time Editing** - Double-click to edit text content
- **English & Nepali Support** - Type in both languages (Unicode)
- **Save Layout** - Save field positions for reuse
- **Preserve Original Template** - Images, seals, signatures remain intact

### PDF Template Management
- Upload template PDFs (original certificate layout)
- List, edit, and delete templates
- Configure exact X, Y coordinates for each field

### Dynamic Form for Filling Certificate
- Input fields for all certificate placeholders
- Support for English and Nepali input
- Input validation and UTF-8 encoding

### PDF Generation
- Use uploaded PDF as background/template
- Overlay text at exact coordinates
- Embed Nepali Unicode font (Mangal.ttf, Kantipur.ttf)
- Output final PDF that matches original template exactly

### Download & Print
- Download generated PDF certificates
- Print preview support
- Save generated certificates for history/auditing

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd snme
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Nepali Font Setup

For proper Nepali text rendering in PDFs, place Nepali Unicode fonts in the `static/fonts/` directory:

1. **Mangal.ttf** - Standard Nepali Unicode font (recommended)
   - On Windows, copy from: `C:\Windows\Fonts\mangal.ttf`

2. **Preeti.ttf** - Alternative Nepali font

3. **Kantipur.ttf** - Alternative Nepali font

See `static/fonts/README.md` for detailed instructions.

## Usage Workflow

### Manual PDF Editor (Recommended)

1. **Upload Template**
   - Navigate to "Upload Template" in the navigation menu
   - Enter a template name and description
   - Upload the original PDF certificate template
   - Click "Upload Template"

2. **Open Manual Editor**
   - Go to "Templates" page
   - Click "✏️ Manual Editor" on your template

3. **Add Text Boxes**
   - Click "➕ Add Text Box" to create a new editable field
   - Drag the text box to position it on the PDF
   - Resize by dragging the corners
   - Double-click to edit text content

4. **Edit Text**
   - Double-click any text box
   - Type text in English or Nepali
   - Adjust font size if needed
   - Click "Save" to apply changes

5. **Save Layout**
   - Click "💾 Save Fields" to save all field positions
   - Fields are saved to database for reuse

6. **Generate PDF**
   - Click "📄 Generate PDF" to create the final certificate
   - System overlays text boxes on original template
   - Download the generated PDF

### Form-Based Approach (Alternative)

1. **Upload Template** (same as above)

2. **Configure Coordinates**
   - Click "📐 Coordinates" on your template
   - Set exact X, Y coordinates for each field
   - Adjust font sizes as needed

3. **Fill Certificate**
   - Click "📝 Form Fill" on your template
   - Fill in all required fields
   - Click "Generate PDF Certificate"

4. **Download/Print**
   - Download the generated PDF
   - Open in print preview

## Manual Editor Features

### Adding Text Boxes
- Click "➕ Add Text Box" button
- A new text box appears on the PDF
- Drag to position it where you want

### Moving Text Boxes
- Click and drag any text box
- Position it exactly where you want on the PDF

### Resizing Text Boxes
- Drag the corners to resize
- Maintain aspect ratio by holding Shift

### Editing Text
- Double-click any text box
- Modal opens with text input
- Type in English or Nepali
- Adjust font size (8-72 points)
- Click "Save" to apply

### Deleting Text Boxes
- Double-click the text box
- Click "Delete" button in the modal
- Text box is removed from canvas

### Saving Layout
- Click "💾 Save Fields" button
- All field positions saved to database
- Layout preserved for future use

### Generating PDF
- Click "📄 Generate PDF" button
- System overlays all text boxes on original template
- Generated PDF preserves original layout
- Download link provided

## Coordinate System

### Understanding Coordinates
- **Origin Point:** (0, 0) is at the bottom-left corner of the PDF
- **X-Axis:** Increases from left to right
- **Y-Axis:** Increases from bottom to top
- **Page Size:** A4 is approximately 595 x 842 points
- **Units:** 1 point = 1/72 inch

### Default Coordinates
These are the default coordinates. Adjust them based on your specific template:

```
full_name: x=150, y=700
sex: x=150, y=680
dob_year: x=150, y=660
dob_month: x=250, y=660
dob_day: x=350, y=660
birth_district: x=150, y=620
birth_vdc: x=150, y=600
birth_ward: x=150, y=580
permanent_district: x=150, y=540
permanent_municipality: x=150, y=520
permanent_ward: x=150, y=500
father_name: x=150, y=460
father_address: x=150, y=440
mother_name: x=150, y=400
mother_address: x=150, y=380
type_of_citizenship: x=150, y=340
certificate_number: x=150, y=320
issued_date: x=150, y=300
issuing_officer_name: x=150, y=260
issuing_officer_designation: x=150, y=240
remarks: x=150, y=200
```

## Project Structure

```
snme/
├── certificate_editor/          # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI application
├── certificates/                # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL routing
│   ├── utils.py                # PDF generation utilities (PyPDF2 + ReportLab)
│   ├── admin.py                # Admin configuration
│   └── templates/              # HTML templates
│       └── certificates/
│           ├── base.html
│           ├── template_list.html
│           ├── template_upload.html
│           ├── template_edit.html
│           ├── template_delete.html
│           ├── certificate_fill.html
│           ├── certificate_preview.html
│           ├── certificate_history.html
│           ├── coordinate_config.html
│           └── pdf_editor.html
├── static/                      # Static files
│   └── fonts/                  # Nepali fonts directory
├── media/                       # Uploaded files
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies (Django, ReportLab, PyPDF2)
└── README.md                    # This file
```

## Database Models

### CertificateTemplate
- `name`: Template name
- `description`: Template description
- `template_file`: Uploaded PDF template
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### EditableField
- `template`: Foreign key to CertificateTemplate
- `field_name`: Name of the field
- `x`: X coordinate in points
- `y`: Y coordinate in points
- `width`: Width of text box in points
- `height`: Height of text box in points
- `text`: Text content
- `font_size`: Font size in points
- `font_name`: Font name for rendering
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### GeneratedCertificate
- `template`: Foreign key to CertificateTemplate
- `filled_data`: JSON field containing all filled certificate fields
- `output_file`: Generated PDF file
- `created_at`: Generation timestamp

## API Endpoints

- `/` - Template list page
- `/templates/upload/` - Upload new template
- `/templates/<id>/edit/` - Edit template
- `/templates/<id>/delete/` - Delete template
- `/templates/<id>/editor/` - Manual PDF editor
- `/templates/<id>/save-fields/` - Save editable fields (JSON)
- `/templates/<id>/generate-from-editor/` - Generate PDF from editor
- `/templates/<id>/fill/` - Fill certificate form
- `/templates/<id>/generate/` - Generate PDF certificate
- `/templates/<id>/coordinates/` - Configure coordinate mapping
- `/certificates/<id>/download/` - Download generated certificate
- `/certificates/<id>/preview/` - View certificate data (JSON)
- `/history/` - View all generated certificates
- `/admin/` - Django admin panel

## Technical Details

### PDF Generation Approach
The application uses **PyPDF2 + ReportLab** to overlay text on the original PDF template:

1. **Read Original Template:** PyPDF2 reads the uploaded PDF template
2. **Create Overlay:** ReportLab creates a new PDF with text at specified coordinates
3. **Merge PDFs:** PyPDF2 merges the overlay with the original template
4. **Preserve Layout:** Original images, seals, signatures, and formatting remain intact
5. **Embed Font:** Nepali Unicode font is embedded for proper character rendering

### Manual Editor Technology
- **PDF.js** - Renders PDF as background image in browser
- **Fabric.js** - Provides drag, resize, and text editing capabilities
- **Canvas Overlay** - Text boxes rendered on canvas layer above PDF
- **AJAX** - Save field positions without page reload

### Dependencies
- **Django 5.2.5** - Web framework
- **ReportLab 4.4.10** - PDF generation and text overlay
- **PyPDF2 3.0.1** - PDF reading and merging
- **Pillow 12.1.1** - Image processing (ReportLab dependency)
- **PDF.js 3.11.174** - PDF rendering in browser (CDN)
- **Fabric.js 5.3.1** - Canvas manipulation (CDN)

## Troubleshooting

### Nepali Text Not Rendering
- Ensure Nepali fonts are placed in `static/fonts/` directory
- Verify font files are valid TTF format
- Restart Django server after adding fonts

### Text Not Aligned Correctly
- Use Manual Editor for visual placement
- Adjust X, Y coordinates in coordinate configuration
- Remember: (0, 0) is at bottom-left corner

### PDF Generation Errors
- Check that all required fields are filled
- Verify template file is a valid PDF
- Check server logs for detailed error messages

### Manual Editor Not Loading
- Ensure internet connection (CDN libraries required)
- Check browser console for JavaScript errors
- Verify PDF.js and Fabric.js loaded correctly

### Database Issues
- Run `python manage.py migrate` to apply migrations
- Delete `db.sqlite3` and re-run migrations if needed

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up proper static file serving
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Configure HTTPS
7. Host PDF.js and Fabric.js locally instead of CDN

## License

This project is for educational and governmental use.

## Support

For issues or questions, please refer to:
- Django: https://docs.djangoproject.com/
- ReportLab: https://www.reportlab.com/docs/reportlab-userguide.pdf
- PyPDF2: https://pypdf2.readthedocs.io/
- PDF.js: https://mozilla.github.io/pdf.js/
- Fabric.js: http://fabricjs.com/
