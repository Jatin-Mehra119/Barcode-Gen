#!/usr/bin/env python3
"""
Test script for the updated multi-barcode generator with titles
"""

from utils import create_multi_barcode_sheet, save_sheets_as_pdf

def test_barcode_with_titles():
    """Test generating barcodes with custom titles"""
    print("Testing barcode generation with titles...")
    
    # Test specifications with titles
    barcode_specs = [
        {'number': 1120000250608, 'count': 3, 'title': 'Product A'},
        {'number': 45678, 'count': 2, 'title': 'Product B'},
        {'number': 7885526, 'count': 2, 'title': 'Special Item'}
    ]
    
    try:
        # Generate the barcode sheets
        sheets = create_multi_barcode_sheet(barcode_specs)
        
        # Ensure sheets is always a list
        if not isinstance(sheets, list):
            sheets = [sheets]
        
        print(f"✅ Successfully generated {len(sheets)} sheet(s)")
        
        # Save as PDF
        output_file = "test_barcodes_with_titles.pdf"
        save_sheets_as_pdf(sheets, output_file)
        
        print(f"✅ Saved as: {output_file}")
        print("Test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_barcode_without_titles():
    """Test generating barcodes without titles (backward compatibility)"""
    print("\nTesting backward compatibility (no titles)...")
    
    barcode_specs = [
        {'number': 1120000250608, 'count': 2},
        {'number': 45678, 'count': 2}
    ]
    
    try:
        sheets = create_multi_barcode_sheet(barcode_specs)
        
        if not isinstance(sheets, list):
            sheets = [sheets]
        
        print(f"✅ Successfully generated {len(sheets)} sheet(s) without titles")
        
        # Save as PDF
        output_file = "test_barcodes_no_titles.pdf"
        save_sheets_as_pdf(sheets, output_file)
        
        print(f"✅ Saved as: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Multi-Barcode Generator with Titles")
    print("=" * 50)
    
    success1 = test_barcode_with_titles()
    success2 = test_barcode_without_titles()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The barcode generator is working correctly.")
        print("\nYou can now run the Streamlit app with:")
        print("streamlit run streamlit_barcode_app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
