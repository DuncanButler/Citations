# Copilot Citations Python

A tool for managing GitHub Copilot-generated code citations and references. This project aims to extract citation comments from code and consolidate them into documentation.

## Features

- Extract citations from code comments
- Generate consolidated citation documentation
- Support for multiple programming languages
- Integration with VS Code

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- Visual Studio Code

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/Copilot-Citations-Python.git
   cd Copilot-Citations-Python
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The Copilot Citations tool can be used from the command line:

```bash
python -m src.__main__ -d /path/to/code -o /path/to/output/citations.md
```

For detailed CLI usage instructions, see the [CLI Usage Guide](./Documentation/cli_usage.md).

## Development

See the [Documentation](./Documentation) directory for development information.
