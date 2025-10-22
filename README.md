# PDF Merger Utility

A simple and efficient Python utility to merge two or more PDF files into a single document.

## Features

- Merge multiple PDF files into one
- Command-line interface with flexible input options
- Error handling and validation
- Support for both positional and named arguments
- Verbose output option
- Cross-platform compatibility

## Installation

1. Install the required dependency:
```bash
pip install -r requirements.txt
```

Or install PyPDF2 directly:
```bash
pip install PyPDF2
```

## Usage

### Command Line

#### Basic usage (positional arguments):
```bash
python pdf_merge.py file1.pdf file2.pdf output.pdf
```

#### Using input option:
```bash
python pdf_merge.py -i file1.pdf file2.pdf file3.pdf -o merged.pdf
```

#### Merge all PDFs in current directory:
```bash
python pdf_merge.py -i *.pdf -o combined.pdf
```

#### Verbose output:
```bash
python pdf_merge.py -i file1.pdf file2.pdf -o output.pdf -v
```

### As a Python Module

```python
from pdf_merge import PDFMerger

# Create a merger instance
merger = PDFMerger()

# Add PDF files
merger.add_pdf("file1.pdf")
merger.add_pdf("file2.pdf")

# Merge and save
merger.merge_pdfs(["file1.pdf", "file2.pdf"], "output.pdf")
```

## Command Line Options

- `input_files`: PDF files to merge (positional arguments)
- `-i, --input`: PDF files to merge (alternative to positional arguments)
- `-o, --output`: Output PDF file path (required)
- `-v, --verbose`: Enable verbose output
- `-h, --help`: Show help message

## Examples

1. **Merge two PDFs:**
   ```bash
   python pdf_merge.py document1.pdf document2.pdf merged_document.pdf
   ```

2. **Merge multiple PDFs with verbose output:**
   ```bash
   python pdf_merge.py -i doc1.pdf doc2.pdf doc3.pdf -o final.pdf -v
   ```

3. **Merge all PDFs in a directory:**
   ```bash
   python pdf_merge.py -i *.pdf -o all_documents.pdf
   ```

## Error Handling

The utility includes comprehensive error handling for:
- Missing input files
- Invalid file paths
- Non-PDF files
- Corrupted PDF files
- Write permission issues
- Insufficient input files (requires at least 2 PDFs)

## Requirements

- Python 3.6+
- PyPDF2 3.0.1

## License

This utility is provided as-is for educational and personal use.