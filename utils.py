# utils.py

import tkinter as tk
from tkinter import ttk

def add_label_entry(parent, label_text, text_var, row):
    """
    Adds a labeled entry widget pair (Label and Entry) to a parent container.

    This function simplifies the process of creating a labeled text input
    field by placing a Label and Entry widget pair in the given parent
    container at the specified row. The Label displays the provided text,
    and the Entry widget is linked to a variable for data input.

    Parameters:
        parent (tk.Widget): The parent container where the Label and Entry pair
            will be added. Typically, a Frame or similar Tkinter widget.
        label_text (str): The text to display on the Label widget.
        text_var (tk.Variable): The Tkinter variable to bind to the Entry widget
            for capturing user input.
        row (int): The row in the grid layout of the parent container where the
            widget pair should be located.

    Returns:
        None
    """
    ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(parent, textvariable=text_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    parent.columnconfigure(1, weight=1)
