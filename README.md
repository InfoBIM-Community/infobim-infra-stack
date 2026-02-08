# InfoBIM IFC

<div align="center">
<pre>
  _____        __      ____ _____ __  __
 |_   _|      / _|    |  _ \_   _|  \/  |
   | |  _ __ | |_ ___ | |_) || | | \  / |
   | | | '_ \|  _/ _ \|  _ < | | | |\/| |
  _| |_| | | | || (_) | |_) || |_| |  | |
 |_____|_| |_|_| \___/|____/_____|_|  |_|
</pre>
</div>

![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge&logo=apache)
![Status](https://img.shields.io/badge/Status-Development-yellow?style=for-the-badge)

### The Capability Engine for BIM Automation

> **Turn your BIM scripts into standardized, agent-ready capabilities.**

**InfoBIM IFC** is a modular runtime environment for Engineering Automation. It decouples the **execution logic** (how to run scripts, handle dependencies, manage Docker) from the **business logic** (validating pipes, counting doors, auditing models).

Whether you are a human running commands in the terminal or an **AI Agent** planning a complex workflow, InfoBIM provides the standard interface to interact with BIM data.

---

## 🚀 Quick Start

### 1. Install
```bash
# 1. Download the CLI
wget https://raw.githubusercontent.com/InfoBIM-Community/infobim-ifc/master/infobim

# 2. Make it executable
chmod +x infobim

# 3. Install environment (downloads the stack & setups venv)
./infobim install

# Optional: Install with Docker support
# ./infobim install --docker
```

### 2. Run a Capability
Execute a specific task directly without opening the full UI:

```bash
# List all sewage pipes (validating against NBR 8160)
./infobim run infobim.capability.list_sewage_pipes --ifc_path ./data/my_project.ifc
```

![Report Example](docs/images/report.png)

### 3. Agent Discovery (New!)
Are you an LLM or building an Agent? Get the full machine-readable catalog of available tools:

```bash
./infobim run --json
```

### 4. File Discovery & Scanning
Automatically scan and index IFC files located in the `data/incoming` directory. This is the first step to bring your BIM models into the InfoBIM environment.

```bash
./infobim ifc scan
```

The system will search for `.ifc` files and display them in the terminal:

![File Search](docs/images/ifc_file_search.png)

Once scanned, the files are ready to be processed by other capabilities:

![File List](docs/images/ifc_file_list.png)

---

## 🧩 Capabilities

A **Capability** is the atomic unit of work in InfoBIM. It wraps your Python scripts with:
1.  **Metadata**: Name, version, description.
2.  **Schema**: Formal definition of Inputs (arguments) and Outputs (return data).
3.  **Docs**: Embedded documentation for both humans and LLMs.

### Included Capabilities

| ID | Description |
|----|-------------|
| `infobim.capability.list_pipes` | Extracts pipe segments with geometry (Length, Z-coordinates) and properties. |
| `infobim.capability.list_sewage_pipes` | Specialized extraction for Sewage systems. Calculates **Real Slope** vs **Minimum Slope (Brazilian Standard NBR 8160, so far)**. |

---

## 🏗️ Architecture

InfoBIM IFC is designed to be the "Operating System" for your BIM scripts.

*   **Runtime**: Handles the environment (Python, Docker, IFCOpenShell).
*   **Registry**: Discovers and registers available Capabilities.
*   **Interfaces**:
    *   **CLI**: Direct execution (`./infobim run ...`).
    *   **TUI**: Interactive Text User Interface (`./infobim run`).
    *   **JSON-RPC**: (Coming soon) for remote execution.

---

## 🤖 For AI Agents

InfoBIM is **Agent-First**.
*   **Discovery**: `run --json` provides the tool definitions (compatible with OpenAI/Claude function calling).
*   **Deterministic Execution**: Agents don't "guess" geometry; they call Capabilities that return precise data.
*   **Structured Output**: All capabilities return strict JSON data, making it easy for LLMs to reason about the results.

---

## 📄 License

This project is part of the **InfoBIM Community**.
Licensed under **Apache 2.0**.

<div align="left">
  <br />
  <b>Proudly developed in Brazil 🇧🇷</b>
</div>
