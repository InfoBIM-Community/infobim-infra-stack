<div>
  <div style="display: inline-block; vertical-align: middle;" width="100">
    <img src="https://avatars.githubusercontent.com/u/252078843" width="100" alt="InfoBIM Logo" />
  </div>
  <div style="display: inline-block; vertical-align: middle; margin-left: 10px;">
    <h1 style="margin: 0; border-bottom: none;">InfoBIM CLI - BIM Data Management</h1>
  </div>
</div>

![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge&logo=apache)
![Docker](https://img.shields.io/badge/docker-available-blue?style=for-the-badge&logo=docker&logoColor=white)
![Textual](https://img.shields.io/badge/TUI-Textual-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Development-yellow?style=for-the-badge)

## 🎯 Objective
**InfoBIM CLI** is a Text-based User Interface (TUI) command-line tool designed to orchestrate and manage BIM data in a unified way. Born from the consolidation of various tools and scripts, it serves as an operations hub for **triaging, visualizing, and importing IFC files**.

The project uses **OntoBDC** as the underlying framework for persistence, semantic interpretation, and data structuring, but maintains its own identity as the interface for data management and operation.

Its purpose is to abstract the complexity of BIM processing, offering an agile and standardized interface for engineers and information managers, regardless of the specific project they are working on.

## 🎥 Preview

<table>
<tr>
<td width="50%">
<a href="">
<img src="docs/images/menu-preview.png" alt="InfoBIM CLI Main Menu" />
</a>
</td>
<td width="50%">
<a href="">
<img src="docs/images/report-preview.png" alt="IFC File Details" />
</a>
</td>
</tr>
<tr>
<td align="center"><b>Main Menu</b><br/>The central hub displaying the active environment and version, providing quick access to core features like IFC screening, visualization, and import workflows.</td>
<td align="center"><b>IFC File Details</b><br/>Comprehensive breakdown of imported IFC files, detailing geometry, property sets, and entity relationships in a structured format.</td>
</tr>
</table>

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[Getting Started](docs/getting_started.md)**: Setup guide, first steps, and configuration.
- **[Architecture](docs/architecture.md)**: System design, core concepts, and data flow.
- **[CLI Reference](docs/cli_reference.md)**: Comprehensive guide to commands, flags, and menus.
- **[Development Guide](docs/development.md)**: Contributing, coding standards, and testing.
- **[API/Integration](docs/integration.md)**: How to integrate with OntoBDC and other systems.

## 🚀 Key Features

### 1. Navigation and Triage
- Automatic scanning of input directories (configurable via adapters).
- Interactive listing and filtering of IFC files.

### 2. File Inspection
- Detailed visualization of IFC file metadata and properties.
- Dynamic rendering of technical reports directly in the terminal (via Jinja2 templates).

### 3. Interactive Import
- Ingestion pipeline for IFC files, structuring data through `ontobdc`.
- **Modal Interface**: Real-time visual feedback of processing steps (Reading, Transforming, Persisting) without blocking navigation.
- Integrated error handling and file validation.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Interface (TUI)**: [Textual](https://textual.textualize.io/) and [Rich](https://rich.readthedocs.io/) for a modern user experience in the terminal.
- **Containerization**: Docker and Docker Compose for isolation and reproducibility.
- **Core**: Integration with `ontobdc` modules for specialized AECO/BIM data manipulation.

## 🧩 Architecture and Patterns

- **Adapters Pattern**: Isolation between the user interface (CLI) and business logic/data access (in `src/cli/adapters`).
- **Asynchrony**: Use of Textual *Worker Threads* for I/O-intensive operations (like IFC parsing), keeping the UI fluid.
- **Factories**: Creation pattern to instantiate services and storage adapters in a decoupled way.

## 🏗️ Project Structure

The directory structure separates infrastructure configuration (Docker) from application code (Python), facilitating maintenance and portability.

```
infra/
├── docker/                 # Containerization Configuration
│   ├── compose/            # Docker Compose files per environment
│   │   ├── config.yaml     # General environment settings
│   │   ├── .env            # Environment variables
│   │   └── docker-compose-*.yaml
│   ├── manifests/          # Dockerfiles
│   ├── cli-requirements.txt # CLI Python dependencies
│   └── web-requirements.txt # Python dependencies (future Web)
├── src/                    # Application Source Code
│   ├── cli/                # Command Line Interface
│   │   ├── adapters/       # Integration Adapters (e.g., Importer)
│   │   ├── terminal/       # TUI Logic (Textual/Rich)
│   │   │   ├── menu/       # Screens and Menus
│   │   │   ├── config.yaml # CLI Configuration
│   │   │   └── run.py      # CLI Entry Point
│   └── lib/                # Shared Libraries and Utilities
├── branch.sh               # Script for git branch management
├── commit.sh               # Script for standardized semantic commits
├── run.sh                  # Main script to start CLI via Docker
└── up.sh                   # Script to bring up background services
```

## ⚙️ How to Run

The tool is designed to run in containers, ensuring the execution environment is identical for all stakeholders (developers, engineers, managers).

### Prerequisites
- Docker Engine
- Docker Compose

### Commands

1. **Start CLI (Interactive Mode)**
   Use the `run.sh` script in the `infra` project root.
   ```bash
   ./run.sh [develop|staging|production]
   ```
   *Default: `develop` if not specified.*
   ```

## 🤝 Contribution & Feedback

We welcome contributions, ideas, and discussions! Whether you're fixing a bug, improving documentation, or proposing new features, your input is valuable.

- **Found an issue?** Please report it on [GitHub Issues](https://github.com/InfoBIM-Community/infobim-infra-stack/issues).
- **Join the Community:** Chat with us on [Discord](https://discord.gg/rwwUwttZ).
- **Have a suggestion?** Join the discussion or submit a Pull Request.
- **Support the project:** If you find this tool useful, consider starring the repository! ⭐

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Proudly developed in Brazil, so far 🇧🇷</b>
</div>
