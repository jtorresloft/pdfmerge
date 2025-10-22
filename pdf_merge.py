#!/usr/bin/env python3
"""
PDF Merger GUI Tool
A simple GUI application to merge two PDF files into one document.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfWriter, PdfReader
    except ImportError:
        raise ImportError("Please install pypdf or PyPDF2: pip install pypdf")


class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Variables to store file paths
        self.pdf1_path = tk.StringVar()
        self.pdf2_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create and layout the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="PDF Merger Tool", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # First PDF selection
        ttk.Label(main_frame, text="First PDF:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pdf1_path, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(main_frame, text="Browse...", command=lambda: self.browse_file(self.pdf1_path)).grid(
            row=1, column=2, pady=5
        )
        
        # Second PDF selection
        ttk.Label(main_frame, text="Second PDF:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pdf2_path, width=50).grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(main_frame, text="Browse...", command=lambda: self.browse_file(self.pdf2_path)).grid(
            row=2, column=2, pady=5
        )
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20
        )
        
        # Output file selection
        ttk.Label(main_frame, text="Output PDF:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(
            row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(main_frame, text="Browse...", command=self.browse_output_file).grid(
            row=4, column=2, pady=5
        )
        
        # Merge button
        merge_btn = ttk.Button(
            main_frame, 
            text="Merge PDFs", 
            command=self.merge_pdfs,
            style='Accent.TButton'
        )
        merge_btn.grid(row=5, column=0, columnspan=3, pady=30)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Info text
        info_text = "Select two PDF files to merge them into a single document."
        ttk.Label(main_frame, text=info_text, foreground="gray").grid(
            row=7, column=0, columnspan=3, pady=(10, 0)
        )
        
    def browse_file(self, path_var):
        """Open file dialog to select a PDF file"""
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            path_var.set(filename)
            self.update_output_path()
            
    def browse_output_file(self):
        """Open file dialog to select output location"""
        filename = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
            
    def update_output_path(self):
        """Auto-suggest output path based on first PDF"""
        if self.pdf1_path.get() and not self.output_path.get():
            input_path = Path(self.pdf1_path.get())
            output_name = input_path.stem + "_merged.pdf"
            output_path = input_path.parent / output_name
            self.output_path.set(str(output_path))
            
    def merge_pdfs(self):
        """Merge the two selected PDFs into one"""
        pdf1 = self.pdf1_path.get()
        pdf2 = self.pdf2_path.get()
        output = self.output_path.get()
        
        # Validation
        if not pdf1 or not pdf2:
            messagebox.showerror("Error", "Please select both PDF files to merge.")
            return
            
        if not os.path.exists(pdf1):
            messagebox.showerror("Error", f"First PDF file not found:\n{pdf1}")
            return
            
        if not os.path.exists(pdf2):
            messagebox.showerror("Error", f"Second PDF file not found:\n{pdf2}")
            return
            
        if not output:
            messagebox.showerror("Error", "Please specify an output file location.")
            return
            
        # Check if output file already exists
        if os.path.exists(output):
            if not messagebox.askyesno(
                "Confirm Overwrite", 
                f"The file '{os.path.basename(output)}' already exists.\n\nDo you want to overwrite it?"
            ):
                return
        
        try:
            self.status_label.config(text="Merging PDFs...", foreground="blue")
            self.root.update()
            
            # Create PDF writer object
            pdf_writer = PdfWriter()
            
            # Read and append first PDF
            with open(pdf1, 'rb') as file1:
                pdf_reader1 = PdfReader(file1)
                for page in pdf_reader1.pages:
                    pdf_writer.add_page(page)
            
            # Read and append second PDF
            with open(pdf2, 'rb') as file2:
                pdf_reader2 = PdfReader(file2)
                for page in pdf_reader2.pages:
                    pdf_writer.add_page(page)
            
            # Write merged PDF to output file
            with open(output, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            self.status_label.config(text="✓ PDFs merged successfully!", foreground="green")
            messagebox.showinfo(
                "Success", 
                f"PDFs merged successfully!\n\nOutput saved to:\n{output}"
            )
            
        except Exception as e:
            self.status_label.config(text="✗ Error occurred", foreground="red")
            messagebox.showerror("Error", f"Failed to merge PDFs:\n\n{str(e)}")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
