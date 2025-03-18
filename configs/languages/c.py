# c.py

C_CONFIG = {
    "gitignore": """# C
*.o
*.obj
*.exe
*.out
*.a
*.so
*.dylib
build/
""",
    "files": {
        "main.c": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}\n",
        "Makefile": "CC = gcc\nCFLAGS = -Wall\n\nall: main\n\nmain: main.o\n\t$(CC) main.o -o main\n\nmain.o: main.c\n\t$(CC) $(CFLAGS) -c main.c\n\nclean:\n\trm -f *.o main\n"
    }
}