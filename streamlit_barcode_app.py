import streamlit as st
import io
import tempfile
import os
import time
import pandas as pd
from bulk_barcode_generator import create_multi_barcode_sheet, save_sheets_as_pdf

def main():
    st.set_page_config(
        page_title="Multi-Barcode Generator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Multi-Barcode Generator")
    st.markdown("Generate multiple different barcodes on A4 sheets for printing")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Barcode Specifications")
        
        # Initialize session state for barcode list
        if 'barcode_list' not in st.session_state:
            st.session_state.barcode_list = [
                {'number': '1120000250608', 'count': 25},
                {'number': '45678', 'count': 25},
                {'number': '7885526', 'count': 36}
            ]
        
        # Form for adding new barcodes
        with st.form("add_barcode_form"):
            st.markdown("**Add New Barcode:**")
            add_col1, add_col2, add_col3 = st.columns([2, 1, 1])
            
            with add_col1:
                new_barcode = st.text_input(
                    "Barcode Number:",
                    placeholder="e.g., 1120000250608",
                    key="new_barcode"
                )
            
            with add_col2:
                new_count = st.number_input(
                    "Quantity:",
                    min_value=1,
                    max_value=500,
                    value=25,
                    step=1,
                    key="new_count"
                )
            
            with add_col3:
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                add_button = st.form_submit_button("➕ Add", use_container_width=True)
        
        # Add barcode to list
        if add_button and new_barcode:
            st.session_state.barcode_list.append({
                'number': new_barcode,
                'count': new_count
            })
            st.rerun()
        
        # Display current barcode list
        st.markdown("**Current Barcode List:**")
        if st.session_state.barcode_list:
            # Create DataFrame for display
            df = pd.DataFrame(st.session_state.barcode_list)
            df.index = df.index + 1  # Start index from 1
            df.columns = ['Barcode Number', 'Quantity']
            
            # Display as table with actions
            for idx, row in df.iterrows():
                cols = st.columns([2, 1, 1])
                with cols[0]:
                    st.text(f"{idx}. {row['Barcode Number']}")
                with cols[1]:
                    st.text(f"Qty: {row['Quantity']}")
                with cols[2]:
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete this barcode"):
                        st.session_state.barcode_list.pop(idx - 1)
                        st.rerun()
            
            # Summary
            total_barcodes = sum(item['count'] for item in st.session_state.barcode_list)
            st.info(f"📊 **Total barcodes to generate:** {total_barcodes}")
            
        else:
            st.warning("No barcodes added yet. Add some barcodes to generate.")
    
    with col2:
        st.subheader("⚙️ Settings & Actions")
        
        # Clear all button
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.barcode_list = []
            st.rerun()
        
        # Load sample data button
        if st.button("📝 Load Sample Data", use_container_width=True):
            st.session_state.barcode_list = [
                {'number': '1120000250608', 'count': 25},
                {'number': '1120000250625', 'count': 25},
                {'number': '1120000250808', 'count': 36}
            ]
            st.rerun()
        
        st.markdown("---")
        
        # Generate button
        generate_button = st.button(
            "🔄 Generate Barcodes", 
            use_container_width=True,
            type="primary",
            disabled=len(st.session_state.barcode_list) == 0
        )
    
    # Process form submission
    if generate_button and st.session_state.barcode_list:
        with st.spinner("Generating barcodes..."):
            try:
                # Prepare barcode specifications
                barcode_specs = [
                    {'number': int(item['number']), 'count': int(item['count'])}
                    for item in st.session_state.barcode_list
                ]
                
                # Generate the barcode sheets
                sheets = create_multi_barcode_sheet(barcode_specs)
                
                # Ensure sheets is always a list
                if not isinstance(sheets, list):
                    sheets = [sheets]
                
                # Create temporary file for PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file_path = tmp_file.name
                
                # Save as PDF
                save_sheets_as_pdf(sheets, tmp_file_path)
                
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
                total_barcodes = sum(item['count'] for item in st.session_state.barcode_list)
                st.success(f"✅ Successfully generated {total_barcodes} barcodes on {len(sheets)} sheet(s)!")
                
                # Display previews
                st.subheader("📋 Preview")
                
                for i, sheet in enumerate(sheets[:3]):  # Show max 3 sheets for performance
                    # Display preview (convert to PNG for web display)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_png:
                        tmp_png_path = tmp_png.name
                    
                    # Create a smaller version for preview
                    preview_img = sheet.copy()
                    preview_img.thumbnail((600, 800), Image.Resampling.LANCZOS)
                    preview_img.save(tmp_png_path, format='PNG')
                    
                    # Display preview
                    st.image(tmp_png_path, caption=f"Sheet {i+1} of {len(sheets)}", use_column_width=True)
                    
                    # Clean up
                    try:
                        time.sleep(0.1)
                        os.unlink(tmp_png_path)
                    except PermissionError:
                        pass
                
                if len(sheets) > 3:
                    st.info(f"Showing preview of first 3 sheets. Total sheets: {len(sheets)}")
                
                # Download button for PDF
                st.subheader("📥 Download")
                filename = f"multi_barcodes_{len(st.session_state.barcode_list)}_types_{total_barcodes}_total.pdf"
                
                st.download_button(
                    label=f"📄 Download PDF ({len(sheets)} sheet{'s' if len(sheets) > 1 else ''})",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Display summary
                st.markdown("---")
                st.subheader("📊 Generation Summary")
                summary_df = pd.DataFrame(st.session_state.barcode_list)
                summary_df.columns = ['Barcode Number', 'Quantity Generated']
                st.dataframe(summary_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error generating barcodes: {str(e)}")
                st.exception(e)
    
    # Instructions
    st.markdown("---")
    st.subheader("📖 Instructions")
    st.markdown("""
    ### How to use this Multi-Barcode Generator:
    
    1. **Add Barcodes**: Enter each barcode number and specify how many copies you need
    2. **Review List**: Check your barcode list in the table above
    3. **Generate**: Click "Generate Barcodes" to create your PDF
    4. **Download**: Get your multi-page PDF with all barcodes organized efficiently
    
    #### 💡 Features:
    - **Multiple barcode types**: Each barcode number can have a different quantity
    - **Multi-page support**: Automatically creates multiple A4 sheets as needed
    - **Optimal layout**: Barcodes are arranged efficiently on each sheet
    - **High quality**: Generated PDFs are print-ready at 300 DPI resolution
    - **Batch processing**: Generate hundreds of barcodes in one go
    
    #### 📋 Example Input:
    ```
    Barcode 1: 1120000250608, Quantity: 25
    Barcode 2: 45678, Quantity: 25  
    Barcode 3: 7885526, Quantity: 36
    ```
    
    This will generate **86 total barcodes** across multiple sheets as needed.
    """)

if __name__ == "__main__":
    # Import PIL here to avoid issues if not installed
    try:
        from PIL import Image
        main()
    except ImportError:
        st.error("❌ PIL (Pillow) library is required. Please install it with: pip install Pillow")
