# Protein Hunter MCP Server Usage

This document describes how to use the Protein Hunter MCP (Model Context Protocol) server.

## Overview

Protein Hunter MCP provides protein design and analysis capabilities through the Model Context Protocol, enabling AI assistants to perform complex protein engineering tasks.

## Installation

### From PyPI (when published)

```bash
uvx protein-hunter-mcp stdio
```

### Local Development

```bash
# Install dependencies
uv sync

# Run post-installation (PyRosetta, Boltz weights, etc.)
uv run postinstall.py
```

## Running the Server

### STDIO Mode (Standard Input/Output)

Default mode for MCP client integration:

```bash
# Using uvx (from PyPI)
uvx --from protein-hunter-mcp@latest stdio

# Using uv run (local development)
uv run protein-hunter-mcp stdio

# Or directly
uv run server.py stdio
```

### HTTP Mode (Streamable HTTP)

For web-based integrations:

```bash
uv run protein-hunter-mcp http --host 0.0.0.0 --port 3003
```

### SSE Mode (Server-Sent Events)

For SSE-based integrations:

```bash
uv run protein-hunter-mcp sse --host 0.0.0.0 --port 3003
```

### Generic Server Command

Run with custom transport:

```bash
uv run protein-hunter-mcp server --transport stdio --port 3003
```

## MCP Client Configuration

### Claude Desktop / Cline

Add to your MCP configuration file:

**For published version:**
```json
{
  "mcpServers": {
    "protein-hunter-mcp": {
      "command": "uvx",
      "args": ["--from", "protein-hunter-mcp@latest", "stdio"]
    }
  }
}
```

**For local development:**
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

### Configuration File Locations

- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cline (VSCode)**: Configure in Cline settings

## Available Tools

### Current Tools (Stub)

#### `ph_hello`

A simple test tool to verify the server is working.

**Parameters:**
- `name` (str, optional): Name to greet (default: "World")

**Returns:**
- `message`: Greeting message
- `version`: Server version
- `transport`: Transport mode being used
- `output_dir`: Output directory path

**Example:**
```json
{
  "name": "ph_hello",
  "arguments": {
    "name": "Protein Hunter"
  }
}
```

**Response:**
```json
{
  "message": "Hello, Protein Hunter!",
  "version": "0.1.0",
  "transport": "stdio",
  "output_dir": "/path/to/protein_hunter_output"
}
```

### Future Tools (To Be Implemented)

- `ph_boltz_predict`: Predict protein structures using Boltz
- `ph_chai_predict`: Predict protein structures using Chai-lab
- `ph_ligandmpnn_design`: Design proteins with LigandMPNN
- `ph_pyrosetta_refine`: Refine protein structures with PyRosetta
- `ph_analyze_structure`: Analyze protein structure properties
- `ph_visualize`: Visualize protein structures

## Output Directory

By default, the server creates output files in `./protein_hunter_output/`. You can customize this:

```bash
uv run protein-hunter-mcp stdio --output-dir /path/to/custom/output
```

## Environment Variables

- `MCP_HOST`: Default host (default: "0.0.0.0")
- `MCP_PORT`: Default port (default: "3003")
- `MCP_TRANSPORT`: Default transport mode (default: "stdio")

## Testing

Run tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=protein_hunter_mcp
```

## Development

### Project Structure

```
protein_hunter_mcp/
├── src/
│   └── protein_hunter_mcp/
│       ├── __init__.py
│       └── server.py          # Main server implementation
├── server.py                   # Entry point
├── pyproject.toml             # Project configuration
├── mcp-config.json            # MCP client config (stdio)
└── mcp-config-server.json     # MCP client config (server mode)
```

### Adding New Tools

1. Add method to `ProteinHunterMCP` class in `server.py`
2. Register in `_register_tools()` method
3. Document in this file
4. Add tests in `test/`

### Code Style

Format code:
```bash
uv run ruff format .
```

Lint code:
```bash
uv run ruff check .
```

Type check:
```bash
uv run mypy src/
```

## Troubleshooting

### Server Won't Start

1. Check dependencies are installed: `uv sync`
2. Verify post-installation completed: `uv run postinstall.py`
3. Check logs for specific errors

### MCP Client Can't Connect

1. Verify the server starts manually: `uv run protein-hunter-mcp stdio`
2. Check MCP configuration file syntax
3. Restart the MCP client application

### CUDA/GPU Issues

Ensure CUDA drivers are properly installed for Boltz operations:

```bash
nvidia-smi  # Check GPU availability
```

## Support

For issues, please check:
- Project README.md
- MIGRATION.md (for conversion notes)
- GitHub Issues (if repository is public)

## License

See LICENSE file for details.

