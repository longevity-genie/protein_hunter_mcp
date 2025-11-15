

from typing import Optional
from pathlib import Path

import asyncio
import csv
from fastmcp import Context


class BoltzTools:
    def __init__(self, gpu_id: int = 0):
        """Initialize BoltzTools with GPU configuration.
        
        Args:
            gpu_id: GPU device ID to use for all operations
        """
        self.gpu_id = gpu_id
    async def design_protein_binder(
        self,
        target_protein_sequence: str,
        design_name: str = "protein_binder",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder for a target protein using Boltz (Example 1: standard binding).
        
        This is a simplified interface for designing protein binders with all-X sequence.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence to design a binder for
            design_name: Name for this design run (default: "protein_binder")
            num_designs: Number of designs to generate (default: 1, recommended: 1-3)
            num_cycles: Number of design cycles (default: 7, recommended: 5-10)
        
        Returns:
            dict: Results with summary CSV contents and status
            
        Example:
            Input: target_protein_sequence="AFTVTVPKDLYVVEYGSNMTIECKFPVEKQLDLAALIVYWEMEDKNIIQFVHGEEDLKVQHSSYRQRARLLKDQLSLGNAALQITDVKLQDAGVYRCMISYGGADYKRITVKVNAPYAAALE"
            Output: {"status": "completed", "results": [...]}
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequence,
            protein_ids="B",
            ctx=ctx,
        )
    
    async def design_protein_binder_with_template(
        self,
        target_protein_sequence: str,
        template_pdb_code: str,
        design_name: str = "protein_binder_template",
        template_chain_id: str = "B",
        template_cif_chain_id: str = "B",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder using a template structure (Example 2: template-based design).
        
        Uses a template PDB structure to guide the design process.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence
            template_pdb_code: PDB code for template structure (e.g., "8ZNL")
            design_name: Name for this design run (default: "protein_binder_template")
            template_chain_id: Chain ID in template to use (default: "B")
            template_cif_chain_id: Chain ID in CIF file (default: "B")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequence,
            protein_ids="B",
            template_path=template_pdb_code,
            template_chain_id=template_chain_id,
            template_cif_chain_id=template_cif_chain_id,
            ctx=ctx,
        )
    
    async def design_protein_binder_with_contacts(
        self,
        target_protein_sequence: str,
        contact_residues: str,
        design_name: str = "protein_binder_contacts",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder with specified contact residues (Example 3: contact specification).
        
        Designs a binder targeting specific residue positions on the target protein.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence
            contact_residues: Comma-separated residue positions (e.g., "29,277,279,293")
            design_name: Name for this design run (default: "protein_binder_contacts")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequence,
            protein_ids="B",
            contact_residues=contact_residues,
            add_constraints=True,
            ctx=ctx,
        )
    
    async def design_multimer_binder(
        self,
        target_protein_sequences: str,
        design_name: str = "multimer_binder",
        protein_chain_ids: str = "B:C",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a binder for a multimeric protein target (Example 4: multimer binder).
        
        Designs a binder for protein complexes with multiple chains (e.g., dimers).
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequences: Target sequences separated by ':' (e.g., "SEQ1:SEQ2")
            design_name: Name for this design run (default: "multimer_binder")
            protein_chain_ids: Chain IDs separated by ':' (default: "B:C")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequences,
            protein_ids=protein_chain_ids,
            ctx=ctx,
        )
    
    async def design_cyclic_peptide_binder(
        self,
        target_protein_sequence: str,
        design_name: str = "cyclic_peptide_binder",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a cyclic peptide binder for a target protein (Example 5: cyclic peptide).
        
        Designs short cyclic peptides (10-20 residues) that bind to target proteins.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence
            design_name: Name for this design run (default: "cyclic_peptide_binder")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequence,
            protein_ids="B",
            min_design_protein_length=10,
            max_design_protein_length=20,
            high_iptm_threshold=0.8,
            cyclic=True,
            ctx=ctx,
        )
    
    async def design_small_molecule_binder(
        self,
        ligand_ccd_code: str,
        design_name: str = "small_molecule_binder",
        ligand_chain_id: str = "B",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder for a small molecule (Example 6: small molecule binder).
        
        Designs proteins that bind to small molecules specified by CCD codes (e.g., "SAM").
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            ligand_ccd_code: Chemical Component Dictionary code (e.g., "SAM", "ATP")
            design_name: Name for this design run (default: "small_molecule_binder")
            ligand_chain_id: Chain ID for ligand (default: "B")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            ligand_ccd=ligand_ccd_code,
            ligand_id=ligand_chain_id,
            min_design_protein_length=130,
            max_design_protein_length=150,
            ctx=ctx,
        )
    
    async def design_nucleic_acid_binder(
        self,
        nucleic_acid_sequence: str,
        nucleic_acid_type: str,
        design_name: str = "nucleic_acid_binder",
        nucleic_chain_id: str = "B",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder for DNA or RNA (Example 7: nucleic acid binder).
        
        Designs proteins that bind to DNA or RNA sequences.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            nucleic_acid_sequence: DNA or RNA sequence (e.g., "AGAGAGAGA")
            nucleic_acid_type: Type of nucleic acid - "dna" or "rna"
            design_name: Name for this design run (default: "nucleic_acid_binder")
            nucleic_chain_id: Chain ID for nucleic acid (default: "B")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            nucleic_seq=nucleic_acid_sequence,
            nucleic_type=nucleic_acid_type,
            nucleic_id=nucleic_chain_id,
            min_design_protein_length=130,
            max_design_protein_length=150,
            ctx=ctx,
        )
    
    async def design_heterogeneous_binder(
        self,
        target_protein_sequence: str,
        ligand_ccd_code: str,
        design_name: str = "heterogeneous_binder",
        protein_chain_id: str = "B",
        ligand_chain_id: str = "C",
        num_designs: int = 1,
        num_cycles: int = 7,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a binder for multiple target types (Example 8: heterogeneous targets).
        
        Designs proteins that bind to both a protein and a small molecule simultaneously.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence
            ligand_ccd_code: Chemical Component Dictionary code for ligand
            design_name: Name for this design run (default: "heterogeneous_binder")
            protein_chain_id: Chain ID for protein target (default: "B")
            ligand_chain_id: Chain ID for ligand (default: "C")
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=design_name,
            protein_seqs=target_protein_sequence,
            protein_ids=protein_chain_id,
            ligand_ccd=ligand_ccd_code,
            ligand_id=ligand_chain_id,
            high_iptm_threshold=0.8,
            ctx=ctx,
        )
    
    async def design_protein_advanced(
        self,
        name: str,
        num_designs: int = 1,
        num_cycles: int = 7,
        # Optional protein target parameters
        protein_seqs: Optional[str] = None,
        protein_ids: str = "B",
        protein_msas: str = "",
        # Optional template parameters
        template_path: Optional[str] = None,
        template_chain_id: Optional[str] = None,
        template_cif_chain_id: Optional[str] = None,
        # Optional contact specification parameters
        contact_residues: Optional[str] = None,
        add_constraints: bool = False,
        # Optional ligand parameters
        ligand_ccd: Optional[str] = None,
        ligand_id: Optional[str] = None,
        # Optional nucleic acid parameters
        nucleic_seq: Optional[str] = None,
        nucleic_type: Optional[str] = None,
        nucleic_id: Optional[str] = None,
        # Design parameters
        min_design_protein_length: int = 90,
        max_design_protein_length: int = 150,
        high_iptm_threshold: float = 0.7,
        percent_X: int = 100,
        cyclic: bool = False,
        # Validation and output parameters
        use_msa_for_af3: bool = True,
        plot: bool = True,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Advanced Boltz design with full parameter control.
        
        Exposes all available parameters for maximum flexibility in protein design.
        Use this when you need fine-grained control over the design process.
        Long-running task: 7-10 minutes per design on an H100 GPU.
        
        Args:
            name: Name for this design run
            num_designs: Number of designs to generate (default: 1)
            num_cycles: Number of design cycles (default: 7)
            protein_seqs: Target protein sequences (colon-separated for multimers)
            protein_ids: Chain IDs for proteins (colon-separated, default: "B")
            protein_msas: MSA files for proteins (default: "")
            template_path: PDB code or path to template structure
            template_chain_id: Chain ID in template for prediction
            template_cif_chain_id: Chain ID in CIF file for alignment
            contact_residues: Comma-separated residue positions for contact specification
            add_constraints: Add constraints for contact residues (default: False)
            ligand_ccd: Chemical Component Dictionary code for ligand
            ligand_id: Chain ID for ligand
            nucleic_seq: DNA or RNA sequence
            nucleic_type: Type of nucleic acid ("dna" or "rna")
            nucleic_id: Chain ID for nucleic acid
            min_design_protein_length: Minimum length of designed protein (default: 90)
            max_design_protein_length: Maximum length of designed protein (default: 150)
            high_iptm_threshold: Threshold for high iPTM filtering (default: 0.7)
            percent_X: Percentage of X (unknown) residues in initial sequence (default: 100)
            cyclic: Enable cyclic peptide design (default: False)
            use_msa_for_af3: Use MSA for AlphaFold3 validation (default: True)
            plot: Generate plots for design cycles (default: True)
        
        Returns:
            dict: Results with summary CSV contents and status
        """
        return await self._run_boltz_design(
            num_designs=num_designs,
            num_cycles=num_cycles,
            gpu_id=self.gpu_id,
            name=name,
            protein_seqs=protein_seqs,
            protein_ids=protein_ids,
            protein_msas=protein_msas,
            template_path=template_path,
            template_chain_id=template_chain_id,
            template_cif_chain_id=template_cif_chain_id,
            contact_residues=contact_residues,
            add_constraints=add_constraints,
            ligand_ccd=ligand_ccd,
            ligand_id=ligand_id,
            nucleic_seq=nucleic_seq,
            nucleic_type=nucleic_type,
            nucleic_id=nucleic_id,
            min_design_protein_length=min_design_protein_length,
            max_design_protein_length=max_design_protein_length,
            high_iptm_threshold=high_iptm_threshold,
            percent_X=percent_X,
            cyclic=cyclic,
            use_msa_for_af3=use_msa_for_af3,
            plot=plot,
            ctx=ctx,
        )
    
    async def _run_boltz_design(
        self,
        num_designs: int,
        num_cycles: int,
        gpu_id: int,
        name: str,
        # Optional protein target parameters
        protein_seqs: Optional[str] = None,
        protein_ids: str = "B",
        protein_msas: str = "",
        # Optional template parameters
        template_path: Optional[str] = None,
        template_chain_id: Optional[str] = None,
        template_cif_chain_id: Optional[str] = None,
        # Optional contact specification parameters
        contact_residues: Optional[str] = None,
        add_constraints: bool = False,
        # Optional ligand parameters
        ligand_ccd: Optional[str] = None,
        ligand_id: Optional[str] = None,
        # Optional nucleic acid parameters
        nucleic_seq: Optional[str] = None,
        nucleic_type: Optional[str] = None,
        nucleic_id: Optional[str] = None,
        # Design parameters
        min_design_protein_length: int = 90,
        max_design_protein_length: int = 150,
        high_iptm_threshold: float = 0.7,
        percent_X: int = 100,
        cyclic: bool = False,
        # Validation and output parameters
        use_msa_for_af3: bool = True,
        plot: bool = True,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Internal method to run Boltz protein design with all optional parameters.
        
        This is the least common denominator for all Boltz design tools. It handles
        all possible parameter combinations for different design scenarios.
        """
        try:
            # Find the Protein-Hunter directory
            protein_hunter_dir = Path(__file__).parent.parent.parent / "Protein-Hunter"
            if not protein_hunter_dir.exists():
                return {
                    "status": "error",
                    "error": f"Protein-Hunter directory not found at {protein_hunter_dir}. Please ensure it's properly installed."
                }
            
            # Build the command with required parameters
            cmd = [
                "python", str(protein_hunter_dir / "boltz_ph" / "design.py"),
                "--num_designs", str(num_designs),
                "--num_cycles", str(num_cycles),
                "--gpu_id", str(gpu_id),
                "--name", name,
                "--min_design_protein_length", str(min_design_protein_length),
                "--max_design_protein_length", str(max_design_protein_length),
                "--high_iptm_threshold", str(high_iptm_threshold),
                "--percent_X", str(percent_X),
            ]
            
            # Add optional protein parameters
            if protein_seqs:
                cmd.extend(["--protein_seqs", protein_seqs])
                cmd.extend(["--protein_ids", protein_ids])
                cmd.extend(["--protein_msas", protein_msas])
            
            # Add optional template parameters
            if template_path:
                cmd.extend(["--template_path", template_path])
                if template_chain_id:
                    cmd.extend(["--template_chain_id", template_chain_id])
                if template_cif_chain_id:
                    cmd.extend(["--template_cif_chain_id", template_cif_chain_id])
            
            # Add optional contact specification parameters
            if contact_residues:
                cmd.extend(["--contact_residues", contact_residues])
                if add_constraints:
                    cmd.append("--add_constraints")
            
            # Add optional ligand parameters
            if ligand_ccd:
                cmd.extend(["--ligand_ccd", ligand_ccd])
                if ligand_id:
                    cmd.extend(["--ligand_id", ligand_id])
            
            # Add optional nucleic acid parameters
            if nucleic_seq:
                cmd.extend(["--nucleic_seq", nucleic_seq])
                if nucleic_type:
                    cmd.extend(["--nucleic_type", nucleic_type])
                if nucleic_id:
                    cmd.extend(["--nucleic_id", nucleic_id])
            
            # Add boolean flags
            if cyclic:
                cmd.append("--cyclic")
            if use_msa_for_af3:
                cmd.append("--use_msa_for_af3")
            if plot:
                cmd.append("--plot")
            
            # Report initial progress
            total_steps = num_designs * num_cycles
            if ctx:
                await ctx.report_progress(progress=0, total=total_steps)
            
            # Run the design process
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(protein_hunter_dir)
            )
            
            # Track progress by reading output
            current_run = 0
            current_cycle = 0
            
            # Read stdout line by line to track progress
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                    
                line_str = line.decode().strip()
                
                # Parse progress from output patterns
                if "=== Starting Design Run" in line_str:
                    parts = line_str.split("Run")
                    if len(parts) > 1:
                        run_info = parts[1].strip().split("/")[0].strip()
                        try:
                            current_run = int(run_info)
                        except ValueError:
                            pass
                
                elif "--- Run" in line_str and "Cycle" in line_str:
                    try:
                        parts = line_str.replace("---", "").strip().split(",")
                        run_part = parts[0].strip().split()[-1]
                        cycle_part = parts[1].strip().split()[-1]
                        current_run = int(run_part)
                        current_cycle = int(cycle_part)
                        
                        progress = current_run * num_cycles + current_cycle
                        if ctx:
                            await ctx.report_progress(
                                progress=min(progress, total_steps),
                                total=total_steps
                            )
                    except (ValueError, IndexError):
                        pass
            
            # Wait for process to complete
            await process.wait()
            
            # Report 100% completion
            if ctx:
                await ctx.report_progress(progress=total_steps, total=total_steps)
            
            if process.returncode != 0:
                stderr = await process.stderr.read()
                return {
                    "status": "error",
                    "error": f"Design process failed with return code {process.returncode}",
                    "stderr": stderr.decode()
                }
            
            # Find the summary CSV file (primary output)
            output_dir = protein_hunter_dir / "results_boltz" / name
            summary_csv = output_dir / "summary_high_iptm.csv"
            
            if not summary_csv.exists():
                return {
                    "status": "error",
                    "error": f"Summary CSV not found at {summary_csv}. Design may have failed."
                }
            
            # Read CSV contents for LLM-friendly results
            try:
                with open(summary_csv, 'r') as f:
                    reader = csv.DictReader(f)
                    results = list(reader)
                
                return {
                    "status": "completed",
                    "summary_csv_path": str(summary_csv),
                    "output_dir": str(output_dir),
                    "num_results": len(results),
                    "results": results
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to read CSV: {str(e)}",
                    "summary_csv_path": str(summary_csv)
                }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


