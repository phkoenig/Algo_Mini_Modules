# GitHub CLI Commands Reference

This README provides a quick reference for common GitHub CLI commands, specifically optimized for PowerShell on Windows.

## Basic Git Commands

### Repository Status

```powershell
# Check the status of your repository
git status

# View remote repository connections
git remote -v

# Check differences between local and remote
git fetch && git status
```

### Viewing Repository Information

```powershell
# View commit history (recent 5 commits)
git log --oneline -n 5

# List all tracked files in the repository
git ls-tree -r --name-only HEAD

# List untracked files (not ignored)
git ls-files --others --exclude-standard
```

### Making Changes

```powershell
# Add files to be committed
git add filename
# Add all files
git add .

# Commit changes
git commit -m "Descriptive message about the changes"

# Push changes to GitHub
git push origin master
```

### Getting Updates

```powershell
# Fetch latest changes from remote
git fetch

# Pull changes (fetch + merge)
git pull origin master
```

## PowerShell-Specific Notes

- When using pipe commands in PowerShell, use PowerShell syntax:
  - Instead of `git status | cat` (Unix-style), use `git status | Out-String`
  - Or simply run commands without piping in PowerShell

- For viewing long outputs in PowerShell:
  ```powershell
  git log | more
  ```

## Project Setup

This project uses a Python virtual environment:

1. Activate the environment:
   ```powershell
   .\activate.bat
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Repository Structure

- `.gitignore` - Specifies files excluded from version control
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked by Git for security)
- `venv/` - Virtual environment (not tracked by Git) 