#!/usr/bin/env python3
"""
Test script for the multi-barcode generator functionality
"""

from bulk_barcode_generator import create_multi_barcode_sheet, save_sheets_as_pdf

def test_multi_barcode_generation():
    """Test the multi-barcode generation functionality"""
    print("Testing multi-barcode generation...")
    
    # Test data similar to what the user requested
    barcode_specs = [
        {'number': 12345, 'count': 25},
        {'number': 45678, 'count': 25},
        {'number': 7885526, 'count': 36}
    ]
    
    try:
        # Generate the barcode sheets
        print("Generating barcode sheets...")
        sheets = create_multi_barcode_sheet(barcode_specs)
        
        # Ensure sheets is always a list
        if not isinstance(sheets, list):
            sheets = [sheets]
        
        print(f"Generated {len(sheets)} sheet(s)")
        
        # Save as PDF
        output_filename = "test_multi_barcodes.pdf"
        print(f"Saving to {output_filename}...")
        save_sheets_as_pdf(sheets, output_filename)
        
        total_barcodes = sum(spec['count'] for spec in barcode_specs)
        print(f"✅ Success! Generated {total_barcodes} barcodes across {len(sheets)} sheet(s)")
        print(f"📄 Output saved as: {output_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_multi_barcode_generation()
