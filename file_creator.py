
# file_creator.py
import os
from logger import logger

class FileCreator:
    def __init__(self, project_path, author):
        self.project_path = project_path
        self.author = author
        from github_manager import GitHubManager
        self.github = GitHubManager()

    def create_directory(self):
        try:
            os.makedirs(self.project_path, exist_ok=True)
            logger.info(f"Created directory: {self.project_path}")
        except Exception as e:
            logger.error(f"Failed to create directory {self.project_path}: {e}")
            raise

    def create_gitignore(self, languages):
        gitignore_path = os.path.join(self.project_path, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write("# Auto-generated .gitignore\n")
                f.write("# .NET Debug and Build Outputs\n")
                f.write("bin/\nobj/\n*.dll\n*.exe\n*.pdb\n*.deps.json\n*.runtimeconfig.json\n")
                f.write("\n# IDE Files\n.idea/\n*.sln.iml\n")
                f.write("\n# Language-specific ignore\n")
                for lang in languages:
                    gitignore_content = self.github.get_gitignore_template(lang)
                    if gitignore_content:
                        f.write(f"\n# {lang} specific ignore\n{gitignore_content}")
                    else:
                        f.write(f"# {lang} (template not found)\n")
            logger.info(f"Created .gitignore at {gitignore_path}")
        else:
            logger.info(f"Skipped .gitignore creation; file already exists at {gitignore_path}")

    def create_license(self, license_key="mit"):  # New method
        license_path = os.path.join(self.project_path, "LICENSE")
        if not os.path.exists(license_path):
            license_content = self.github.get_license_content(license_key)
            if license_content:
                with open(license_path, "w") as f:
                    f.write(license_content.replace("[year]", "2025").replace("[fullname]", self.author))
                logger.info(f"Created {license_key.upper()} license at {license_path}")
            else:
                logger.warning(f"Failed to fetch {license_key} license; using fallback")
                with open(license_path, "w") as f:
                    f.write(f"MIT License\n\nCopyright (c) 2025 {self.author}\n")
                logger.info(f"Created fallback MIT license at {license_path}")
        else:
            logger.info(f"Skipped LICENSE creation; file already exists at {license_path}")

    def create_readme(self, project_name):
        readme_path = os.path.join(self.project_path, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w") as f:
                f.write(f"# {project_name}\n\nCreated by {self.author}\n")
            logger.info(f"Created README.md at {readme_path}")
        else:
            logger.info(f"Skipped README.md creation; file already exists at {readme_path}")