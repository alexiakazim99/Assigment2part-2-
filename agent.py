import os
from dotenv import load_dotenv
from agent_loop import run_agent

load_dotenv()

def main():
    with open("config/system_prompt.md", "r") as f:
        system_prompt = f.read()
    
    print("Agent ready. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        run_agent(user_input, system_prompt)

if __name__ == "__main__":
    main()