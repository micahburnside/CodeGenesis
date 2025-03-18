# java.py

JAVA_CONFIG = {
    "gitignore": """# Java
*.class
*.jar
*.war
*.ear
build/
out/
target/
""",
    "files": {
        "src/Main.java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}\n"
    }
}