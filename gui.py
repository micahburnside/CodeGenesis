# gui.py

import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from file_creator import FileCreator
from git_manager import GitManager
from github_manager import GitHubManager
from logger import logger
from menu_manager import MenuManager
from gui_manager import GuiManager


class ProjectCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeGenesis - Project Creator")
        self.root.geometry("500x800")
        self.root.configure(bg="#1C2526")
        self.project_name = tk.StringVar()
        self.author = tk.StringVar()
        self.destination_folder = tk.StringVar(value=os.getcwd())
        self.use_github = tk.BooleanVar()
        self.is_new_project = tk.BooleanVar(value=True)  # New checkbox variable, default to True (new project)
        self.additional_branches = []
        self.github = GitHubManager()
        github_available = self.github.is_available
        if not github_available:
            messagebox.showwarning("GitHub Credentials Missing", "GitHub credentials not set. Please configure .env.")
        self.languages = self.github.get_language_templates() or []
        license_list = self.github.get_license_templates() if github_available else [
            {"key": "mit", "name": "MIT License"}]
        self.licenses = {lic["key"]: lic["name"] for lic in license_list}
        self.menu_manager = MenuManager(self.root)
        self.gui_manager = GuiManager(self.root, self.project_name, self.author, self.destination_folder,
                                      self.languages, self.licenses, self.use_github, self.is_new_project,
                                      self._update_branches, self.create_project, github_available)

    def _update_branches(self, branches):
        self.additional_branches = branches

    def validate_input(self):
        project_name = self.project_name.get().strip()
        author = self.author.get().strip()
        destination_folder = self.destination_folder.get().strip()
        selected_lang = self.gui_manager.get_selected_language()
        selected_license = self.gui_manager.get_selected_license() or "mit"
        additional_branches = self.gui_manager.get_additional_branches()
        if not all([project_name, author, destination_folder, selected_lang]):
            messagebox.showerror("CodeGenesis Error", "All fields (name, author, folder, language) are required!")
            return None, None, None, None, None, None
        if any(" " in b for b in additional_branches):
            messagebox.showerror("CodeGenesis Error", "Branch names cannot contain spaces!")
            return None, None, None, None, None, None
        return project_name, author, destination_folder, selected_lang, selected_license, additional_branches

    def create_project(self):
        project_name, author, destination_folder, selected_lang, selected_license, additional_branches = self.validate_input()
        if not project_name:
            return
        local_name = os.path.basename(destination_folder)

        # Determine project_path based on is_new_project checkbox
        if self.is_new_project.get():
            project_path = os.path.join(destination_folder, project_name)  # New project: create subfolder
            if not os.path.exists(project_path):
                try:
                    os.makedirs(project_path, exist_ok=True)
                    logger.info(f"Created new project directory at '{project_path}'")
                except OSError as e:
                    messagebox.showerror("CodeGenesis Error", f"Failed to create directory '{project_path}': {e}")
                    logger.error(f"Failed to create directory '{project_path}': {e}")
                    return
        else:
            project_path = destination_folder  # Existing project: use destination_folder directly
            if not os.path.exists(project_path):
                messagebox.showerror("CodeGenesis Error",
                                     f"Directory '{project_path}' does not exist for existing project!")
                logger.error(f"Directory '{project_path}' does not exist for existing project")
                return

        final_name = project_name
        repo_url = None

        if self.use_github.get() and self.github.is_available:
            repo_name = project_name
            while True:
                response = messagebox.askyesno("GitHub Repository Name",
                                               f"Use '{repo_name}' as GitHub repo name?\n'No' uses '{local_name}'.")
                if not response:
                    repo_name = local_name
                logger.info(f"Selected GitHub repo name: {repo_name}")
                if self.github.check_repository_exists(repo_name):
                    overwrite = messagebox.askyesno("Repository Exists",
                                                    f"'{repo_name}' exists. Overwrite it? (Deletes existing repo!)")
                    if overwrite:
                        self.github.delete_repository(repo_name)
                        logger.info(f"Deleted existing GitHub repository '{repo_name}'")
                        break
                    else:
                        new_name = simpledialog.askstring("New Repository Name",
                                                          "Enter a new GitHub repo name (or cancel to skip):",
                                                          parent=self.root)
                        if not new_name or not new_name.strip():
                            messagebox.showwarning("CodeGenesis Warning", "GitHub setup skipped")
                            final_name = local_name
                            break
                        repo_name = new_name.strip()
                        continue
                break
            if repo_name:
                repo_url = self.github.create_repository(repo_name, default_branch="main",
                                                         private=self.gui_manager.get_repo_privacy())
                final_name = repo_name

        git = GitManager(project_path)
        if not git.setup_project(repo_url, "main", "dev", "staging", additional_branches):
            messagebox.showerror("CodeGenesis Error", "Git setup failed!")
            return

        file_creator = FileCreator(project_path, author)
        file_creator.create_gitignore([selected_lang])
        file_creator.create_license(selected_license)
        file_creator.create_readme(final_name)
        logger.info("Project files created successfully")

        if not git.finalize_project(repo_url, "dev", additional_branches):
            messagebox.showerror("CodeGenesis Error", "Failed to finalize Git setup!")
            return

        if repo_url:
            privacy_str = "private" if self.gui_manager.get_repo_privacy() else "public"
            pushed_branches = ["dev"] + additional_branches
            logger.info(f"Project pushed to GitHub: {repo_url} as {privacy_str} (pushed: {', '.join(pushed_branches)})")
            messagebox.showinfo("CodeGenesis Success", f"Project pushed to {repo_url} ({privacy_str})\n"
                                                       f"Pushed branches: {', '.join(pushed_branches)}\n"
                                                       f"Local-only: main (empty), staging (empty)")
        messagebox.showinfo("CodeGenesis Success", f"Project initialized at '{project_path}'! Current branch: dev")