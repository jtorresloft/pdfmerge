# PDF Merger GUI Tool

A modern, user-friendly GUI application for merging multiple PDF files into a single document.

## Features

- **Easy File Selection**: Add PDF files through file dialog or drag-and-drop
- **File Management**: Remove individual files or clear all at once
- **Progress Tracking**: Real-time progress bar and status updates
- **Error Handling**: Comprehensive error messages and validation
- **Modern Interface**: Clean, intuitive design using tkinter
- **Threaded Processing**: Non-blocking UI during PDF merging

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python pdf_merge.py
   ```

2. Add PDF files to merge:
   - Click "Add PDFs" to browse for files
   - Or drag and drop PDF files directly onto the window

3. Specify output location:
   - Enter the output file path manually
   - Or click "Browse" to choose a location

4. Click "Merge PDFs" to start the merging process

## Requirements

- Python 3.6+
- PyPDF2 3.0.1
- tkinter (usually included with Python)

## Notes

- The application preserves the order of files as they appear in the list
- You can reorder files by removing and re-adding them in the desired order
- The merged PDF will contain all pages from all selected PDFs in sequence