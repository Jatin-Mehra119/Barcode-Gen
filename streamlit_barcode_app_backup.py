import streamlit as st
import io
import tempfile
import os
import time
from utils import create_a4_barcode_sheet

def main():
    st.set_page_config(
        page_title="Barcode Generator",
        page_icon="📊",
        layout="centered"
    )
    
    st.title("📊 Bulk Barcode Generator")
    st.markdown("Generate multiple barcodes on an A4 sheet for printing")
    
    # Create input form
    with st.form("barcode_form"):
        st.subheader("Barcode Settings")
          # Barcode number input
        start_number = st.number_input(
            "Barcode Number:",
            min_value=1,
            max_value=999999999999999,
            value=1120000250608,
            step=1,
            help="Enter the barcode number (all generated barcodes will have this same number)"
        )
        
        # Number of barcodes input
        barcode_count = st.number_input(
            "Number of Barcodes:",
            min_value=1,
            max_value=100,
            value=65,
            step=1,
            help="How many barcodes to generate (maximum depends on A4 sheet capacity)"
        )
        
        # Generate button
        generate_button = st.form_submit_button("🔄 Generate Barcodes", use_container_width=True)
    
    # Process form submission
    if generate_button:
        with st.spinner("Generating barcodes..."):
            try:                # Generate the barcode sheet
                a4_sheet = create_a4_barcode_sheet(int(start_number), int(barcode_count))
                
                # Create temporary file for PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file_path = tmp_file.name
                
                # Save as PDF (outside the context manager to ensure file is closed)
                a4_sheet.save(tmp_file_path, format='PDF', dpi=(300, 300))
                
                # Read the PDF file
                with open(tmp_file_path, 'rb') as f:
                    pdf_data = f.read()
                  # Clean up temporary file
                try:
                    time.sleep(0.1)  # Small delay to ensure file is released
                    os.unlink(tmp_file_path)
                except PermissionError:
                    # If we can't delete it immediately, it will be cleaned up by the OS later
                    pass
                
                # Success message
                st.success(f"✅ Successfully generated {barcode_count} barcodes!")
                  # Display preview (convert to PNG for web display)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_png:
                    tmp_png_path = tmp_png.name
                
                # Create a smaller version for preview
                preview_img = a4_sheet.copy()
                preview_img.thumbnail((800, 1200), Image.Resampling.LANCZOS)
                preview_img.save(tmp_png_path, format='PNG')
                
                # Display preview
                st.subheader("📋 Preview")
                st.image(tmp_png_path, caption=f"A4 sheet with {barcode_count} barcodes", use_column_width=True)
                  # Clean up
                try:
                    time.sleep(0.1)  # Small delay to ensure file is released
                    os.unlink(tmp_png_path)
                except PermissionError:
                    # If we can't delete it immediately, it will be cleaned up by the OS later
                    pass
                  # Download button for PDF
                st.subheader("📥 Download")
                filename = f"barcodes_{start_number}_{barcode_count}_copies.pdf"
                
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                  # Display barcode range
                st.info(f"📊 Generated {barcode_count} copies of barcode: {start_number}")
                
            except Exception as e:
                st.error(f"❌ Error generating barcodes: {str(e)}")
                st.exception(e)
    
    # Instructions
    st.markdown("---")
    st.subheader("📖 Instructions")
    st.markdown("""    1. **Enter the barcode number** - This number will be used for all generated barcodes
    2. **Choose how many barcodes** you want to generate
    3. **Click Generate** to create your A4 barcode sheet
    4. **Download the PDF** for high-quality printing
      #### 💡 Tips:
    - The app automatically arranges barcodes to fit optimally on an A4 sheet
    - Generated PDFs are print-ready at 300 DPI resolution
    - Maximum barcodes per sheet depends on the barcode size and A4 dimensions
    - All barcodes will have the same number (no incrementation)
    """)

if __name__ == "__main__":
    # Import PIL here to avoid issues if not installed
    try:
        from PIL import Image
        main()
    except ImportError:
        st.error("❌ PIL (Pillow) library is required. Please install it with: pip install Pillow")
