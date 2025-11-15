# Protein Sequences - MCP Resources

This document describes the protein sequences and other molecular data exposed as MCP resources from the Protein-Hunter examples.

## Available Resources

All protein sequences from the Protein-Hunter README examples are now available as MCP resources. These can be accessed by MCP clients to use in protein design workflows.

### Boltz Examples

#### Example 1: Protein-Protein Design (All X Sequence)
- **Resource URI**: `protein://example1/pdl1`
- **Description**: PDL1 protein sequence for protein-protein design with all X sequence
- **Sequence**: `AFTVTVPKDLYVVEYGSNMTIECKFPVEKQLDLAALIVYWEMEDKNIIQFVHGEEDLKVQHSSYRQRARLLKDQLSLGNAALQITDVKLQDAGVYRCMISYGGADYKRITVKVNAPYAAALE`
- **Length**: 113 amino acids
- **Usage**: Designing a protein binder for PDL1 using de novo exploration

#### Example 2: Template-Based Design
- **Resource URI**: `protein://example2/pdl1_short`
- **Description**: Shorter PDL1 variant for template-based design
- **Sequence**: `FTVTVPKDLYVVEYGSNMTIECKFPVEKQLDLAALIVYWEMEDKNIIQFVHGEEDLKVQHSSYRQRARLLKDQLSLGNAALQITDVKLQDAGVYRCMISYGGADYKRITVKVNK`
- **Length**: 106 amino acids
- **Usage**: Design with template structure (PDB: 8ZNL)

#### Example 3: Contact Specification Design
- **Resource URI**: `protein://example3/pdl1_contact`
- **Description**: PDL1 sequence for contact specification design
- **Sequence**: Same as Example 1
- **Usage**: Design with specific interface residue positions (e.g., residues 2,3,10)

#### Example 4: Multimer Binder Design
- **Resource URI**: `protein://example4/multimer`
- **Description**: Multimer protein sequence (1GNW dimer) for multimer binder design
- **Sequence**: `AGIKVFGHPASIATRRVLIALHEKNLDFELVHVELKDGEHKKEPFLSRNPFGQVPAFEDGDLKLFESRAITQYIAHRYENQGTNLLQTDSKNISQYAIMAIGMQVEDHQFDPVASKLAFEQIFKSIYGLTTDEAVVAEEEAKLAKVLDVYEARLKEFKYLAGETFTLTDLHHIPAIQYLLGTPTKKLFTERPRVNEWVAEITKRPASEKVQ`
- **Length**: 176 amino acids
- **Usage**: Designing a binder for a dimeric protein complex

#### Example 5: Small Molecule Binder Design
- **Protein Resource URI**: `protein://example5/pdl1_ligand`
- **Ligand Resource URI**: `ligand://example5/sam`
- **Protein Sequence**: Same as Example 1
- **Ligand**: SAM (S-Adenosyl methionine)
- **Usage**: Design protein binder for a small molecule (SAM)

#### Example 6: DNA/RNA Binder Design
- **Resource URI**: `nucleic://example6/rna`
- **Description**: RNA sequence for DNA/RNA binder design
- **Sequence**: `AGAGAGAGA`
- **Type**: RNA
- **Length**: 9 nucleotides
- **Usage**: Design protein binder for nucleic acids

#### Example 7: Multiple/Heterogeneous Target Types
- **Protein Resource URI**: `protein://example7/pdl1_multiple`
- **Description**: PDL1 sequence for designs with multiple/heterogeneous target types
- **Sequence**: Same as Example 1
- **Usage**: Target multiple types of molecules (protein + ligand + template)

### Chai Examples

#### Chai Ligand Binder
- **Resource URI**: `ligand://chai/smiles`
- **Description**: SMILES string for ligand binder design
- **SMILES**: `O=C(NCc1cocn1)c1cnn(C)c1C(=O)Nc1ccn2cc(nc2n1)c1ccccc1`
- **Usage**: Design protein binder for a small molecule using Chai model

