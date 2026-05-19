import os

TOOL_OUTPUT_LIMIT = int(os.getenv("TOOL_OUTPUT_LIMIT", 4000))

def limit_output(text):
    if len(text) > TOOL_OUTPUT_LIMIT:
        return text[:TOOL_OUTPUT_LIMIT] + f"\n\n[Output truncated at {TOOL_OUTPUT_LIMIT} characters]"
    return text