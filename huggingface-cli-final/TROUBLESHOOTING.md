# Troubleshooting & Debugging Guide

Here are the most common issues you might run into while installing or running the AI CLI on different operating systems, and exactly how to fix them!

## Issue 1: "The process cannot access the file because it is being used" (Windows)
**Error:** `[WinError 32]` or `Permission Denied` during installation.
**Cause:** You are trying to run the installer while the `ai chat` window is actively open and running in another terminal. Windows locks the executable while it is running.
**Fix:** Type `quit` or close your currently open terminal completely, then try running `install.bat` again.

## Issue 2: "externally-managed-environment" (Kali Linux / Debian)
**Error:** `PEP 668` error when locally running the installer script on strict Linux distributions. 
**Cause:** Modern Linux distributions strictly prevent global `pip` installations to protect native system files.
**Fix:** Run the manual installation commands in your terminal and append the system bypass override flag to force it:
```bash
pip install -r requirements.txt --break-system-packages
pip install -e . --break-system-packages
```

## Issue 3: Emoji or Unicode Encoding Crash (Windows CMD)
**Error:** `'charmap' codec can't encode character...`
**Cause:** The AI generated a complex emoji or foreign symbol, but you are using an older Windows Command Prompt that does not natively stream UTF-8 sequences.
**Fix:** The application now safely catches and strips unreadable emojis by default so it won't crash! However, for full native visual support, you can enable modern Unicode mode by running `chcp 65001` in your terminal before using the CLI.

## Issue 4: "API Key Not Valid" or "Authentication Error"
**Cause:** Hugging face rejected your token.
**Fix:**
1. Ensure you copied the token exactly from your `huggingface.co/settings/tokens` page.
2. Run `ai login YOUR_NEW_TOKEN` using the actual letters straight in the command rather than relying on bash pipelines or variable expansions.
