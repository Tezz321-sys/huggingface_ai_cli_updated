import argparse
import sys
import json
from pathlib import Path
import os

try:
    from huggingface_hub import InferenceClient
except ImportError:
    print("Please install requirements: pip install huggingface_hub")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".ai_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

def init_config():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    init_config()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    init_config()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)


def login(api_key):
    config = load_config()
    config['api_key'] = api_key
    save_config(config)
    print("Logged in successfully! Your Free Hugging Face Token has been saved.")

def logout():
    config = load_config()
    if 'api_key' in config:
        del config['api_key']
        save_config(config)
        print("Logged out successfully.")
    else:
        print("Not logged in.")

def clear_history():
    if HISTORY_FILE.exists():
        os.remove(HISTORY_FILE)
    print("Conversation history cleared.")

def get_file_content(filepath):
    """Loads file contents into text to append to the prompt context"""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return None
        
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return f"--- FILE: {os.path.basename(filepath)} ---\n{content}\n--- END FILE ---"
    except Exception as e:
        print(f"Failed to read file: {e}")
        return None

def complete_chat(history, prompt, attached_file_content=None):
    config = load_config()
    if not config.get('api_key'):
        print("You are not logged in. Please run 'ai login <your_hf_token>' first.")
        sys.exit(1)
        
    # Free HuggingFace Inference API Client
    client = InferenceClient(api_key=config['api_key'])
    
    # Qwen 2.5 72B is an insanely fast, incredibly smart free open-source model currently dominating benchmarks
    model_id = "Qwen/Qwen2.5-72B-Instruct"
    
    full_prompt = prompt
    if attached_file_content:
        full_prompt += f"\n\n[Attached File Content]:\n{attached_file_content}"
        
    temp_history = history.copy()
    temp_history.append({"role": "user", "content": full_prompt})
    
    reply = ""
    try:
        response = client.chat_completion(
            model=model_id,
            messages=temp_history,
            max_tokens=2048,
            stream=True
        )
        for chunk in response:
            if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content:
                    try:
                        sys.stdout.write(content)
                        sys.stdout.flush()
                    except UnicodeEncodeError:
                        sys.stdout.write(content.encode('ascii', 'ignore').decode('ascii'))
                        sys.stdout.flush()
                    reply += content
        print() 
    except Exception as e:
        print(f"\nError communicating with Hugging Face API: {e}")
        
    return reply

def ask(prompt, file_arg=None):
    attached_file_content = None
    if file_arg:
        attached_file_content = get_file_content(file_arg)
        
    history = load_history()
    
    print("\nHugging Face AI: ", end="")
    reply = complete_chat(history, prompt, attached_file_content)
    
    if reply:
        # Save standard prompt back to history to save tokens instead of entire file context again
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": reply})
        save_history(history)

def repl():
    eval_config = load_config()
    if not eval_config.get('api_key'):
        print("You are not logged in. Please run 'ai login <your_hf_token>' first.")
        sys.exit(1)
    
    print("Entering instant interactive mode.")
    print("Type 'quit' or 'exit' to leave.")
    print("To attach a text file context, type '/file <path-to-file>' (e.g. /file info.txt) and press Enter FIRST.")
    history = load_history()
    
    pending_file_path = None
        
    while True:
        try:
            prefix = ""
            if pending_file_path:
                prefix = f"[File: {os.path.basename(pending_file_path)}] "
            
            prompt = input(f"{prefix}You: ")
            
            if prompt.strip().lower() in ['quit', 'exit']:
                break
                
            if prompt.strip().startswith("/file "):
                filepath = prompt.strip()[6:].strip()
                if os.path.exists(filepath):
                    pending_file_path = filepath
                    print(f"File '{os.path.basename(filepath)}' attached! Now type your actual prompt.")
                else:
                    print(f"Error: File '{filepath}' not found.")
                continue
                
            if not prompt.strip():
                continue
            
            attached_file_content = None
            if pending_file_path:
                attached_file_content = get_file_content(pending_file_path)
                pending_file_path = None
                
            print("Hugging Face AI: ", end="")
            reply = complete_chat(history, prompt, attached_file_content)
            
            if reply:
                history.append({"role": "user", "content": prompt})
                history.append({"role": "assistant", "content": reply})
                save_history(history)
                
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    example_text = '''
Examples:
  ai login hf_abc123                         # Authenticate your Hugging Face token
  ai chat                                    # Start an interactive chat session
  ai ask "Summarize this:" -f report.txt     # Upload a text file and ask a quick question
  ai clear                                   # Erase background conversation history
  
Inside 'ai chat' mode, you can upload files for context by typing:
  /file path/to/document.txt
  (Press Enter, then ask your question about the file)
'''

    parser = argparse.ArgumentParser(
        description="Official Lightning-Fast Free AI CLI",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    login_parser = subparsers.add_parser("login", help="Login securely with your Hugging Face Token")
    login_parser.add_argument("api_key", type=str, help="Your Free Hugging Face Token")
    
    subparsers.add_parser("logout", help="Logout and remove your token")
    
    ask_parser = subparsers.add_parser("ask", help="Ask a quick prompt")
    ask_parser.add_argument("prompt", nargs="+", type=str, help="The prompt to send")
    ask_parser.add_argument("--file", "-f", type=str, help="Path to a text file", default=None)
    
    subparsers.add_parser("clear", help="Clear history")
    subparsers.add_parser("chat", help="Start the interactive REPL")
    
    args = parser.parse_args()
    
    if args.command == "login":
        login(args.api_key)
    elif args.command == "logout":
        logout()
    elif args.command == "ask":
        ask(" ".join(args.prompt), args.file)
    elif args.command == "clear":
        clear_history()
    elif args.command == "chat":
        repl()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
