# Barcode Generator App

A Streamlit web application for generating bulk barcodes on A4 sheets for printing.

## Features

- 🔢 **Custom Starting Number**: Enter any starting barcode number
- 📊 **Bulk Generation**: Generate multiple sequential barcodes
- 📄 **PDF Output**: High-quality PDF ready for printing
- 🖼️ **Live Preview**: See your barcode sheet before downloading
- 📐 **Auto Layout**: Automatically arranges barcodes to fit A4 sheet optimally

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Streamlit App

1. Navigate to the project directory
2. Run the Streamlit app:
```bash
streamlit run streamlit_barcode_app.py
```

3. Open your web browser and go to the URL shown in the terminal (usually `http://localhost:8501`)

### Using the App

1. **Enter Starting Barcode Number**: Input the first barcode number you want
2. **Set Number of Barcodes**: Choose how many sequential barcodes to generate
3. **Click Generate**: The app will create your barcode sheet
4. **Preview**: View the generated A4 sheet layout
5. **Download PDF**: Get the high-resolution PDF for printing

### Command Line Usage (Original Script)

You can still use the original script directly:
```bash
python bulk_barcode_generator.py
```

## Technical Details

- **Output Format**: PDF at 300 DPI for high-quality printing
- **Barcode Type**: Code128 format
- **Sheet Size**: A4 (210mm × 297mm)
- **Auto-fitting**: Calculates optimal grid layout based on barcode dimensions
- **Sequential Numbers**: Each barcode increments from the starting number

## Dependencies

- `streamlit`: Web app framework
- `python-barcode`: Barcode generation library
- `Pillow (PIL)`: Image processing library

## File Structure

- `streamlit_barcode_app.py`: Main Streamlit web application
- `bulk_barcode_generator.py`: Core barcode generation functions
- `requirements.txt`: Python dependencies
- `README.md`: This documentation file
