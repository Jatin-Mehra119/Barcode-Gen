# Bulk barcode generator for A4 sheet printing

from barcode.codex import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw
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

def create_a4_barcode_sheet(start_number, count=65):
    """Create an A4 sheet with multiple barcodes (legacy function for backwards compatibility)"""
    barcode_specs = [{'number': start_number, 'count': count}]
    return create_multi_barcode_sheet(barcode_specs)

def create_multi_barcode_sheet(barcode_specs):
    """Create multiple A4 sheets with different barcodes
    
    Args:
        barcode_specs: List of dictionaries with 'number' and 'count' keys
                      e.g., [{'number': 12345, 'count': 25}, {'number': 67890, 'count': 30}]
    
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
    
    # Generate first barcode to get dimensions
    if not barcode_specs:
        raise ValueError("No barcode specifications provided")
    
    sample_barcode = generate_single_barcode(barcode_specs[0]['number'], options)
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
        for _ in range(count):
            all_barcodes.append(number)
            
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
                
            current_number = all_barcodes[i]
            
            # Generate barcode
            barcode_img = generate_single_barcode(current_number, options)
            
            # Calculate position
            x = start_x + col * (barcode_width + 10)
            y = start_y + row * (barcode_height + 10)
            
            # Paste barcode on canvas
            canvas.paste(barcode_img, (x, y))
            
            print(f"Generated barcode {i+1}/{total_barcodes}: {current_number} (Sheet {sheet_num + 1})")
        
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
