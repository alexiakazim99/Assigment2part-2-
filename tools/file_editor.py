from output_limiter import limit_output

def edit_file(filepath, old_content, new_content):
    try:
        with open(filepath, "r") as f:
            content = f.read()
        
        if old_content not in content:
            return f"Could not find the specified content in {filepath}"
        
        updated = content.replace(old_content, new_content, 1)
        
        with open(filepath, "w") as f:
            f.write(updated)
        
        return limit_output(f"Successfully edited {filepath}")
    
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error editing file: {str(e)}"