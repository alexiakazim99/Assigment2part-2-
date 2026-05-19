from tools.bash_tool import run_bash
from tools.file_editor import edit_file

TOOLS = {
    "bash": run_bash,
    "edit_file": edit_file,
}

def get_tool(name):
    return TOOLS.get(name)

def get_tool_names():
    return list(TOOLS.keys())