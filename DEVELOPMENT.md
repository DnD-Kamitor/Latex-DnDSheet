# Development Setup

## Prerequisites

- Python 3.10 or higher
- `python3-venv` package (for virtual environments)
- LuaLaTeX (for PDF generation)
- DND-5e-LaTeX-Template (see installation below)

## Initial Setup

### 1. Install Python venv (if not already installed)

```bash
sudo apt install python3.11-venv
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install development dependencies

```bash
pip install -e ".[dev]"
```

### 4. Run tests

```bash
pytest
```

## Running the CLI

After installation, you can run the CLI in development mode:

```bash
# Show help
python -m dndsheet --help

# Check dependencies
python -m dndsheet check

# Generate character sheet (Phase 5+)
python -m dndsheet generate examples/fighter.json
```

## Project Structure

```
Latex-DnDSheet/
├── src/dndsheet/          # Main package
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Module entry point
│   ├── cli.py             # CLI interface
│   └── ...                # Other modules (added in later phases)
├── tests/
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── templates/             # Jinja2 LaTeX templates
├── rulebooks/             # D&D reference data
├── examples/              # Example character files
└── pyproject.toml         # Project configuration
```

## Development Workflow

1. Create a new branch for your feature
2. Make changes
3. Run tests: `pytest`
4. Check code style: `black src/ tests/` and `ruff check src/ tests/`
5. Commit changes
6. Push and create PR

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=dndsheet --cov-report=html
```

### Run specific test file
```bash
pytest tests/unit/test_cli.py
```

## Code Style

We use:
- **Black** for code formatting (line length: 100)
- **Ruff** for linting
- **pytest** for testing

Run formatters:
```bash
black src/ tests/
ruff check src/ tests/ --fix
```
