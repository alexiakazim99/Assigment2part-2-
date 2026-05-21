import subprocess
from safety import is_safe
from output_limiter import limit_output

def run_bash(command):
    if not is_safe(command):
        return f"Command blocked for safety reasons: {command}"
    
    print(f"\nAgent wants to run: {command}")
    confirm = input("Allow? (y/n): ")
    
    if confirm.lower() != "y":
        return "Command was rejected by user."
    
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    
    output = result.stdout or result.stderr
    return limit_output(output)