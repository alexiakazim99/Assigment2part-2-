from llm_client import client, model
from session import Session
from tool_registry import get_tool, get_tool_names

def run_agent(user_input, system_prompt):
    session = Session(system_prompt)
    session.add_user_message(user_input)
    
    for _ in range(10):
        response = client.chat.completions.create(
            model=model,
            messages=session.get_messages(),
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "bash",
                        "description": "Run a bash command",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The bash command to run"
                                }
                            },
                            "required": ["command"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "edit_file",
                        "description": "Edit a specific section of a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filepath": {
                                    "type": "string"
                                },
                                "old_content": {
                                    "type": "string"
                                },
                                "new_content": {
                                    "type": "string"
                                }
                            },
                            "required": ["filepath", "old_content", "new_content"]
                        }
                    }
                }
            ],
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            session.add_assistant_message(message.content or "")
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                import json
                args = json.loads(tool_call.function.arguments)
                
                tool = get_tool(tool_name)
                if tool:
                    result = tool(**args)
                else:
                    result = f"Unknown tool: {tool_name}"
                
                print(f"\nTool: {tool_name}")
                print(f"Result: {result}")
                
                session.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        else:
            print(f"\nAgent: {message.content}")
            break