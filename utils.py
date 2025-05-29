# Bulk barcode generator for A4 sheet printing

from barcode.codex import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import io
import os

def generate_single_barcode(number, options):
    """Generate a single barcode and return as PIL Image"""
    writer = ImageWriter()
    writer.format = 'PNG'
    writer.dpi = 300
    
    # Create barcode
    my_code = Code128(str(number), writer=writer)
    
    # Save to memory buffer
    buffer = io.BytesIO()
    my_code.write(buffer, options=options)
    buffer.seek(0)
    
    # Open as PIL Image
    return Image.open(buffer)

def generate_barcode_with_title(number, title, options):
    """Generate a barcode with custom title text on top"""
    # First generate the standard barcode
    barcode_img = generate_single_barcode(number, options)
    
    if not title:
        return barcode_img
    
    # Calculate dimensions for the combined image
    barcode_width, barcode_height = barcode_img.size
      # Try to load a font, fall back to default if not available
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 22)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 22)
        except:
            # Fall back to default font
            font = ImageFont.load_default()
    
    # Create a temporary image to measure text size
    temp_img = Image.new('RGB', (1, 1), 'white')
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Get text bounding box
    bbox = temp_draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Add padding for text
    text_padding = 10
    title_section_height = text_height + (text_padding * 2)
    
    # Create new image with space for title
    combined_width = max(barcode_width, text_width + (text_padding * 2))
    combined_height = barcode_height + title_section_height
    
    combined_img = Image.new('RGB', (combined_width, combined_height), 'white')
    draw = ImageDraw.Draw(combined_img)
    
    # Draw the title text centered at the top
    text_x = (combined_width - text_width) // 2
    text_y = text_padding
    draw.text((text_x, text_y), title, fill='black', font=font)
    
    # Paste the barcode below the title
    barcode_x = (combined_width - barcode_width) // 2
    barcode_y = title_section_height
    combined_img.paste(barcode_img, (barcode_x, barcode_y))
    
    return combined_img

def create_a4_barcode_sheet(start_number, count=65):
    """Create an A4 sheet with multiple barcodes (legacy function for backwards compatibility)"""
    barcode_specs = [{'number': start_number, 'count': count, 'title': ''}]
    sheets = create_multi_barcode_sheet(barcode_specs)
    return sheets[0] if isinstance(sheets, list) else sheets

