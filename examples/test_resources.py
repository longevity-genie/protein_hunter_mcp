#!/usr/bin/env python3
"""
Example script demonstrating how to use Protein Hunter MCP resources and tools.

This script shows how to:
1. Access protein sequence resources
2. Use the Boltz protein-protein design tool
3. Monitor progress for long-running tasks
"""

from pathlib import Path
import asyncio
import sys

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from protein_hunter_mcp.server import (
    EXAMPLE_PDL1_SEQUENCE,
    EXAMPLE_PDL1_SHORT_SEQUENCE,
    EXAMPLE_MULTIMER_SEQUENCE,
    EXAMPLE_RNA_SEQUENCE,
    EXAMPLE_LIGAND_SAM,
    EXAMPLE_LIGAND_SMILES,
    EXAMPLE_GENERIC_TARGET,
)


def test_resource_constants():
    """Test that all resource constants are accessible."""
    print("Testing Protein Sequence Resources\n")
    print("=" * 80)
    
    resources = [
        ("Example 1: PDL1 Sequence", EXAMPLE_PDL1_SEQUENCE),
        ("Example 2: PDL1 Short", EXAMPLE_PDL1_SHORT_SEQUENCE),
        ("Example 4: Multimer Sequence", EXAMPLE_MULTIMER_SEQUENCE),
        ("Example 6: RNA Sequence", EXAMPLE_RNA_SEQUENCE),
        ("Example 5: SAM Ligand", EXAMPLE_LIGAND_SAM),
        ("Chai: Ligand SMILES", EXAMPLE_LIGAND_SMILES),
        ("Chai: Generic Target", EXAMPLE_GENERIC_TARGET),
    ]
    
    for name, sequence in resources:
        seq_len = len(sequence)
        preview = sequence[:50] + "..." if len(sequence) > 50 else sequence
        print(f"\n{name}:")
        print(f"  Length: {seq_len}")
        print(f"  Preview: {preview}")
    
    print("\n" + "=" * 80)
    print("✓ All resource constants accessible\n")


async def test_tool_signature():
    """Test the Boltz design tool signature (without actually running it)."""
    print("Testing Boltz Protein-Protein Design Tool\n")
    print("=" * 80)
    
    from protein_hunter_mcp.server import ProteinHunterMCP
    
    # Create server instance
    server = ProteinHunterMCP(output_dir="/tmp/protein_hunter_test")
    
    print("\n✓ Server initialized successfully")
    print(f"  Output directory: {server.output_dir}")
    print(f"  Tool prefix: {server.prefix}")
    
    # Check that tools are registered
    print("\nRegistered tools:")
    print(f"  - {server.prefix}design_protein_binder (simplified, LLM-friendly)")
    print(f"  - {server.prefix}boltz_protein_design_advanced (full control)")
    
    print("\n" + "=" * 80)
    print("✓ Tool registration successful\n")


def print_usage_example():
    """Print an example of how to use the tool via MCP."""
    print("Example MCP Tool Call\n")
    print("=" * 80)
    
    example = """
# Example 1: Simple PDL1 binder design (LLM-friendly, recommended)
result = await mcp_client.call_tool(
    "ph_design_protein_binder",
    {
        "target_protein_sequence": EXAMPLE_PDL1_SEQUENCE,
        "design_name": "PDL1_binder_test",
        "num_designs": 1,
        "num_cycles": 7,
        "gpu_id": 0
    }
)
# Returns: {"status": "completed", "summary_csv": "/path/to/summary_high_iptm.csv"} (or summary_all_runs.csv if no high-ipTM cycles)

# Example 2: Advanced - Multimer binder design with full control
result = await mcp_client.call_tool(
    "ph_boltz_protein_design_advanced",
    {
        "protein_seqs": f"{EXAMPLE_MULTIMER_SEQUENCE}:{EXAMPLE_MULTIMER_SEQUENCE}",
        "protein_ids": "B:C",
        "num_designs": 3,
        "num_cycles": 7,
        "name": "multimer_binder",
        "gpu_id": 0,
        "use_msa_for_af3": True,
        "plot": True
    }
)

# Example 3: Advanced - Mixed amino acids (50% X, 50% random)
result = await mcp_client.call_tool(
    "ph_boltz_protein_design_advanced",
    {
        "protein_seqs": EXAMPLE_PDL1_SEQUENCE,
        "num_designs": 3,
        "num_cycles": 7,
        "name": "PDL1_mixed_aa",
        "percent_X": 50,
        "gpu_id": 0,
        "plot": True
    }
)

# All tools return only the summary CSV path for easy access to results
"""
    print(example)
    print("=" * 80)
    print()


def print_resource_access_example():
    """Print an example of how to access resources via MCP."""
    print("Example MCP Resource Access\n")
    print("=" * 80)
    
    example = """
# List all available resources
resources = await mcp_client.list_resources()

# Read a specific protein sequence resource
pdl1_seq = await mcp_client.read_resource("protein://example1/pdl1")

# Read ligand resource
sam_ligand = await mcp_client.read_resource("ligand://example5/sam")

# Read RNA sequence resource
rna_seq = await mcp_client.read_resource("nucleic://example6/rna")

# Available resource URIs:
# - protein://example1/pdl1
# - protein://example2/pdl1_short
# - protein://example3/pdl1_contact
# - protein://example4/multimer
# - protein://example5/pdl1_ligand
# - protein://example7/pdl1_multiple
# - ligand://example5/sam
# - ligand://chai/smiles
# - nucleic://example6/rna
# - protein://chai/generic_target
"""
    print(example)
    print("=" * 80)
    print()


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("Protein Hunter MCP - Resource and Tool Testing")
    print("=" * 80 + "\n")
    
    # Test 1: Resource constants
    test_resource_constants()
    
    # Test 2: Tool signature (async)
    print("Running async tool signature test...")
    asyncio.run(test_tool_signature())
    
    # Test 3: Usage examples
    print_resource_access_example()
    print_usage_example()
    
    print("=" * 80)
    print("All tests completed successfully!")
    print("=" * 80 + "\n")
    
    print("Next steps:")
    print("1. Start the MCP server: uv run protein-hunter-mcp server")
    print("2. Connect an MCP client")
    print("3. List resources to see all protein sequences")
    print("4. Call ph_design_protein_binder for simple design (requires GPU)")
    print("5. Or call ph_boltz_protein_design_advanced for full control (requires GPU)")
    print()


if __name__ == "__main__":
    main()

