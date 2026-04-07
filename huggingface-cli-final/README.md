# Free Official AI Command-Line Interface

An OS-independent, completely free AI command-line interface. This tool utilizes the official **Hugging Face Serverless Inference API** to connect you directly with world-class open-source models (like Qwen 72B, Llama 3, or Mistral) right in your terminal, with zero latency and perfect stability.

## Features
- **Official & Blazingly Fast**: Zero proxy tunneling! You get direct serverless API speeds (< 1 sec ping).
- **Zero Cost**: Uses the completely free Hugging Face Inference endpoints. 
- **Cross-Platform**: Works identically and natively on Windows, Linux, and macOS.
- **Persistent Sessions**: Log in once, and your conversation history stays intact across terminal runs.
- **Interactive Chat**: Includes a live REPL environment with streaming token responses identical to real LLM websites.
- **File Uploads**: Supports injecting text file content into your conversation context natively!

## Installation

You can clone this repository or download the source code, then run the handy installer for your specific operating system to make it available as a global bash tool.

### For Windows:
Double-click `install.bat` or run it from the command line:
```bat
.\install.bat
```

### For Linux / macOS:
Make the script executable and run it:
```bash
chmod +x install.sh
./install.sh
```

## Setup (Getting your Free Token)
Because this uses official ultra-fast servers, you need a free access token from Hugging Face.
1. Go to **huggingface.co** and create a free account.
2. Go to your settings: **huggingface.co/settings/tokens**
3. Create a free "Access Token" (Give it *Read* permissions).
4. Run this in your terminal to bind the CLI to your token:
   ```bash
   ai login YOUR_HUGGINGFACE_TOKEN_HERE
   ```

## How to Use

**Start a continuous chat**
```bash
ai chat
```

**Ask a quick single question**
```bash
ai ask "Write a short poem about the ocean"
```

**Attach a text file for context reading**
```bash
ai ask "Please summarize this document" -f document.txt
```
*(Or type `/file path/to/document.txt` while inside the interactive `ai chat` mode before specifying your prompt!).*
