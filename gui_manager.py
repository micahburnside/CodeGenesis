# gui_manager.py

import tkinter as tk
from tkinter import ttk
from utils import add_label_entry
import os
from tkinter import filedialog

class GuiManager:
    def __init__(self, root, project_name_var, author_var, destination_folder_var, languages, licenses, use_github_var,
                 is_new_project, branch_callback, create_callback, github_available=True):
        self.root = root
        self.project_name_var = project_name_var
        self.author_var = author_var
        self.destination_folder_var = destination_folder_var
        self.languages = languages
        self.licenses = licenses
        self.use_github_var = use_github_var
        self.is_new_project = is_new_project  # Add is_new_project variable
        self.branch_callback = branch_callback
        self.create_callback = create_callback
        self.additional_branches = []
        self.selected_language = tk.StringVar()
        self.selected_license = tk.StringVar()
        self.is_private_repo = tk.BooleanVar(value=False)
        self.github_available = github_available
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        style = tk.ttk.Style()
        style.theme_use('default')
        style.configure("TFrame", background="#1C2526")
        style.configure("Header.TLabel", font=("Orbitron", 14, "bold"), foreground="#FFFFFF", background="#1C2526")
        style.configure("TLabel", font=("Helvetica", 10), foreground="#E0E6E6", background="#1C2526")
        style.configure("TEntry", fieldbackground="#2E3839", foreground="#FFFFFF", insertcolor="#FFFFFF")
        style.configure("TButton", font=("Orbitron", 12, "bold"), foreground="#FFFFFF", background="#3A4A4B",
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", "#4A5A5B")], foreground=[("active", "#E0E6E6")])
        style.configure("TCheckbutton", font=("Helvetica", 10), foreground="#E0E6E6", background="#1C2526")
        style.configure("Separator.TSeparator", background="#3A4A4B")
        style.configure("TCombobox", fieldbackground="#2E3839", foreground="#FFFFFF", background="#3A4A4B")

    def _create_widgets(self):
        # Project Details Section
        project_frame = tk.Frame(self.root, bg="#1C2526")
        project_frame.pack(pady=20, padx=20, fill='x')
        tk.Label(project_frame, text="PROJECT PARAMETERS", font=("Orbitron", 14, "bold"),
                 fg="#FFFFFF", bg="#1C2526").grid(row=0, column=0, columnspan=3, sticky='w')
        add_label_entry(project_frame, "Project Name", self.project_name_var, 1)
        add_label_entry(project_frame, "Author", self.author_var, 2)

        tk.Label(project_frame, text="Destination Folder", font=("Helvetica", 10), fg="#E0E6E6",
                 bg="#1C2526").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(project_frame, textvariable=self.destination_folder_var, width=40).grid(row=3, column=1, padx=5,
                                                                                         pady=5)
        tk.Button(project_frame, text="Browse", command=self.select_folder).grid(row=3, column=2, padx=5, pady=5)

        # New Project Checkbox
        tk.Checkbutton(project_frame, text="New Project (create new directory)", variable=self.is_new_project,
                       font=("Helvetica", 10), fg="#E0E6E6", bg="#1C2526", selectcolor="#1C2526",
                       activebackground="#1C2526", activeforeground="white").grid(row=4, column=0, columnspan=3,
                                                                                  sticky='w', padx=5, pady=5)

        # Core Branches Section
        core_branches_frame = tk.Frame(self.root, bg="#1C2526")
        core_branches_frame.pack(pady=10, padx=20)
        tk.Label(core_branches_frame, text="CORE BRANCHES", font=("Orbitron", 14, "bold"),
                 fg="#FFFFFF", bg="#1C2526").pack(anchor='w')
        for branch in ["main (empty)", "dev (initial files)", "staging (empty)"]:
            tk.Label(core_branches_frame, text=branch, fg="#E0E6E6", bg="#1C2526").pack(anchor='w', padx=10, pady=2)

        # Additional Branches Section
        additional_branches_frame = tk.Frame(self.root, bg="#1C2526")
        additional_branches_frame.pack(pady=10, padx=20)
        tk.Label(additional_branches_frame, text="FEATURE BRANCHES", font=("Orbitron", 14, "bold"),
                 fg="#FFFFFF", bg="#1C2526").pack(anchor='w')
        self.branch_entries_frame = tk.Frame(additional_branches_frame, bg="#1C2526")
        self.branch_entries_frame.pack(fill='x')
        tk.Button(additional_branches_frame, text="+ ADD BRANCH", command=self.add_branch).pack(pady=5)

        # Separator
        tk.Frame(self.root, height=2, bg="#3A4A4B").pack(fill='x', pady=10)

        # Language Selection Section
        languages_frame = tk.Frame(self.root, bg="#1C2526")
        languages_frame.pack(pady=10, padx=20)
        tk.Label(languages_frame, text="LANGUAGE MODULE", font=("Orbitron", 14, "bold"),
                 fg="#FFFFFF", bg="#1C2526").pack(anchor='w')
        self.language_combo = tk.ttk.Combobox(languages_frame, textvariable=self.selected_language,
                                              values=list(self.languages), state="readonly", height=10)
        self.language_combo.pack(anchor='w', padx=10, pady=5)
        self.language_combo.set("Select a language")

        # License Selection Section
        licenses_frame = tk.Frame(self.root, bg="#1C2526")
        licenses_frame.pack(pady=10, padx=20)
        tk.Label(licenses_frame, text="LICENSE", font=("Orbitron", 14, "bold"),
                 fg="#FFFFFF", bg="#1C2526").pack(anchor='w')
        self.license_combo = tk.ttk.Combobox(licenses_frame, textvariable=self.selected_license,
                                             values=list(self.licenses.keys()), state="readonly", height=10)
        self.license_combo.pack(anchor='w', padx=10, pady=5)
        self.license_combo.set("Select a license")

        # GitHub Option
        github_frame = tk.Frame(self.root, bg="#1C2526")
        github_frame.pack(pady=10, padx=20)
        github_checkbox = tk.ttk.Checkbutton(github_frame, text="Deploy to GitHub", variable=self.use_github_var,
                                             state="normal" if self.github_available else "disabled")
        github_checkbox.pack(anchor='w')

        # Repository Privacy Options (Public/Private)
        repo_type_frame = tk.Frame(github_frame, bg="#1C2526")
        repo_type_frame.pack(anchor='w', padx=20)
        self.public_radio = tk.ttk.Radiobutton(
            repo_type_frame, text="Public", variable=self.is_private_repo, value=False
        )
        self.private_radio = tk.ttk.Radiobutton(
            repo_type_frame, text="Private", variable=self.is_private_repo, value=True
        )
        self.public_radio.pack(side="left", padx=5)
        self.private_radio.pack(side="left", padx=5)

        # Control radio button state
        self.update_repo_type_state()
        self.use_github_var.trace("w", self.update_repo_type_state)

        if not self.github_available:
            tk.Label(github_frame, text="GitHub credentials not set", fg="red", bg="#1C2526").pack(anchor='w')

        # Create Project Button
        create_button_frame = tk.Frame(self.root, bg="#1C2526")
        create_button_frame.pack(pady=30)
        tk.Button(create_button_frame, text="LAUNCH PROJECT", command=self.create_callback,
                  font=("Orbitron", 12, "bold"), fg="#FFFFFF", bg="#3A4A4B", bd=0, padx=5).pack()

    def select_folder(self):
        initial_dir = self.destination_folder_var.get() or os.getcwd()
        folder_selected = filedialog.askdirectory(initialdir=initial_dir)
        if folder_selected:
            self.destination_folder_var.set(folder_selected)

    def add_branch(self):
        branch_var = tk.StringVar()
        self.additional_branches.append(branch_var)
        frame = tk.Frame(self.branch_entries_frame, bg="#1C2526")
        frame.pack(fill='x', pady=2)
        tk.Entry(frame, textvariable=branch_var, width=20).pack(side="left", padx=5)
        tk.Button(frame, text="REMOVE", command=lambda f=frame, v=branch_var: self.remove_branch(f, v)).pack(
            side="left", padx=5)
        self.branch_callback(self.additional_branches)

    def remove_branch(self, frame, branch_var):
        frame.destroy()
        if branch_var in self.additional_branches:
            self.additional_branches.remove(branch_var)
        self.branch_callback(self.additional_branches)

    def get_additional_branches(self):
        return [var.get().strip() for var in self.additional_branches if var.get().strip()]

    def get_selected_language(self):
        return self.selected_language.get() if self.selected_language.get() != "Select a language" else None

    def get_selected_license(self):
        return self.selected_license.get() if self.selected_license.get() != "Select a license" else None

    def update_repo_type_state(self, *args):
        state = "normal" if self.use_github_var.get() and self.github_available else "disabled"
        self.public_radio.config(state=state)
        self.private_radio.config(state=state)

    def get_repo_privacy(self):
        return self.is_private_repo.get()