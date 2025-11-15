# Protein Hunter MCP

An MCP (Model Context Protocol) server for Protein Hunter - protein design and analysis tools powered by Boltz, Chai-lab, PyRosetta, and LigandMPNN.

## Requirements

- Python 3.10-3.12
- [uv](https://github.com/astral-sh/uv) package manager
- CUDA-capable GPU (recommended for Boltz)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd /data/sources/protein_hunter_mcp
   ```

2. **Sync dependencies with uv**:
   ```bash
   uv sync
   ```

3. **Run post-installation script**:
   ```bash
   uv run postinstall.py
   ```

   This script will:
   - Download Boltz weights to `~/.boltz`
   - Install PyRosetta (with automatic pip→uv redirection)
   - Setup LigandMPNN model parameters (if available)
   - Make DAlphaBall.gcc executable
   - Verify installations

## What's Included

### Core Dependencies
- **Boltz** v2.2.1 with CUDA support - protein structure prediction
- **Chai-lab** - advanced protein modeling
- **PyRosetta** - protein design and analysis
- **LigandMPNN** - ligand-conditioned protein design

### Additional Tools
- ProDy, PyPDB - protein structure analysis
- py3Dmol, py2Dmol - molecular visualization
- matplotlib, seaborn - plotting and visualization

## Usage

After installation, you can use the MCP server:

```bash
uv run protein_hunter_mcp
```

## Development

Install development dependencies:
```bash
uv sync --extra dev
```

This includes:
- pytest, pytest-asyncio - testing
- mypy - type checking
- ruff - linting and formatting
- ipykernel - Jupyter notebook support

Run tests:
```bash
uv run pytest
```

## Troubleshooting

### PyRosetta Installation Issues
If PyRosetta fails to install, the postinstall script uses a PATH wrapper to redirect `pip` calls to `uv pip`. Check the output for specific errors.

### CUDA Issues
Ensure you have a CUDA-compatible GPU and drivers installed. Boltz requires CUDA for optimal performance.

### Missing LigandMPNN or DAlphaBall
These are optional components from the Protein-Hunter repository. The postinstall script will skip them if not found.

## Architecture

This is a uv-based project, converted from the original conda-based Protein Hunter setup. Key differences:
- Uses `pyproject.toml` for dependency management
- All dependencies available via PyPI or git
- Post-install script handles special cases (PyRosetta, model weights)

## License

See LICENSE file for details.
