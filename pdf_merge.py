#!/usr/bin/env python3

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional


APP_TITLE = "PDF Merger"


class PDFMergerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)

        # State
        self.pdf1_path_var = tk.StringVar()
        self.pdf2_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.merge_order_var = tk.StringVar(value="1_then_2")  # values: "1_then_2" or "2_then_1"

        # Layout
        self._build_layout()

    def _build_layout(self) -> None:
        padding_x = 10
        padding_y = 8

        # Row 0: PDF 1
        lbl_pdf1 = tk.Label(self.root, text="PDF 1:")
        lbl_pdf1.grid(row=0, column=0, sticky="w", padx=padding_x, pady=padding_y)

        ent_pdf1 = tk.Entry(self.root, textvariable=self.pdf1_path_var, width=60)
        ent_pdf1.grid(row=0, column=1, sticky="we", padx=(0, padding_x), pady=padding_y)

        btn_pdf1 = tk.Button(self.root, text="Browse...", command=lambda: self._choose_pdf(self.pdf1_path_var))
        btn_pdf1.grid(row=0, column=2, sticky="e", padx=(0, padding_x), pady=padding_y)

        # Row 1: PDF 2
        lbl_pdf2 = tk.Label(self.root, text="PDF 2:")
        lbl_pdf2.grid(row=1, column=0, sticky="w", padx=padding_x, pady=padding_y)

        ent_pdf2 = tk.Entry(self.root, textvariable=self.pdf2_path_var, width=60)
        ent_pdf2.grid(row=1, column=1, sticky="we", padx=(0, padding_x), pady=padding_y)

        btn_pdf2 = tk.Button(self.root, text="Browse...", command=lambda: self._choose_pdf(self.pdf2_path_var))
        btn_pdf2.grid(row=1, column=2, sticky="e", padx=(0, padding_x), pady=padding_y)

        # Row 2: Merge Order
        lbl_order = tk.Label(self.root, text="Order:")
        lbl_order.grid(row=2, column=0, sticky="w", padx=padding_x, pady=padding_y)

        rdo_12 = tk.Radiobutton(self.root, text="PDF 1 then PDF 2", variable=self.merge_order_var, value="1_then_2", command=self._suggest_output_name)
        rdo_12.grid(row=2, column=1, sticky="w", padx=(0, padding_x), pady=padding_y)

        rdo_21 = tk.Radiobutton(self.root, text="PDF 2 then PDF 1", variable=self.merge_order_var, value="2_then_1", command=self._suggest_output_name)
        rdo_21.grid(row=2, column=2, sticky="w", padx=(0, padding_x), pady=padding_y)

        # Row 3: Output file
        lbl_output = tk.Label(self.root, text="Output:")
        lbl_output.grid(row=3, column=0, sticky="w", padx=padding_x, pady=padding_y)

        ent_output = tk.Entry(self.root, textvariable=self.output_path_var, width=60)
        ent_output.grid(row=3, column=1, sticky="we", padx=(0, padding_x), pady=padding_y)

        btn_output = tk.Button(self.root, text="Save As...", command=self._choose_output)
        btn_output.grid(row=3, column=2, sticky="e", padx=(0, padding_x), pady=padding_y)

        # Row 4: Actions
        btn_merge = tk.Button(self.root, text="Merge PDFs", command=self._on_merge)
        btn_merge.grid(row=4, column=1, sticky="e", padx=(0, padding_x), pady=(padding_y, padding_y))

        btn_reset = tk.Button(self.root, text="Reset", command=self._reset_fields)
        btn_reset.grid(row=4, column=2, sticky="w", padx=(0, padding_x), pady=(padding_y, padding_y))

        # Row 5: Status
        self.status_var = tk.StringVar(value="Ready.")
        lbl_status = tk.Label(self.root, textvariable=self.status_var, anchor="w", fg="#555")
        lbl_status.grid(row=5, column=0, columnspan=3, sticky="we", padx=padding_x, pady=(0, padding_y))

        # Allow column 1 to stretch
        self.root.grid_columnconfigure(1, weight=1)

    def _choose_pdf(self, target_var: tk.StringVar) -> None:
        initial_dir = None
        other_path = self._first_existing([self.pdf1_path_var.get(), self.pdf2_path_var.get()])
        if other_path:
            initial_dir = os.path.dirname(other_path)

        file_path = filedialog.askopenfilename(
            title="Select PDF",
            initialdir=initial_dir,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if file_path:
            target_var.set(file_path)
            self._suggest_output_name()
            self.status_var.set("Selected: " + os.path.basename(file_path))

    def _choose_output(self) -> None:
        suggestion = self._build_output_suggestion()
        initial_dir = os.path.dirname(suggestion) if suggestion else None
        initial_file = os.path.basename(suggestion) if suggestion else "merged.pdf"

        output_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=[("PDF files", "*.pdf")],
        )
        if output_path:
            if not output_path.lower().endswith(".pdf"):
                output_path += ".pdf"
            self.output_path_var.set(output_path)
            self.status_var.set("Output set: " + os.path.basename(output_path))

    def _first_existing(self, paths: list[str]) -> Optional[str]:
        for p in paths:
            if p and os.path.exists(p):
                return p
        return None

    def _sanitize_name(self, name: str) -> str:
        invalid = '<>:"/\\|?*'  # characters invalid on some platforms
        return "".join((ch if ch not in invalid else "_") for ch in name)

    def _build_output_suggestion(self) -> Optional[str]:
        pdf1 = self.pdf1_path_var.get().strip()
        pdf2 = self.pdf2_path_var.get().strip()
        if not pdf1 or not pdf2:
            return None

        base1 = os.path.splitext(os.path.basename(pdf1))[0]
        base2 = os.path.splitext(os.path.basename(pdf2))[0]
        base1 = self._sanitize_name(base1)
        base2 = self._sanitize_name(base2)

        if self.merge_order_var.get() == "1_then_2":
            name = f"merged_{base1}_{base2}.pdf"
        else:
            name = f"merged_{base2}_{base1}.pdf"

        initial_dir = os.path.dirname(pdf1) if os.path.isdir(os.path.dirname(pdf1)) else os.getcwd()
        return os.path.join(initial_dir, name)

    def _suggest_output_name(self) -> None:
        suggestion = self._build_output_suggestion()
        if suggestion and not self.output_path_var.get().strip():
            self.output_path_var.set(suggestion)

    def _reset_fields(self) -> None:
        self.pdf1_path_var.set("")
        self.pdf2_path_var.set("")
        self.output_path_var.set("")
        self.merge_order_var.set("1_then_2")
        self.status_var.set("Ready.")

    def _validate(self) -> tuple[bool, Optional[str]]:
        pdf1 = self.pdf1_path_var.get().strip()
        pdf2 = self.pdf2_path_var.get().strip()
        output_path = self.output_path_var.get().strip()

        if not pdf1 or not pdf2:
            return False, "Please select both input PDFs."
        if not os.path.exists(pdf1):
            return False, "PDF 1 does not exist."
        if not os.path.exists(pdf2):
            return False, "PDF 2 does not exist."
        if os.path.isdir(pdf1) or os.path.isdir(pdf2):
            return False, "Inputs must be files, not directories."
        if os.path.samefile(pdf1, pdf2) if os.path.exists(pdf1) and os.path.exists(pdf2) else False:
            return False, "PDF 1 and PDF 2 must be different files."
        if not pdf1.lower().endswith(".pdf") or not pdf2.lower().endswith(".pdf"):
            return False, "Inputs must be .pdf files."

        if not output_path:
            # Autogenerate suggestion if missing
            suggestion = self._build_output_suggestion() or os.path.join(os.getcwd(), "merged.pdf")
            self.output_path_var.set(suggestion)
            output_path = suggestion

        out_dir = os.path.dirname(output_path) or os.getcwd()
        if not os.path.isdir(out_dir):
            return False, "Output directory does not exist."

        # Disallow writing over an input
        try:
            if (os.path.exists(output_path) and (os.path.samefile(output_path, pdf1) or os.path.samefile(output_path, pdf2))):
                return False, "Output cannot be the same as an input file."
        except Exception:
            # On some filesystems, samefile can raise if paths are not resolvable; ignore here
            pass

        # Confirm overwrite
        if os.path.exists(output_path):
            ok = messagebox.askyesno(APP_TITLE, f"'{os.path.basename(output_path)}' exists. Overwrite?")
            if not ok:
                return False, None

        return True, None

    def _on_merge(self) -> None:
        is_valid, error_message = self._validate()
        if not is_valid:
            if error_message:
                messagebox.showerror(APP_TITLE, error_message)
                self.status_var.set(error_message)
            return

        pdf1 = self.pdf1_path_var.get().strip()
        pdf2 = self.pdf2_path_var.get().strip()
        output_path = self.output_path_var.get().strip()

        # Determine order
        pdfs_in_order = [pdf1, pdf2] if self.merge_order_var.get() == "1_then_2" else [pdf2, pdf1]

        # Lazy-import pypdf so the GUI can still open without it
        try:
            from pypdf import PdfReader, PdfWriter
            from pypdf.errors import PdfReadError
        except Exception:  # noqa: BLE001
            messagebox.showerror(APP_TITLE, "Missing dependency: 'pypdf'.\nInstall with: pip install pypdf")
            self.status_var.set("Missing dependency: pypdf")
            return

        writer = PdfWriter()
        try:
            for input_path in pdfs_in_order:
                # Open file in binary mode to ensure proper reading
                with open(input_path, "rb") as f_in:
                    try:
                        reader = PdfReader(f_in)
                    except PdfReadError as ex:  # type: ignore[name-defined]
                        messagebox.showerror(APP_TITLE, f"Failed to read '{os.path.basename(input_path)}': {ex}")
                        self.status_var.set("Failed to read input PDF")
                        return

                    if getattr(reader, "is_encrypted", False):
                        # Attempt no-password decrypt; most unprotected PDFs will simply not be encrypted
                        try:
                            decrypt_result = reader.decrypt("")  # type: ignore[attr-defined]
                            if decrypt_result == 0:
                                messagebox.showerror(APP_TITLE, f"'{os.path.basename(input_path)}' is encrypted and requires a password.")
                                self.status_var.set("Encrypted PDF not supported without password")
                                return
                        except Exception:
                            messagebox.showerror(APP_TITLE, f"'{os.path.basename(input_path)}' is encrypted and cannot be merged.")
                            self.status_var.set("Encrypted PDF not supported")
                            return

                    for page in reader.pages:
                        writer.add_page(page)

            with open(output_path, "wb") as f_out:
                writer.write(f_out)

            messagebox.showinfo(APP_TITLE, f"Merged PDF saved to:\n{output_path}")
            self.status_var.set("Merge complete.")
        except PermissionError:
            messagebox.showerror(APP_TITLE, "Permission denied when writing the output file.")
            self.status_var.set("Permission denied.")
        except FileNotFoundError:
            messagebox.showerror(APP_TITLE, "One or more files were not found.")
            self.status_var.set("File not found.")
        except Exception as ex:  # noqa: BLE001
            messagebox.showerror(APP_TITLE, f"Unexpected error: {ex}")
            self.status_var.set("Unexpected error.")


def main() -> None:
    root = tk.Tk()
    app = PDFMergerApp(root)
    # Try to pre-suggest output name when both inputs are pre-filled via CLI (if we ever support that)
    root.mainloop()


if __name__ == "__main__":
    main()
