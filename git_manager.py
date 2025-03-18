# git_manager.py

import subprocess
import shlex
from logger import logger

class GitManager:
    def __init__(self, project_path):
        self.project_path = project_path

    def run_command(self, command):
        if isinstance(command, str):
            command = shlex.split(command)
        try:
            result = subprocess.run(
                command,
                check=True,
                text=True,
                cwd=self.project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info(f"Command succeeded: '{' '.join(command)}'")
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing command '{' '.join(command)}': {e.stderr}")
            return False

    def initialize_repo(self):
        return self.run_command("git init")

    def set_remote(self, url):
        return self.run_command(f"git remote add origin {url}")

    def fetch_remote(self):
        return self.run_command("git fetch origin")

    def setup_branches(self, main_branch, dev_branch, staging_branch, feature_branches=None):
        if feature_branches is None:
            feature_branches = []
        if not self.run_command(f"git checkout {main_branch}"):
            return False
        if not self.run_command(f"git checkout -b {dev_branch}"):
            return False
        if not self.run_command(f"git checkout {main_branch}"):
            return False
        if not self.run_command(f"git checkout -b {staging_branch}"):
            return False
        if not self.commit_changes("Initial empty commit on staging", allow_empty=True):
            logger.error("Failed to create empty commit on staging")
            return False
        if not self.push_branch(staging_branch):
            logger.error(f"Failed to push {staging_branch} to remote")
            return False
        for feature_branch in feature_branches:
            if not self.run_command(f"git checkout {dev_branch}"):
                return False
            if not self.run_command(f"git checkout -b {feature_branch}"):
                return False
        if not self.run_command(f"git checkout {dev_branch}"):
            return False
        return True

    def add_files(self):
        return self.run_command("git add .")

    def commit_changes(self, message="Initial project setup on dev", allow_empty=False):
        cmd = f'git commit -m "{message}"'
        if allow_empty:
            cmd += " --allow-empty"
        return self.run_command(cmd)

    def push_branch(self, branch_name, force=False):
        cmd = f"git push origin {branch_name}"
        if force:
            cmd += " --force"
        return self.run_command(cmd)

    def setup_project(self, repo_url=None, main_branch="main", dev_branch="dev", staging_branch="staging", feature_branches=None):
        if feature_branches is None:
            feature_branches = []
        if not self.initialize_repo():
            logger.error("Git initialization failed")
            return False
        if not self.run_command(f"git checkout -b {main_branch}"):
            logger.error("Failed to create main branch")
            return False
        if not self.commit_changes("Initial empty commit", allow_empty=True):
            logger.error("Failed to create empty commit on main")
            return False
        if repo_url:
            if not self.set_remote(repo_url):
                logger.error("Failed to set remote")
                return False
            if not self.push_branch(main_branch, force=True):
                logger.error(f"Failed to push {main_branch} to remote")
                return False
            if not self.fetch_remote():
                logger.error("Failed to fetch from remote")
                return False
        if not self.setup_branches(main_branch, dev_branch, staging_branch, feature_branches):
            logger.error("Git branch setup failed")
            return False
        return True

    def finalize_project(self, repo_url=None, dev_branch="dev", feature_branches=None):
        if feature_branches is None:
            feature_branches = []
        # Assumption: .gitignore is created by FileCreator before this point
        if not self.add_files():  # Stages all files in project_path after .gitignore exists
            logger.error("Failed to add files")
            return False
        if not self.commit_changes("Initial project setup on dev"):
            logger.error("Failed to commit files on dev")
            return False
        if repo_url and not self.push_branch(dev_branch):
            logger.error(f"Failed to push {dev_branch} to remote")
            return False
        if repo_url:
            # Merge dev into feature branches to propagate all files
            for feature_branch in feature_branches:
                if not self.run_command(f"git checkout {feature_branch}"):
                    logger.error(f"Failed to checkout {feature_branch}")
                    return False
                if not self.run_command(f"git merge {dev_branch}"):
                    logger.error(f"Failed to merge {dev_branch} into {feature_branch}")
                    return False
                if not self.push_branch(feature_branch):
                    logger.error(f"Failed to push {feature_branch} to remote")
                    return False
            # Return to dev
            if not self.run_command(f"git checkout {dev_branch}"):
                logger.error(f"Failed to return to {dev_branch}")
                return False
        return True


