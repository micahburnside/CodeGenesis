# javascript.py

JAVASCRIPT_CONFIG = {
    "gitignore": """# JavaScript
node_modules/
*.log
dist/
build/
coverage/
""",
    "files": {
        "package.json": '{\n    "name": "project",\n    "version": "1.0.0",\n    "main": "index.js",\n    "scripts": {\n        "start": "node index.js"\n    }\n}\n',
        "index.js": "console.log('Hello, World!');\n"
    }
}