# Tebogen (Telegram Bot Generator)

Version: 0.0.8

A powerful tool for creating data-collecting Telegram bots.

# Setting Up Development Environment

This project uses **`pre-commit`** hooks to ensure code consistency and quality. The tools included are:
- **`black`**: Formats code to a consistent style.
- **`isort`**: Organizes imports.
- **`autoflake`**: Removes unused imports and variables.

## Prerequisites
- **Python**: Make sure you have Python (3.7 or higher) installed.
- **Git**: Ensure Git is installed and properly configured.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install `pre-commit`:
   ```bash
   pip install pre-commit
   ```

3. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. (Optional) Run hooks manually for the entire codebase:
   ```bash
   pre-commit run --all-files
   ```

## How It Works
- Whenever you attempt to commit changes (`git commit`), `pre-commit` will automatically run:
  - **`black`**: Formats your Python files.
  - **`isort`**: Reorders and organizes imports.
  - **`autoflake`**: Removes unused imports and variables.

- If any changes are made by these tools, the commit will be stopped. You’ll need to review and re-add the changes, then commit again.

---

## FAQ
### What if `pre-commit` modifies files during the commit process?
Simply add the modified files back and commit again:
```bash
git add .
git commit -m "Your commit message"
```

### How to update the pre-commit hooks if `.pre-commit-config.yaml` changes?
Run:
```bash
pre-commit autoupdate
pre-commit install
```

### Can I bypass the hooks temporarily?
Yes, you can use the `--no-verify` flag:
```bash
git commit --no-verify -m "Your commit message"
```
> Note: This should only be used in rare cases, such as emergencies.

---

## Future Contributors
When other developers clone the repository, they only need to install `pre-commit` and run:
```bash
pip install pre-commit
pre-commit install
```

