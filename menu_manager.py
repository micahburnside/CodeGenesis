
# menu_manager.py

import tkinter as tk
from logger import logger
from tkinter import messagebox

class MenuManager:
    def __init__(self, root):
        """Initialize the MenuManager with the root window."""
        self.root = root
        self._create_menu()

    def _create_menu(self):
        """Create the top-level menu bar with a File dropdown."""
        menubar = tk.Menu(self.root, bg="#1C2526", fg="#FFFFFF", activebackground="#4A5A5B", activeforeground="#E0E6E6")
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1C2526", fg="#FFFFFF", activebackground="#4A5A5B", activeforeground="#E0E6E6")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Preferences", command=self._open_preferences)

    def _open_preferences(self):
        """Placeholder for opening a Preferences dialog."""
        logger.info("Preferences menu opened")
        messagebox.showinfo("Preferences", "Settings dialog coming soon!")
