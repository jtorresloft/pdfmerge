#!/usr/bin/env python3
"""
PDF Merge Utility
A simple utility to merge two PDF documents into one.
"""

import sys
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs(pdf1_path: str, pdf2_path: str, output_path: str) -> None:
    """
    Merge two PDF files into a single PDF document.
    
    Args:
        pdf1_path: Path to the first PDF file
        pdf2_path: Path to the second PDF file
        output_path: Path where the merged PDF will be saved
    
    Raises:
        FileNotFoundError: If either input PDF doesn't exist
        Exception: If there's an error reading or writing PDFs
    """
    # Validate input files exist
    if not Path(pdf1_path).exists():
        raise FileNotFoundError(f"First PDF not found: {pdf1_path}")
    if not Path(pdf2_path).exists():
        raise FileNotFoundError(f"Second PDF not found: {pdf2_path}")
    
    try:
        # Create PDF writer object
        pdf_writer = PdfWriter()
        
        # Read and add pages from first PDF
        print(f"Reading {pdf1_path}...")
        pdf1_reader = PdfReader(pdf1_path)
        for page_num in range(len(pdf1_reader.pages)):
            page = pdf1_reader.pages[page_num]
            pdf_writer.add_page(page)
        print(f"  Added {len(pdf1_reader.pages)} pages from first PDF")
        
        # Read and add pages from second PDF
        print(f"Reading {pdf2_path}...")
        pdf2_reader = PdfReader(pdf2_path)
        for page_num in range(len(pdf2_reader.pages)):
            page = pdf2_reader.pages[page_num]
            pdf_writer.add_page(page)
        print(f"  Added {len(pdf2_reader.pages)} pages from second PDF")
        
        # Write merged PDF to output file
        print(f"Writing merged PDF to {output_path}...")
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        
        total_pages = len(pdf1_reader.pages) + len(pdf2_reader.pages)
        print(f"✓ Successfully merged {total_pages} pages into {output_path}")
        
    except Exception as e:
        raise Exception(f"Error merging PDFs: {str(e)}")


def main():
    """Main entry point for the PDF merge utility."""
    parser = argparse.ArgumentParser(
        description="Merge two PDF documents into one.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document1.pdf document2.pdf merged.pdf
  %(prog)s /path/to/first.pdf /path/to/second.pdf output.pdf
        """
    )
    
    parser.add_argument(
        'pdf1',
        help='Path to the first PDF file'
    )
    parser.add_argument(
        'pdf2',
        help='Path to the second PDF file'
    )
    parser.add_argument(
        'output',
        help='Path for the merged output PDF file'
    )
    
    args = parser.parse_args()
    
    try:
        merge_pdfs(args.pdf1, args.pdf2, args.output)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
