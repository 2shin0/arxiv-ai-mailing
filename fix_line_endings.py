import sys

def fix_file_line_endings(file_path):
    """Converts CRLF line endings to LF in a file."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        new_content = content.replace(b'\r\n', b'\n')
        
        if new_content != content:
            with open(file_path, 'wb') as f:
                f.write(new_content)
            print(f"Successfully converted line endings in '{file_path}' to LF.")
        else:
            print(f"Line endings in '{file_path}' are already LF.")

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_line_endings.py <file_path>")
        sys.exit(1)
    
    file_to_fix = sys.argv[1]
    fix_file_line_endings(file_to_fix)
