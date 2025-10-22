#!/usr/bin/env python3
"""
PDF Merger Utility

A simple utility to merge two or more PDF files into a single document.
Supports command-line usage and can be imported as a module.

Usage:
    python pdf_merge.py file1.pdf file2.pdf output.pdf
    python pdf_merge.py -i input1.pdf input2.pdf -o merged.pdf
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("Error: PyPDF2 is required. Install it with: pip install PyPDF2")
    sys.exit(1)


class PDFMerger:
    """A utility class for merging PDF files."""
    
    def __init__(self):
        self.writer = PdfWriter()
    
    def add_pdf(self, file_path: str) -> bool:
        """
        Add a PDF file to the merger.
        
        Args:
            file_path (str): Path to the PDF file to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Error: File '{file_path}' does not exist.")
                return False
            
            if not file_path.suffix.lower() == '.pdf':
                print(f"Error: '{file_path}' is not a PDF file.")
                return False
            
            reader = PdfReader(str(file_path))
            
            # Add all pages from the PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                self.writer.add_page(page)
            
            print(f"Added {len(reader.pages)} pages from '{file_path}'")
            return True
            
        except Exception as e:
            print(f"Error reading '{file_path}': {str(e)}")
            return False
    
    def merge_pdfs(self, input_files: List[str], output_file: str) -> bool:
        """
        Merge multiple PDF files into one.
        
        Args:
            input_files (List[str]): List of PDF file paths to merge
            output_file (str): Path for the output merged PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not input_files:
            print("Error: No input files provided.")
            return False
        
        if len(input_files) < 2:
            print("Error: At least 2 PDF files are required for merging.")
            return False
        
        print(f"Merging {len(input_files)} PDF files...")
        
        # Add each PDF file
        for file_path in input_files:
            if not self.add_pdf(file_path):
                return False
        
        # Write the merged PDF
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as output_file_handle:
                self.writer.write(output_file_handle)
            
            print(f"Successfully merged PDFs into '{output_path}'")
            return True
            
        except Exception as e:
            print(f"Error writing output file '{output_file}': {str(e)}")
            return False
    
    def get_page_count(self) -> int:
        """Get the total number of pages in the merged PDF."""
        return len(self.writer.pages)


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Merge two or more PDF files into a single document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_merge.py file1.pdf file2.pdf output.pdf
  python pdf_merge.py -i doc1.pdf doc2.pdf doc3.pdf -o merged.pdf
  python pdf_merge.py --input *.pdf --output combined.pdf
        """
    )
    
    # Input files argument
    parser.add_argument(
        'input_files',
        nargs='*',
        help='PDF files to merge (positional arguments)'
    )
    
    # Alternative input option
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        dest='input_opt',
        help='PDF files to merge (alternative to positional arguments)'
    )
    
    # Output file argument
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file path'
    )
    
    # Verbose option
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Determine input files
    input_files = args.input_files or args.input_opt or []
    
    if not input_files:
        parser.error("No input files provided. Use positional arguments or -i/--input option.")
    
    # Create merger and merge PDFs
    merger = PDFMerger()
    
    if args.verbose:
        print(f"Input files: {input_files}")
        print(f"Output file: {args.output}")
    
    success = merger.merge_pdfs(input_files, args.output)
    
    if success:
        page_count = merger.get_page_count()
        print(f"Merge completed successfully! Total pages: {page_count}")
        sys.exit(0)
    else:
        print("Merge failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()