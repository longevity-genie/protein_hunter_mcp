#!/usr/bin/env python3
"""Protein Hunter MCP Server - Protein design and analysis tools."""

import os
from enum import Enum
from typing import Optional
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

import typer

from protein_hunter_mcp.boltz import BoltzTools
from protein_hunter_mcp.chai import ChaiTools
from typing_extensions import Annotated
from fastmcp import FastMCP

from protein_hunter_mcp.example_sequences import EXAMPLE_PDL1_SEQUENCE, EXAMPLE_PDL1_SHORT_SEQUENCE, EXAMPLE_MULTIMER_SEQUENCE, EXAMPLE_RNA_SEQUENCE, EXAMPLE_RNA_LONG_SEQUENCE, EXAMPLE_LIGAND_SAM, EXAMPLE_LIGAND_SMILES, EXAMPLE_GENERIC_TARGET
# Get package version
try:
    __version__ = version("protein-hunter-mcp")
except PackageNotFoundError:
    __version__ = "unknown"



class TransportType(str, Enum):
    STDIO = "stdio"
    STREAMABLE_HTTP = "streamable-http"
    SSE = "sse"

# Configuration
DEFAULT_HOST = os.getenv("MCP_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("MCP_PORT", "3003"))
DEFAULT_TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio")
DEFAULT_GPU_ID = int(os.getenv("GPU_ID", "0"))

class ProteinHunterMCP(FastMCP):
    """Protein Hunter MCP Server with protein design and analysis tools."""
    
    def __init__(
        self, 
        name: str = f"Protein Hunter MCP Server v{__version__}",
        prefix: str = "ph_",
        transport_mode: str = "stdio",
        output_dir: Optional[str] = None,
        gpu_id: int = DEFAULT_GPU_ID,
        **kwargs
    ):
        """Initialize the Protein Hunter tools with FastMCP functionality."""
        super().__init__(name=name, **kwargs)
        
        self.prefix = prefix
        self.transport_mode = transport_mode
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "protein_hunter_output"
        self.gpu_id = gpu_id
        self.boltz_tools = BoltzTools(gpu_id=gpu_id)
        self.chai_tools = ChaiTools(gpu_id=gpu_id)
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
            
        self._register_tools()
    
    def _register_tools(self):
        """Register Protein Hunter tools and resources."""
        
        # Register simple LLM-friendly tools for each Boltz example
        self.tool(name=f"{self.prefix}design_protein_binder")(self.boltz_tools.design_protein_binder)
        self.tool(name=f"{self.prefix}design_protein_binder_with_template")(self.boltz_tools.design_protein_binder_with_template)
        self.tool(name=f"{self.prefix}design_protein_binder_with_contacts")(self.boltz_tools.design_protein_binder_with_contacts)
        self.tool(name=f"{self.prefix}design_multimer_binder")(self.boltz_tools.design_multimer_binder)
        self.tool(name=f"{self.prefix}design_cyclic_peptide_binder")(self.boltz_tools.design_cyclic_peptide_binder)
        self.tool(name=f"{self.prefix}design_small_molecule_binder")(self.boltz_tools.design_small_molecule_binder)
        self.tool(name=f"{self.prefix}design_nucleic_acid_binder")(self.boltz_tools.design_nucleic_acid_binder)
        self.tool(name=f"{self.prefix}design_heterogeneous_binder")(self.boltz_tools.design_heterogeneous_binder)
        
        # Register Boltz advanced tool
        #self.tool(name=f"{self.prefix}design_protein_advanced")(self.boltz_tools.design_protein_advanced)
        
        # Register Chai tools
        self.tool(name=f"{self.prefix}chai_design_unconditional_protein")(self.chai_tools.design_unconditional_protein)
        self.tool(name=f"{self.prefix}chai_design_protein_binder")(self.chai_tools.design_protein_binder_chai)
        self.tool(name=f"{self.prefix}chai_design_cyclic_peptide_binder")(self.chai_tools.design_cyclic_peptide_binder_chai)
        self.tool(name=f"{self.prefix}chai_design_ligand_binder")(self.chai_tools.design_ligand_binder_chai)
        
        # Register Chai advanced tool
        #self.tool(name=f"{self.prefix}chai_design_protein_advanced")(self.chai_tools.design_protein_advanced_chai)
        
        # Register resources for protein sequences from examples
        self._register_resources()
    
    def _register_resources(self):
        """Register MCP resources for protein sequences."""
        
        # Register each example sequence as a resource
        @self.resource(f"protein://example1/pdl1")
        def example1_pdl1() -> str:
            """Example 1: PDL1 protein sequence for protein-protein design with all X sequence."""
            return EXAMPLE_PDL1_SEQUENCE
        
        @self.resource(f"protein://example2/pdl1_short")
        def example2_pdl1_short() -> str:
            """Example 2: Shorter PDL1 variant for template-based design."""
            return EXAMPLE_PDL1_SHORT_SEQUENCE
        
        @self.resource(f"protein://example3/pdl1_contact")
        def example3_pdl1_contact() -> str:
            """Example 3: PDL1 sequence for contact specification design."""
            return EXAMPLE_PDL1_SEQUENCE
        
        @self.resource(f"protein://example4/multimer")
        def example4_multimer() -> str:
            """Example 4: Multimer protein sequence (1GNW dimer) for multimer binder design."""
            return EXAMPLE_MULTIMER_SEQUENCE
        
        @self.resource(f"protein://example5/pdl1_ligand")
        def example5_pdl1_ligand() -> str:
            """Example 5: PDL1 sequence for small molecule binder design."""
            return EXAMPLE_PDL1_SEQUENCE
        
        @self.resource(f"ligand://example5/sam")
        def example5_sam() -> str:
            """Example 5: SAM ligand CCD code for small molecule binder design."""
            return EXAMPLE_LIGAND_SAM
        
        @self.resource(f"nucleic://example6/rna")
        def example6_rna() -> str:
            """Example 6: RNA sequence for DNA/RNA binder design."""
            return EXAMPLE_RNA_SEQUENCE
        
        @self.resource(f"protein://example7/pdl1_multiple")
        def example7_pdl1_multiple() -> str:
            """Example 7: PDL1 sequence for designs with multiple/heterogeneous target types."""
            return EXAMPLE_PDL1_SEQUENCE
        
        @self.resource(f"ligand://chai/smiles")
        def chai_ligand_smiles() -> str:
            """Chai example: SMILES string for ligand binder design."""
            return EXAMPLE_LIGAND_SMILES
        
        @self.resource(f"protein://chai/generic_target")
        def chai_generic_target() -> str:
            """Chai example: Generic target sequence (20 amino acids) for unconditional design."""
            return EXAMPLE_GENERIC_TARGET
    





def create_app(transport_mode: str = "stdio", output_dir: Optional[str] = None):
    """Create and configure the FastMCP application."""
    return ProteinHunterMCP(transport_mode=transport_mode, output_dir=output_dir)

# CLI application setup
cli_app = typer.Typer(help="Protein Hunter MCP Server CLI")

@cli_app.command()
def server(
    host: Annotated[str, typer.Option(help="Host to run the server on.")] = DEFAULT_HOST,
    port: Annotated[int, typer.Option(help="Port to run the server on.")] = DEFAULT_PORT,
    transport: Annotated[str, typer.Option(help="Transport type: stdio, streamable-http, or sse")] = DEFAULT_TRANSPORT,
    output_dir: Annotated[Optional[str], typer.Option(help="Output directory for local files (stdio mode)")] = None,
):
    """Runs the Protein Hunter MCP server."""
    # Validate transport value
    if transport not in ["stdio", "streamable-http", "sse"]:
        typer.echo(f"Invalid transport: {transport}. Must be one of: stdio, streamable-http, sse")
        raise typer.Exit(1)
        
    app = create_app(transport_mode=transport, output_dir=output_dir)

    # Different transports need different arguments
    if transport in ["stdio"]:
        app.run(transport="stdio")
    else:
        app.run(transport=transport, host=host, port=port)

@cli_app.command(name="stdio")
def stdio():
    """Runs the Protein Hunter MCP server in stdio mode (standard input/output)."""
    app = create_app(transport_mode="stdio")
    app.run(transport="stdio")

@cli_app.command(name="http")
def http(
    host: Annotated[str, typer.Option(help="Host to run the server on.")] = DEFAULT_HOST,
    port: Annotated[int, typer.Option(help="Port to run the server on.")] = DEFAULT_PORT,
    output_dir: Annotated[Optional[str], typer.Option(help="Output directory for local files")] = None,
):
    """Runs the Protein Hunter MCP server in streamable HTTP mode."""
    app = create_app(transport_mode="streamable-http", output_dir=output_dir)
    app.run(transport="streamable-http", host=host, port=port)

@cli_app.command(name="sse")
def sse(
    host: Annotated[str, typer.Option(help="Host to run the server on.")] = DEFAULT_HOST,
    port: Annotated[int, typer.Option(help="Port to run the server on.")] = DEFAULT_PORT,
    output_dir: Annotated[Optional[str], typer.Option(help="Output directory for local files")] = None,
):
    """Runs the Protein Hunter MCP server in Server-Sent Events (SSE) mode."""
    app = create_app(transport_mode="sse", output_dir=output_dir)
    app.run(transport="sse", host=host, port=port)

if __name__ == "__main__":
    cli_app()

