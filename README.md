# Agantai - Autonomous AI Code Repair Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Gemini API](https://img.shields.io/badge/Gemini%20API-Powered-orange?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Agantai** is an advanced, autonomous AI agent designed to repair, patch, and write code. Built on top of the Google Gemini API, it acts as an intelligent pair programmer that can explore your codebase, diagnose errors, and implement fixes with minimal human intervention.

Unlike simple chatbots, Agantai works in a loop: it reads files, plans changes, applies patches, and verify its own work by running tests—all automatically.

---

## 🚀 Features

- **Autonomous Error Fixing**: Can read a file, identify syntax or logic errors, and apply patches without manual copying/pasting.
- **Context Awareness**: Efficiently scans file structures using `get_files_info` to understand the project layout before making changes.
- **Smart Tooling**:
  - `get_files_info`: Discovers file paths and structures.
  - `get_file_content`: Reads code context.
  - `patch_file_lines`: Surgical edits to fix specific bugs.
  - `write_file`: Creates or completely rewrites files when necessary.
  - `run_python_file`: Executes code to verify fixes immediately.
- **Self-Correction Loop**: If a fix fails (the code errors out), the agent analyzes the new error and retries automatically up to a defined limit.

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

- **Python**: Version 3.10 or higher.
- **Gemini API Key**: A valid API key from [Google AI Studio](https://aistudio.google.com/).

## 📥 Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/zkzkGamal/agantic-ai.git
    cd agantai
    ```

2.  **Set Up a Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.

    ```bash
    # Create the virtual environment
    python3 -m venv .venv

    # Activate it (Linux/macOS)
    source .venv/bin/activate

    # Activate it (Windows)
    # .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    This project uses `pyproject.toml`. You can install dependencies using `pip` or `uv`.
    ```bash
    pip install -e .
    # OR if you use uv
    uv sync
    ```

## 🔑 Configuration

1.  Create a `.env` file in the root directory:

    ```bash
    cp .env.example .env
    ```

2.  Open `.env` and add your Google Gemini API key:
    ```ini
    GEMINI_API_KEY=your_api_key_here
    ```

## 💻 Usage

The main entry point is `main.py`. You interact with the agent by providing a prompt via the CLI.

### Basic Command

```bash
python main.py --prompt "Your instruction here"
```

### Options

- `--prompt`: (Required) The instruction or task for the agent.
- `--verbose`: (Optional) Prints detailed token usage and step-by-step agent thoughts.

### Examples

**1. Fix a buggy file:**

```bash
python main.py --prompt "Fix the syntax error in calculator/main.py and run it to verify."
```

**2. Create a new feature:**

```bash
python main.py --prompt "Create a new script in functions/hello.py that prints 'Hello World' and run it." --verbose
```

**3. Analyze and Document:**

```bash
python main.py --prompt "Read the main.py file and create a documentation block at the top explaining what it does."
```

## 🧪 Testing

The project includes a `tests.py` file to verify that the agent's internal tools (file reading, writing, execution) are working correctly on your system.

Run the tests using:

```bash
python tests.py
```

This will print the output of various tool checks (listing files, reading content, writing dummy files) to ensuring the environment is set up correctly.

## 📂 Project Structure

```
agantai/
├── call_functions.py       # wrapper for handling function tool calls
├── config.py               # Configuration settings
├── functions/              # Directory containing tool definitions (schemas)
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── patch_file_line.py
│   ├── run_python_file.py
│   └── write_file.py
├── main.py                 # Main entry point and agent loop
├── pyproject.toml          # Project dependencies
├── tests.py                # System verification script
└── README.md               # Project documentation
```

## 🔮 Future Roadmap

- [ ] Add support for more LLM models (OpenAI, Anthropic).
- [ ] Implement a safer sandbox for code execution (Docker).
- [ ] Add support for multi-file refactoring in a single pass.
- [ ] Create a web-based UI for easier interaction.

---

_Built by [Zkaria Gamal]_
