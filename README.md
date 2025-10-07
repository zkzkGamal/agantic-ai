# 🧠 Agantai — Self-Healing AI Coding Agent

**Agantai** is an autonomous AI-driven coding assistant that can explore a project’s structure, read and analyze code, identify bugs, apply self-repairs, and verify fixes — all without manual intervention.  
It acts like a “self-healing developer,” capable of diagnosing logic issues, refactoring code, and rerunning tests until the issue is resolved.

---

## 🚀 Features

- 🧩 **Autonomous File Exploration**  
  Automatically lists and inspects all project files and directories.

- 🔍 **Context-Aware Debugging**  
  Reads and understands relevant code files to locate the root cause of a bug or logical error.

- 🧠 **Smart Reasoning Loop**  
  Plans the next step (read → analyze → fix → verify) using an internal reasoning chain.

- 🛠️ **Self-Healing Fix Engine**  
  Modifies and overwrites buggy code, then re-runs the application or tests to confirm the fix.

- 🧾 **Test-Aware Validation**  
  Integrates with project tests or runtime outputs to verify correctness automatically.

- ⚙️ **Function-Oriented Design**  
  Core operations (list, read, write, run) are implemented as modular functions inside `/functions`.

---

## 📂 Project Structure
``` tree
agantai/
│
├── calculator/ # Example project for demonstration
│ ├── README.md
│ ├── main.py # Main entrypoint
│ ├── calculator.py # Core logic
│ ├── pkg/
│ │ ├── calculator.py # Calculator logic class
│ │ └── render.py # Output rendering utilities
│ └── tests.py # Unit tests for calculator
│
├── functions/ # Agent capability modules
│ ├── get_files_info.py # Lists all project files
│ ├── get_file_content.py # Reads file content
│ ├── run_python_file.py # Executes Python files
│ └── write_file.py # Writes or modifies files
│
├── main.py # Core AI agent entrypoint
├── call_functions.py # Internal function routing logic
├── config.py # Configuration and system prompt
├── pyproject.toml # Environment configuration
├── uv.lock # Dependency lockfile
├── .env.example # Example environment variables
└── tests.py # Global project tests
```
