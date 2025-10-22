#!/usr/bin/env python3
"""
Utility to merge two PDF files into a single document.

Usage:
  python pdf_merge.py INPUT_1.pdf INPUT_2.pdf -o merged.pdf

Requires the `pypdf` package. Install via:
  pip install -r requirements.txt
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import List

try:
    from pypdf import PdfReader, PdfWriter
except Exception as import_error:  # pragma: no cover - graceful message for missing dependency
    sys.stderr.write(
        "Error: Failed to import 'pypdf'. Install dependencies with 'pip install -r requirements.txt'\n"
    )
    raise


def validate_input_file(pdf_path: str) -> None:
    """Validate that the path points to an existing PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input file not found: {pdf_path}")
    if not os.path.isfile(pdf_path):
        raise ValueError(f"Input path is not a file: {pdf_path}")
    # Basic extension check (not strictly required, but helpful)
    _, ext = os.path.splitext(pdf_path)
    if ext.lower() != ".pdf":
        raise ValueError(f"Input file does not have .pdf extension: {pdf_path}")


def ensure_output_writable(output_path: str, overwrite: bool) -> None:
    """Ensure output path is writable, create parent directories if needed."""
    parent_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(parent_dir, exist_ok=True)
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace it."
        )


def merge_two_pdfs(input_pdf_path_1: str, input_pdf_path_2: str, output_pdf_path: str) -> None:
    """Merge two PDF files in the given order into a single output PDF."""
    validate_input_file(input_pdf_path_1)
    validate_input_file(input_pdf_path_2)

    writer = PdfWriter()

    def _append_pdf(pdf_path: str) -> None:
        reader = PdfReader(pdf_path)
        if getattr(reader, "is_encrypted", False):
            # Do not attempt to decrypt without a password; fail with a clear message
            raise PermissionError(f"PDF is encrypted and cannot be read: {pdf_path}")
        for page in reader.pages:
            writer.add_page(page)

    _append_pdf(input_pdf_path_1)
    _append_pdf(input_pdf_path_2)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge two PDF files into a single document (in order)."
    )
    parser.add_argument("input_pdf_1", help="Path to the first input PDF")
    parser.add_argument("input_pdf_2", help="Path to the second input PDF")
    parser.add_argument(
        "-o",
        "--output",
        default="merged.pdf",
        help="Path to the output PDF (default: merged.pdf)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it already exists",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        ensure_output_writable(args.output, args.overwrite)
        merge_two_pdfs(args.input_pdf_1, args.input_pdf_2, args.output)
    except (FileNotFoundError, FileExistsError, ValueError, PermissionError) as known_error:
        sys.stderr.write(f"Error: {known_error}\n")
        return 2
    except Exception as unexpected_error:  # pragma: no cover - safety net
        sys.stderr.write(f"Unexpected error: {unexpected_error}\n")
        return 1

    print(f"Merged PDF written to: {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
