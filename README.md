# 📊 Multi-Barcode Generator

A comprehensive Streamlit web application for generating bulk barcodes on A4 sheets for printing. Generate different barcode numbers with custom quantities and optional titles, all optimally arranged for professional printing.

## ✨ Features

- 🔢 **Multiple Barcode Types**: Generate different barcode numbers with individual quantities
- 📝 **Custom Titles**: Add optional titles above each barcode for easy identification
- 📊 **Bulk Generation**: Generate multiple sequential barcodes efficiently
- 📄 **High-Quality PDF Output**: Professional 300 DPI PDF ready for printing
- 🖼️ **Live Preview**: See your barcode sheet before downloading
- 📐 **Smart Auto-Layout**: Automatically arranges barcodes to fit A4 sheet optimally
- 💾 **Session Management**: Save and edit your barcode specifications
- 🎯 **Flexible Input**: Support for various barcode number formats

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Steps

1. Clone or download the project to your local machine
2. Navigate to the project directory:
```bash
cd "Barcode Gen"
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### 🌐 Running the Streamlit Web App (Recommended)

1. Navigate to the project directory in your terminal/command prompt
2. Start the Streamlit app:
```bash
streamlit run streamlit_barcode_app.py
```

3. Open your web browser and go to the URL shown in the terminal (usually `http://localhost:8501`)

### 📱 Using the Web Interface

1. **Add Barcodes**: 
   - Enter barcode number, quantity, and optional title
   - Click "Add Barcode" to add to your list
   - Repeat for multiple different barcodes

2. **Manage Your List**:
   - View all added barcodes in the specification table
   - Edit or remove barcodes as needed
   - See total barcode count and estimated sheets

3. **Generate & Download**:
   - Click "Generate Barcodes" to create your sheets
   - Preview the generated layout
   - Download the high-resolution PDF for printing

### ⚡ Command Line Usage (Advanced)

For direct scripting or automation, use the core generator:
```bash
python bulk_barcode_generator.py
```

Or run the test script to see examples:
```bash
python test_app.py
```

## 🔧 Technical Details

- **Output Format**: PDF at 300 DPI for professional printing quality
- **Barcode Type**: Code128 format (industry standard)
- **Sheet Size**: A4 (210mm × 297mm) optimized for standard printers
- **Smart Layout**: Automatically calculates optimal grid layout based on barcode dimensions
- **Multi-Barcode Support**: Generate different barcode numbers with individual quantities
- **Title Support**: Optional custom titles above each barcode
- **Memory Efficient**: Processes large quantities without performance issues

## 📦 Dependencies

The application requires the following Python packages:

- `streamlit>=1.28.0`: Modern web app framework for the user interface
- `python-barcode>=0.15.1`: Professional barcode generation library
- `Pillow>=10.0.0`: Advanced image processing and manipulation
- `pandas>=1.5.0`: Data handling and management

## 📁 Project Structure

```
Barcode Gen/
├── streamlit_barcode_app.py     # Main Streamlit web application
├── bulk_barcode_generator.py    # Core barcode generation engine
├── test_app.py                  # Test script with examples
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
└── test_titles.py               # Title functionality tests
```

## 🎯 Use Cases

- **Inventory Management**: Generate barcodes for product tracking
- **Asset Labeling**: Create labels for equipment and assets
- **Event Management**: Generate ticket or participant barcodes
- **Retail Operations**: Product labeling and price tags
- **Document Tracking**: File and document identification systems

## 🖨️ Printing Tips

1. **Paper Settings**: Use A4 paper size (210mm × 297mm)
2. **Print Quality**: Set to high quality/600 DPI for best results
3. **Margins**: Ensure printer margins don't crop the barcodes
4. **Test Print**: Always do a test print with one sheet first
5. **Scanner Testing**: Test barcodes with your scanner before bulk printing

## 🔍 Example Usage

### Sample Barcode Specifications
```
Barcode: 1120000250608 | Quantity: 25 | Title: "Product A"
Barcode: 1120000250625 | Quantity: 25 | Title: "Product B"  
Barcode: 1120000250808 | Quantity: 36 | Title: "Product C"
```

This would generate a total of 86 barcodes across multiple A4 sheets, with each barcode clearly labeled.

## 🐛 Troubleshooting

### Common Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**Streamlit not starting:**
- Ensure you're in the correct directory
- Check if port 8501 is available
- Try: `streamlit run streamlit_barcode_app.py --server.port 8502`

**PDF not generating:**
- Check available disk space
- Ensure write permissions in the directory
- Verify all required dependencies are installed

**Barcodes not scanning:**
- Check print quality settings
- Ensure adequate contrast (black bars on white background)
- Verify barcode format compatibility with your scanner

## 🚀 Getting Started Quick Guide

1. **Install Python** (if not already installed)
2. **Download/Clone** this project
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run the app**: `streamlit run streamlit_barcode_app.py`
5. **Open browser** to `http://localhost:8501`
6. **Add your barcodes** and generate!

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Made with ❤️ for efficient barcode generation and printing**