def create_multi_barcode_sheet(barcode_specs):
    """Create multiple A4 sheets with different barcodes
    
    Args:
        barcode_specs: List of dictionaries with 'number', 'count', and optional 'title' keys
                      e.g., [{'number': 12345, 'count': 25, 'title': 'Product A'}, 
                             {'number': 67890, 'count': 30, 'title': 'Product B'}]
    
    Returns:
        List of PIL Images (one per A4 sheet) or single PIL Image if only one sheet
    """
    
    # A4 dimensions at 300 DPI: 2480 x 3508 pixels
    a4_width = 2480
    a4_height = 3508
    
    # Margins (in pixels at 300 DPI)
    margin_left = 100
    margin_top = 100
    margin_right = 100
    margin_bottom = 100
    
    # Available space for barcodes
    available_width = a4_width - margin_left - margin_right
    available_height = a4_height - margin_top - margin_bottom
    
    # Barcode generation options - smaller for fitting more on page
    options = {
        'module_width': 0.25,  # Reduced width for smaller barcodes
        'module_height': 8.0,  # Reduced height
        'quiet_zone': 3.0,     # Smaller quiet zone
        'font_size': 6,        # Smaller font
        'text_distance': 3.0,  # Less distance
        'background': 'white',
        'foreground': 'black',
    }
      # Generate first barcode to get dimensions (check if it has a title for sizing)
    if not barcode_specs:
        raise ValueError("No barcode specifications provided")
    
    first_spec = barcode_specs[0]
    first_title = first_spec.get('title', '')
    if first_title:
        sample_barcode = generate_barcode_with_title(first_spec['number'], first_title, options)
    else:
        sample_barcode = generate_single_barcode(first_spec['number'], options)
    barcode_width, barcode_height = sample_barcode.size
    
    # Calculate grid layout
    # Try to fit as many as possible while maintaining readability
    cols = available_width // (barcode_width + 10)  # 10px spacing
    rows = available_height // (barcode_height + 10)  # 10px spacing
    barcodes_per_sheet = cols * rows
    
    print(f"Grid layout: {cols}x{rows} = {barcodes_per_sheet} barcodes per sheet")
    print(f"Barcode size: {barcode_width}x{barcode_height} pixels")
    
    # Create all barcodes based on specifications
    all_barcodes = []
    for spec in barcode_specs:
        number = spec['number']
        count = spec['count']
        title = spec.get('title', '')
        for _ in range(count):
            all_barcodes.append({'number': number, 'title': title})
            
    total_barcodes = len(all_barcodes)
    sheets_needed = (total_barcodes + barcodes_per_sheet - 1) // barcodes_per_sheet
    
    print(f"Total barcodes to generate: {total_barcodes}")
    print(f"Sheets needed: {sheets_needed}")
    
    sheets = []
    
    for sheet_num in range(sheets_needed):
        # Create A4 canvas
        canvas = Image.new('RGB', (a4_width, a4_height), 'white')
        
        # Calculate actual spacing to center the grid
        total_grid_width = cols * barcode_width + (cols - 1) * 10
        total_grid_height = rows * barcode_height + (rows - 1) * 10
        
        start_x = margin_left + (available_width - total_grid_width) // 2
        start_y = margin_top + (available_height - total_grid_height) // 2
        
        # Calculate barcode range for this sheet
        start_idx = sheet_num * barcodes_per_sheet
        end_idx = min(start_idx + barcodes_per_sheet, total_barcodes)
        
        # Generate and place barcodes for this sheet
        for i in range(start_idx, end_idx):
            position_on_sheet = i - start_idx
            row = position_on_sheet // cols
            col = position_on_sheet % cols
            if row >= rows:
                break
                
            barcode_data = all_barcodes[i]
            current_number = barcode_data['number']
            current_title = barcode_data['title']
            
            # Generate barcode with or without title
            if current_title:
                barcode_img = generate_barcode_with_title(current_number, current_title, options)
            else:
                barcode_img = generate_single_barcode(current_number, options)
            
            # Calculate position
            x = start_x + col * (barcode_width + 10)
            y = start_y + row * (barcode_height + 10)
            
            # Paste barcode on canvas
            canvas.paste(barcode_img, (x, y))
            
            title_info = f" ('{current_title}')" if current_title else ""
            print(f"Generated barcode {i+1}/{total_barcodes}: {current_number}{title_info} (Sheet {sheet_num + 1})")
        
        sheets.append(canvas)
    
    # Return single sheet if only one, otherwise return list
    return sheets[0] if len(sheets) == 1 else sheets

def save_sheets_as_pdf(sheets, filename):
    """Save multiple sheets as a single PDF file"""
    if not isinstance(sheets, list):
        sheets = [sheets]
    
    if len(sheets) == 1:
        sheets[0].save(filename, format='PDF', dpi=(300, 300))
    else:
        # Save first sheet as PDF and append others
        sheets[0].save(filename, format='PDF', dpi=(300, 300), save_all=True, append_images=sheets[1:])

def main():
    try:
        # Starting number for barcodes
        start_number = 1120000250608
        
        # Number of barcodes to generate
        barcode_count = 65
        
        print("Generating A4 sheet with barcodes...")
        
        # Create the A4 sheet
        a4_sheet = create_a4_barcode_sheet(start_number, barcode_count)
        
        # Save the sheet
        output_file = "a4_barcode_sheet.png"
        a4_sheet.save(output_file, dpi=(300, 300))
        
        print(f"A4 barcode sheet saved as: {output_file}")
        print("The image is ready for high-quality printing!")
        
        # Also create a PDF version for better printing
        try:
            pdf_file = "a4_barcode_sheet.pdf"
            a4_sheet.save(pdf_file, dpi=(300, 300))
            print(f"PDF version saved as: {pdf_file}")
        except Exception as e:
            print(f"Could not create PDF: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
