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
1. Fork and clone the repository:
   ```bash
   git clone <repository-fork-url>
   cd <repository-fork-folder>
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

## Debugging for Contributors

To make development and debugging easier, you can set up the project in editable mode. This allows you to make changes to the source files and immediately see the effects without having to reinstall the package every time.

### Steps to Set Up Debugging

1. **Install the project in editable mode**:
   Run the following command in the root directory of the project (where `setup.py` or `pyproject.toml` is located):
   ```bash
   pip install -e .
   ```
   This will install the project in "editable" mode, meaning any changes you make to the source code will be reflected immediately.

2. **Run the project**:
   After installation, you can use the project’s CLI entry point (if defined in the setup):
   ```bash
   tebogen
   ```
   This will execute the latest version of the code directly from your working directory.

3. **Make Changes**:
   - Edit the source files in the `tebogen/` directory.
   - Changes will automatically apply the next time you run `tebogen`.

### Notes
- Ensure you have all necessary dependencies installed by running:
  ```bash
  pip install -r requirements.txt
  ```

- If you encounter any issues, verify that the correct Python environment is active:
  ```bash
  which python
  which tebogen
  ```

- For major changes or to ensure a clean environment, reinstall the package:
  ```bash
  pip uninstall tebogen
  pip install -e .
  ```

This setup helps streamline development by reducing the need for repeated package builds.

