# main.py


import tkinter as tk
from gui import ProjectCreatorApp
from logger import logger
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()  # Load variables from .env file
    github_token = os.getenv("GITHUB_TOKEN")
    root = tk.Tk()
    app = ProjectCreatorApp(root)
    logger.info("Starting CodeGenesis Project Creator...")
    print("Starting CodeGenesis Project Creator...")
    root.mainloop()

# TODO: Add functionality to select github, gitlab, Plastic PCS, GitTea, or local only
# TODO: Add indicator to show AI Connectivity Status
# TODO: Add functionality to select which AI engine and link credentials
# TODO: Add Status and Progress Indicators to UI
# TODO: Add system status readout panel
# TODO: Change Core Branches functionality to choose branches from checklist
# TODO: Add Menu Item "Settings", make it work
# TODO: Add Dark mode / Light Mode
# TODO: Clean up UI, give professional look
# TODO: Save this project to Github
# TODO: Create README.md template that includes platform and language module specific content
# TODO: FIX: new projects are created inside code genesis directory. They should be created wherever the user chooses through the file explorer window pop up. Add Project directory output selection. Python projects should be saved in designated python folders, dotnet in dotnet folders,
# TODO: Link local git repo with remote url, set remote url
# TODO: convert this to dotnet
# TODO: Build identical version in SwiftUI
# TODO: Build Web Version in Angular
# TODO: Build Android Version in Kotlin
# TODO: Needs a place to add Git PAT in GUI which autogenerates an .env or whatever better method AI recommends....SSH?
# TODO: Add Postgres SQL Database
# TODO: Add functionality to view git log history in GUI