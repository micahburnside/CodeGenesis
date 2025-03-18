from .languages.python import PYTHON_CONFIG
from .languages.c import C_CONFIG
from .languages.java import JAVA_CONFIG
from .languages.javascript import JAVASCRIPT_CONFIG
import os

# Dictionary of all language configurations
LANGUAGE_CONFIGS = {
    "Python": PYTHON_CONFIG,
    "C": C_CONFIG,
    "Java": JAVA_CONFIG,
    "JavaScript": JAVASCRIPT_CONFIG
}

LICENSE_DIR = os.path.join(os.path.dirname(__file__), "licenses")

def get_license_content(license_name, author):
    """Load a license template and format it with the current year and author."""
    from datetime import datetime
    license_path = os.path.join(LICENSE_DIR, f"{license_name}.txt")
    if not os.path.exists(license_path):
        raise FileNotFoundError(f"License '{license_name}' not found in {LICENSE_DIR}")
    with open(license_path, "r") as f:
        return f.read().format(year=datetime.now().year, author=author)