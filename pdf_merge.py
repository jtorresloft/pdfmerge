#!/usr/bin/env python3
"""
PDF Merger GUI Tool
A modern GUI application for merging PDF files using tkinter and PyPDF2.
"""

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception as e:
    print("tkinter is required but not installed.")
    print("On Debian/Ubuntu: sudo apt-get update && sudo apt-get install -y python3-tk")
    sys.exit(1)
import os
import sys
from pathlib import Path
import threading
from typing import List, Optional

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("PyPDF2 not found. Please install it with: pip install PyPDF2")
    sys.exit(1)

# Optional drag-and-drop support via tkinterdnd2
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False
    DND_FILES = None  # type: ignore
    TkinterDnD = None  # type: ignore


class PDFMergerGUI:
    def __init__(self, root, dnd_enabled: bool = False):
        self.root = root
        self.dnd_enabled = dnd_enabled
        self.root.title("PDF Merger Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # PDF files list
        self.pdf_files: List[str] = []
        
        # Create GUI
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Configure ttk styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Action.TButton', padding=(10, 5))
        style.configure('Danger.TButton', padding=(10, 5))
        
        # Configure frame styles
        style.configure('Card.TFrame', relief='raised', borderwidth=1)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Merger Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Instructions
        instructions_text = "Select PDF files to merge."
        if self.dnd_enabled:
            instructions_text += " Drag and drop is supported."
        instructions = ttk.Label(main_frame, text=instructions_text, font=('Arial', 10))
        instructions.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="PDF Files", padding="10")
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(1, weight=1)
        
        # File list with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=8, selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # File operations frame
        file_ops_frame = ttk.Frame(file_frame)
        file_ops_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        file_ops_frame.columnconfigure(0, weight=1)
        file_ops_frame.columnconfigure(1, weight=1)
        file_ops_frame.columnconfigure(2, weight=1)
        
        # Add files button
        self.add_files_btn = ttk.Button(file_ops_frame, text="Add PDFs", 
                                       command=self.add_files, style='Action.TButton')
        self.add_files_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        # Remove file button
        self.remove_file_btn = ttk.Button(file_ops_frame, text="Remove Selected", 
                                         command=self.remove_file, style='Danger.TButton')
        self.remove_file_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Clear all button
        self.clear_all_btn = ttk.Button(file_ops_frame, text="Clear All", 
                                       command=self.clear_all, style='Danger.TButton')
        self.clear_all_btn.grid(row=0, column=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Output settings frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        output_frame.columnconfigure(1, weight=1)
        
        # Output file selection
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=40)
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_output_btn = ttk.Button(output_frame, text="Browse", 
                                           command=self.browse_output)
        self.browse_output_btn.grid(row=0, column=2, sticky=tk.W)
        
        # Merge button
        self.merge_btn = ttk.Button(main_frame, text="Merge PDFs", 
                                   command=self.start_merge, style='Action.TButton')
        self.merge_btn.grid(row=4, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to merge PDFs")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, sticky=tk.W)
        
        # Configure drag and drop (if available)
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality if supported"""
        if not self.dnd_enabled:
            return
        def drop(event):
            files = self.root.tk.splitlist(event.data)
            pdf_files = [f for f in files if f.lower().endswith('.pdf')]
            if pdf_files:
                self.add_files_from_list(pdf_files)
            else:
                messagebox.showwarning("Invalid Files", "Please drop PDF files only.")
        
        # Enable drag and drop on the file listbox for better UX
        try:
            self.file_listbox.drop_target_register(DND_FILES)  # type: ignore[arg-type]
            self.file_listbox.dnd_bind('<<Drop>>', drop)
        except Exception:
            # As a fallback, attempt to bind at the root level
            try:
                self.root.drop_target_register(DND_FILES)  # type: ignore[arg-type]
                self.root.dnd_bind('<<Drop>>', drop)
            except Exception:
                # If DnD setup fails, silently disable it
                self.dnd_enabled = False
    
    def add_files(self):
        """Add PDF files through file dialog"""
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if files:
            self.add_files_from_list(files)
    
    def add_files_from_list(self, files: List[str]):
        """Add files from a list to the file listbox"""
        for file_path in files:
            if file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                filename = os.path.basename(file_path)
                self.file_listbox.insert(tk.END, filename)
        
        self.update_merge_button_state()
    
    def remove_file(self):
        """Remove selected file from the list"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            del self.pdf_files[index]
            self.update_merge_button_state()
    
    def clear_all(self):
        """Clear all files from the list"""
        self.file_listbox.delete(0, tk.END)
        self.pdf_files.clear()
        self.update_merge_button_state()
    
    def browse_output(self):
        """Browse for output file location"""
        file_path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path_var.set(file_path)
    
    def update_merge_button_state(self):
        """Update merge button state based on current conditions"""
        has_files = len(self.pdf_files) >= 2
        has_output = bool(self.output_path_var.get().strip())
        self.merge_btn.config(state=tk.NORMAL if has_files and has_output else tk.DISABLED)
    
    def start_merge(self):
        """Start the PDF merging process in a separate thread"""
        if len(self.pdf_files) < 2:
            messagebox.showerror("Error", "Please select at least 2 PDF files to merge.")
            return
        
        if not self.output_path_var.get().strip():
            messagebox.showerror("Error", "Please specify an output file path.")
            return
        
        # Disable merge button during operation
        self.merge_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Merging PDFs...")
        
        # Start merge in separate thread
        thread = threading.Thread(target=self.merge_pdfs)
        thread.daemon = True
        thread.start()
    
    def merge_pdfs(self):
        """Merge PDF files"""
        try:
            output_path = self.output_path_var.get()
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Initialize PDF writer
            pdf_writer = PdfWriter()
            total_pages = 0
            
            # Count total pages for progress tracking
            for file_path in self.pdf_files:
                try:
                    reader = PdfReader(file_path)
                    total_pages += len(reader.pages)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Error", f"Could not read {os.path.basename(file_path)}: {str(e)}"))
                    return
            
            # Merge PDFs
            processed_pages = 0
            for i, file_path in enumerate(self.pdf_files):
                try:
                    reader = PdfReader(file_path)
                    
                    # Add all pages from current PDF
                    for page in reader.pages:
                        pdf_writer.add_page(page)
                        processed_pages += 1
                        
                        # Update progress
                        progress = (processed_pages / total_pages) * 100
                        self.root.after(0, lambda p=progress: self.progress_var.set(p))
                        self.root.after(0, lambda f=os.path.basename(file_path): 
                                      self.status_var.set(f"Processing {f}..."))
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Error", f"Error processing {os.path.basename(file_path)}: {str(e)}"))
                    return
            
            # Write merged PDF
            self.root.after(0, lambda: self.status_var.set("Writing merged PDF..."))
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            # Success
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_var.set("PDFs merged successfully!"))
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", f"PDFs merged successfully!\nOutput saved to: {output_path}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Merge failed: {str(e)}"))
        finally:
            # Re-enable merge button
            self.root.after(0, lambda: self.merge_btn.config(state=tk.NORMAL))


def main():
    """Main function to run the application"""
    # Use TkinterDnD.Tk when available to enable drag-and-drop
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()  # type: ignore[assignment]
    else:
        root = tk.Tk()
    app = PDFMergerGUI(root, dnd_enabled=DND_AVAILABLE)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()