#### Chai Unconditional Design
- **Resource URI**: `protein://chai/generic_target`
- **Description**: Generic target sequence (20 amino acids) for unconditional design
- **Sequence**: `ACDEFGHIKLMNPQRSTVWY`
- **Usage**: Generate de novo proteins with diverse amino acid composition

## Tool: Boltz Protein-Protein Design

The `ph_boltz_protein_design` tool implements the first Boltz example as a long-running task with progress tracking.

### Function Signature

```python
ph_boltz_protein_design(
    protein_seqs: str,
    ctx: Context,
    num_designs: int = 2,
    num_cycles: int = 7,
    protein_ids: str = "B",
    protein_msas: str = "",
    gpu_id: int = 0,
    name: str = "protein_design",
    min_design_protein_length: int = 90,
    max_design_protein_length: int = 150,
    high_iptm_threshold: float = 0.7,
    percent_X: int = 100,
    use_msa_for_af3: bool = True,
    plot: bool = True,
) -> dict[str, str]
```

### Parameters

- **protein_seqs**: Target protein sequence(s). Use ':' to separate multiple chains
- **ctx**: FastMCP context for progress reporting
- **num_designs**: Number of designs to generate (default: 2)
- **num_cycles**: Number of design cycles (default: 7)
- **protein_ids**: Chain IDs for proteins, separated by ':' for multimers (default: "B")
- **protein_msas**: MSA files or "" for no MSA (default: "")
- **gpu_id**: GPU device ID to use (default: 0)
- **name**: Name for this design run (default: "protein_design")
- **min_design_protein_length**: Minimum length for designed protein (default: 90)
- **max_design_protein_length**: Maximum length for designed protein (default: 150)
- **high_iptm_threshold**: iPTM threshold for high-confidence designs (default: 0.7)
- **percent_X**: Percentage of X (unknown) residues vs random amino acids (default: 100)
- **use_msa_for_af3**: Use MSA for AlphaFold3 validation (default: True)
- **plot**: Generate plots (default: True)

### Returns

Returns a dictionary with:
- **status**: "completed" or "error"
- **output_dir**: Path to output directory
- **command**: The command that was executed
- **high_iptm_yaml**: Path to high iPTM YAML files (if available)
- **high_iptm_cif**: Path to high iPTM CIF files (if available)
- **summary_file**: Path to summary CSV file (if available)

### Usage Example

```python
# Using the PDL1 sequence from Example 1
result = await mcp_client.call_tool(
    "ph_boltz_protein_design",
    {
        "protein_seqs": "AFTVTVPKDLYVVEYGSNMTIECKFPVEKQLDLAALIVYWEMEDKNIIQFVHGEEDLKVQHSSYRQRARLLKDQLSLGNAALQITDVKLQDAGVYRCMISYGGADYKRITVKVNAPYAAALE",
        "num_designs": 3,
        "num_cycles": 7,
        "name": "PDL1_design",
        "percent_X": 100,
        "min_design_protein_length": 90,
        "max_design_protein_length": 150
    }
)
```

### Progress Tracking

This tool provides real-time progress updates during the 7-10 minute execution time on an H100 GPU. The progress is tracked based on:
- Number of designs × Number of cycles
- Output parsing for design and cycle completion

## Notes

- **Runtime**: The Boltz protein-protein design typically takes 7-10 minutes on an H100 GPU
- **GPU Required**: These tools require GPU acceleration
- **Output Location**: Results are saved to `Protein-Hunter/output/{name}/`
- **Validation**: High-confidence designs can be validated using AlphaFold3 if configured

## Example Workflow

1. **List available resources** to see all protein sequences
2. **Read a resource** to get the sequence for your target protein
3. **Call the design tool** with the sequence and desired parameters
4. **Monitor progress** through the context progress reporting
5. **Retrieve results** from the output directory specified in the response

## Related Files

- `server.py`: Main MCP server implementation
- `run_protein_hunter.py`: Example commands for all use cases
- `README.md`: Full Protein-Hunter documentation

