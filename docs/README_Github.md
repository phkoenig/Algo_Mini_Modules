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

- PowerShell may encounter issues with long command outputs or paging. If you experience truncated output or errors like:
  ```
  System.ArgumentOutOfRangeException: The value must be greater than or equal to zero and less than the console's buffer size
  ```
  Try these solutions:
  - Increase your console buffer size in PowerShell settings
  - Use `| Out-String` instead of `| more` or `| cat`
  - For git commands that produce a lot of output, add specific limiting parameters (like `-n 5` for `git log`)

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
- `docs/` - Documentation files
  - `README_*.md` - Various README files for different components
  - Naming convention: `README_Topic.md` (e.g., `README_KuCoin_Websocket_Consolidated.md`)
- `modules/` - Python modules for different functionalities
  - `Trading_Pairs/` - Modules for handling trading pairs
  - `Websocket_Raw_Data/` - Modules for WebSocket connections
- `examples/` - Example code demonstrating usage
- `temp/` - Temporary test scripts (not tracked by Git)

## Documentation Guidelines

- All README files should be placed in the `docs/` folder
- Use the naming convention `README_Topic.md`
- For API documentation, use consolidated files that combine overview and detailed guides
- Keep the root folder clean, with only essential files

## Common Git Workflows

### Renaming Files

```powershell
# Rename a file and track the change in git
git mv old_filename.md new_filename.md

# If you've already renamed the file outside of git
git add new_filename.md
git rm old_filename.md
```

### Handling Deleted Files

```powershell
# Remove a file from the repository
git rm filename.md

# If you've already deleted the file
git add -u
```

Last updated: 26.02.2025 