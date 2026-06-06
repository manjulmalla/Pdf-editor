# Nepali Fonts for Certificate Generation

This directory should contain Nepali Unicode fonts for PDF generation.

## Required Fonts

Place the following font files in this directory:

1. **Mangal.ttf** - Standard Nepali Unicode font (recommended)
2. **Preeti.ttf** - Alternative Nepali font
3. **Kantipur.ttf** - Alternative Nepali font

## How to Obtain Fonts

### Option 1: Download Mangal Font
- Mangal is a standard Windows font located at: `C:\Windows\Fonts\mangal.ttf`
- Copy this file to this directory

### Option 2: Download from Internet
- Search for "Mangal font download" or "Nepali Unicode font download"
- Ensure the font is in TTF format
- Place the downloaded font file in this directory

### Option 3: Use System Fonts
If you're on Windows, the system already has Mangal font. The application will try to use it automatically.

## Font Registration

The application will automatically register the Nepali font when generating PDFs. If no Nepali font is found, it will fall back to the default Helvetica font.

## Troubleshooting

If Nepali text appears as boxes or garbled characters in the generated PDF:
1. Ensure the font file is in this directory
2. Verify the font file is a valid TTF file
3. Check that the font supports Nepali Unicode characters
4. Restart the Django development server after adding fonts
