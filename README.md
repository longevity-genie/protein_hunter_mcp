# Protein Hunter MCP

An MCP (Model Context Protocol) server for Protein Hunter - protein design and analysis tools powered by Boltz, Chai-lab, PyRosetta, and LigandMPNN.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to AI assistants. This server exposes Protein Hunter's capabilities through MCP, enabling AI assistants like Claude to perform protein design and analysis tasks.

## Requirements

- Python 3.10-3.12
- [uv](https://github.com/astral-sh/uv) package manager
- CUDA-capable GPU (recommended for Boltz)
- Git with submodule support

## Installation

1. **Clone the repository with submodules**:
   ```bash
   git clone --recurse-submodules https://github.com/YOUR_USERNAME/protein_hunter_mcp.git
   cd protein_hunter_mcp
   ```

   If you already cloned without `--recurse-submodules`, initialize the submodules:
   ```bash
   git submodule update --init --recursive
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Sync dependencies with uv**:
   ```bash
   uv sync
   ```

   This will install:
   - Modified Boltz from the Protein-Hunter submodule (with custom features)
   - Chai-lab from the sokrypton fork
   - All required dependencies

4. **Run post-installation script**:
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

## Quick Start

### Running the MCP Server

**STDIO mode** (for MCP clients like Claude Desktop):
```bash
uv run protein-hunter-mcp stdio
```

**HTTP mode** (for web integrations):
```bash
uv run protein-hunter-mcp http --port 3003
```

**SSE mode** (for Server-Sent Events):
```bash
uv run protein-hunter-mcp sse --port 3003
```

### Testing the Server

Run the hello world test:
```bash
uv run pytest test/test_server.py -v
```

### Using with Claude Desktop

Add to your Claude Desktop MCP configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "protein-hunter-mcp": {
      "command": "uv",
      "args": ["--directory", "/data/sources/protein_hunter_mcp", "run", "server.py", "stdio"]
    }
  }
}
```

For detailed usage instructions, see [MCP_USAGE.md](MCP_USAGE.md).

## Tool Usage

### Design Parameters

Each tool accepts parameters specific to its design type:

**Common Parameters (all tools):**
- `design_name` / `jobname`: Name for the design run
- `num_designs` / `n_trials`: Number of designs to generate (default: 1)
- `num_cycles` / `n_cycles`: Number of optimization cycles (Boltz: 7, Chai: 5)

**Boltz-Specific:**
- `target_protein_sequence`: Amino acid sequence of the target protein
- `template_pdb_code`: PDB code for template structures (e.g., "8ZNL")
- `contact_residues`: Comma-separated residue positions for contact specification
- `ligand_ccd_code`: Chemical Component Dictionary code (e.g., "SAM", "ATP")
- `nucleic_acid_sequence`: DNA or RNA sequence
- `min/max_design_protein_length`: Length constraints for designed protein

**Chai-Specific:**
- `target_protein_sequence`: Target protein sequence
- `ligand_smiles`: SMILES string for small molecules
- `target_length`: Desired length of designed protein
- `percent_X`: Percentage of unknown residues in initial sequence

### Performance Notes

- **Runtime**: 7-10 minutes per design on H100 GPU (Boltz), 5-10 minutes (Chai)
- **Progress Tracking**: All tools report progress through MCP context
- **GPU Support**: Configure via `GPU_ID` environment variable or server initialization
- **Output**: Results include PDB files, sequences, and metrics in structured directories

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

### Submodule Issues
If you encounter errors about missing `Protein-Hunter` directory or Boltz import errors:
```bash
# Initialize/update submodules
git submodule update --init --recursive

# If submodule is out of sync
git submodule update --remote --merge

# Reinstall dependencies
uv sync --reinstall-package boltz
```

### PyRosetta Installation Issues
If PyRosetta fails to install, the postinstall script uses a PATH wrapper to redirect `pip` calls to `uv pip`. Check the output for specific errors.

### CUDA Issues
Ensure you have a CUDA-compatible GPU and drivers installed. Boltz requires CUDA for optimal performance.

### Missing LigandMPNN or DAlphaBall
These are optional components from the Protein-Hunter repository. The postinstall script will skip them if not found.

### Boltz Import Errors
If you see `TypeError: Boltz2.predict_step() got an unexpected keyword argument`, you're likely using the standard Boltz package instead of the modified version. Ensure:
1. The Protein-Hunter submodule is initialized (`git submodule update --init --recursive`)
2. Dependencies are synced properly (`uv sync --reinstall-package boltz`)

## Architecture

This is a uv-based project, converted from the original conda-based Protein Hunter setup.

### Key Components

1. **ProteinHunterMCP Server** (`server.py`)
   - Built on FastMCP framework
   - Supports multiple transport modes (STDIO, HTTP, SSE)
   - Registers all design tools with `ph_` prefix
   - Manages GPU configuration (via `GPU_ID` env var or `--gpu-id` flag)
   - Provides MCP resources for example sequences

2. **BoltzTools** (`boltz.py`)
   - 8 specialized design methods covering different binding scenarios
   - 1 advanced method with full parameter control
   - Async subprocess execution for long-running tasks
   - Progress tracking via MCP context reporting
   - Returns structured results with CSV summaries and output paths

3. **ChaiTools** (`chai.py`)
   - 4 specialized design methods for different use cases
   - 1 advanced method with full parameter control
   - Async subprocess execution with progress tracking
   - Returns structured results with PDB files and metrics

### Design Philosophy

- **Simplified Interfaces**: Each tool focuses on a specific use case with sensible defaults
- **Advanced Options**: Advanced methods expose all parameters for power users
- **Long-Running Tasks**: Design processes run 7-10 minutes per design on H100 GPU
- **LLM-Friendly Results**: Structured JSON responses with paths and metrics
- **Resource Management**: Example sequences provided as MCP resources for easy reference

### Technical Features

- Uses `pyproject.toml` for dependency management
- All dependencies available via PyPI or git
- Post-install script handles special cases (PyRosetta, model weights, Protein-Hunter setup)
- Async design execution with subprocess management
- Progress reporting through MCP context
- Type-hinted function signatures throughout

## Project Structure

```
protein_hunter_mcp/
├── src/
│   └── protein_hunter_mcp/
│       ├── __init__.py
│       ├── server.py          # MCP server implementation
│       ├── boltz.py           # Boltz design tools (8 methods)
│       ├── chai.py            # Chai design tools (4 methods)
│       └── example_sequences.py  # Example protein/ligand sequences
├── Protein-Hunter/            # Git submodule with design scripts
│   ├── boltz_ph/             # Boltz design implementation
│   ├── chai_ph/              # Chai design implementation
│   └── results_*/            # Output directories
├── server.py                  # Server entry point
├── postinstall.py            # Post-installation setup script
├── test/                      # Test suite
│   └── test_server.py        # Server tests
├── pyproject.toml            # Project configuration
├── mcp-config.json           # MCP client config examples
├── README.md                 # This file
├── MCP_USAGE.md              # Detailed MCP usage guide
└── PROTEIN_SEQUENCES.md      # Documentation for example sequences
```

## Available MCP Tools

All tools are prefixed with `ph_` to avoid naming conflicts. The server exposes 12 protein design tools across two platforms:

### Boltz Design Tools (8 tools)

1. **`ph_design_protein_binder`**: Design a protein binder for a target protein (standard binding with all-X sequence)
2. **`ph_design_protein_binder_with_template`**: Design a protein binder using a template PDB structure
3. **`ph_design_protein_binder_with_contacts`**: Design a protein binder with specified contact residues
4. **`ph_design_multimer_binder`**: Design a binder for multimeric protein targets (e.g., dimers)
5. **`ph_design_cyclic_peptide_binder`**: Design cyclic peptide binders (10-20 residues)
6. **`ph_design_small_molecule_binder`**: Design protein binders for small molecules (via CCD codes)
7. **`ph_design_nucleic_acid_binder`**: Design protein binders for DNA or RNA sequences
8. **`ph_design_heterogeneous_binder`**: Design binders for multiple target types (protein + small molecule)

### Chai Design Tools (4 tools)

1. **`ph_chai_design_unconditional_protein`**: Design de novo proteins of a desired length
2. **`ph_chai_design_protein_binder`**: Design a protein binder for a target protein using Chai
3. **`ph_chai_design_cyclic_peptide_binder`**: Design cyclic peptide binders using Chai
4. **`ph_chai_design_ligand_binder`**: Design protein binders for small molecules (via SMILES)

### MCP Resources

The server provides example sequences and ligands as MCP resources:

- `protein://example1/pdl1`: PDL1 sequence for standard binder design
- `protein://example2/pdl1_short`: Shorter PDL1 variant for template-based design
- `protein://example3/pdl1_contact`: PDL1 sequence for contact specification
- `protein://example4/multimer`: Multimer sequence (1GNW dimer)
- `ligand://example5/sam`: SAM ligand CCD code
- `nucleic://example6/rna`: RNA sequence for nucleic acid binder design
- `ligand://chai/smiles`: SMILES string for Chai ligand binder design
- `protein://chai/generic_target`: Generic target sequence for unconditional design

### Coming Soon

- **`ph_ligandmpnn_design`**: Protein design with LigandMPNN
- **`ph_pyrosetta_refine`**: Structure refinement with PyRosetta
- **`ph_analyze_structure`**: Protein structure analysis
- **`ph_visualize`**: 3D visualization of protein structures

## License

See LICENSE file for details.
