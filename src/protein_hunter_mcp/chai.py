from typing import Optional
from pathlib import Path

import asyncio
import json
from fastmcp import Context


class ChaiTools:
    def __init__(self, gpu_id: int = 0):
        """Initialize ChaiTools with GPU configuration.
        
        Args:
            gpu_id: GPU device ID to use for all operations
        """
        self.gpu_id = gpu_id
    async def design_unconditional_protein(
        self,
        design_name: str = "unconditional_design",
        target_length: int = 120,
        percent_X: int = 0,
        n_trials: int = 1,
        n_cycles: int = 5,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design de novo proteins of a desired length (Chai Example 1: unconditional design).
        
        Generate unconditional proteins without a specific target.
        Long-running task: 5-10 minutes per design on an H100 GPU.
        
        Args:
            design_name: Name for this design run (default: "unconditional_design")
            target_length: Length of protein to design (default: 120)
            percent_X: Percentage of X (unknown) residues (default: 0)
            n_trials: Number of design trials to generate (default: 1)
            n_cycles: Number of design cycles (default: 5, recommended: 5-7)
        
        Returns:
            dict: Results with output directory contents and status
            
        Example:
            Input: target_length=120, percent_X=0
            Output: {"status": "completed", "results": [...]}
        """
        return await self._run_chai_design(
            jobname=design_name,
            length=target_length,
            percent_X=percent_X,
            seq="",
            target_seq="ACDEFGHIKLMNPQRSTVWY",
            n_trials=n_trials,
            n_cycles=n_cycles,
            gpu_id=self.gpu_id,
            ctx=ctx,
        )
    
    async def design_protein_binder_chai(
        self,
        target_protein_sequence: str,
        design_name: str = "protein_binder",
        target_length: int = 120,
        percent_X: int = 80,
        n_trials: int = 1,
        n_cycles: int = 5,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder for a target protein using Chai (Example 2: protein binder).
        
        Designs a protein that binds to a specific target protein sequence.
        Long-running task: 5-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence to design a binder for
            design_name: Name for this design run (default: "protein_binder")
            target_length: Length of binder protein (default: 120)
            percent_X: Percentage of X residues for diversity (default: 80)
            n_trials: Number of design trials to generate (default: 1)
            n_cycles: Number of design cycles (default: 5)
        
        Returns:
            dict: Results with output directory contents and status
            
        Example:
            Input: target_protein_sequence="AFTVTVPKDLYVVEYGSNMTIECKFPVEKQLDLAALIVYWEMEDKNIIQFVHGEEDLKVQHSSYRQRARLLKDQLSLGNAALQITDVKLQDAGVYRCMISYGGADYKRITVKVNAPYAAALE"
            Output: {"status": "completed", "results": [...]}
        """
        return await self._run_chai_design(
            jobname=design_name,
            length=target_length,
            percent_X=percent_X,
            seq="",
            target_seq=target_protein_sequence,
            n_trials=n_trials,
            n_cycles=n_cycles,
            gpu_id=self.gpu_id,
            use_msa_for_af3=True,
            ctx=ctx,
        )
    
    async def design_cyclic_peptide_binder_chai(
        self,
        target_protein_sequence: str,
        design_name: str = "cyclic_peptide_binder",
        target_length: int = 15,
        percent_X: int = 80,
        n_trials: int = 1,
        n_cycles: int = 5,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a cyclic peptide binder for a target protein using Chai (Example 3: cyclic peptide).
        
        Designs short cyclic peptides that bind to target proteins.
        Long-running task: 5-10 minutes per design on an H100 GPU.
        
        Args:
            target_protein_sequence: Target protein sequence
            design_name: Name for this design run (default: "cyclic_peptide_binder")
            target_length: Length of cyclic peptide (default: 15)
            percent_X: Percentage of X residues (default: 80)
            n_trials: Number of design trials to generate (default: 1)
            n_cycles: Number of design cycles (default: 5)
        
        Returns:
            dict: Results with output directory contents and status
        """
        return await self._run_chai_design(
            jobname=design_name,
            length=target_length,
            percent_X=percent_X,
            seq="",
            target_seq=target_protein_sequence,
            cyclic=True,
            n_trials=n_trials,
            n_cycles=n_cycles,
            gpu_id=self.gpu_id,
            use_msa_for_af3=True,
            ctx=ctx,
        )
    
    async def design_ligand_binder_chai(
        self,
        ligand_smiles: str,
        design_name: str = "ligand_binder",
        target_length: int = 120,
        percent_X: int = 50,
        n_trials: int = 1,
        n_cycles: int = 5,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Design a protein binder for a small molecule ligand using Chai (Example 4: ligand binder).
        
        Designs proteins that bind to small molecules specified by SMILES strings.
        Long-running task: 5-10 minutes per design on an H100 GPU.
        
        Args:
            ligand_smiles: SMILES string for the target ligand
            design_name: Name for this design run (default: "ligand_binder")
            target_length: Length of binder protein (default: 120)
            percent_X: Percentage of X residues (default: 50, matches example)
            n_trials: Number of design trials to generate (default: 1)
            n_cycles: Number of design cycles (default: 5)
        
        Returns:
            dict: Results with output directory contents and status
            
        Example:
            Input: ligand_smiles="O=C(NCc1cocn1)c1cnn(C)c1C(=O)Nc1ccn2cc(nc2n1)c1ccccc1"
            Output: {"status": "completed", "results": [...]}
        """
        return await self._run_chai_design(
            jobname=design_name,
            length=target_length,
            percent_X=percent_X,
            seq="",
            target_seq=ligand_smiles,
            n_trials=n_trials,
            n_cycles=n_cycles,
            gpu_id=self.gpu_id,
            hysteresis_mode="esm",
            temperature=0.01,
            ctx=ctx,
        )
    
    async def design_protein_advanced_chai(
        self,
        jobname: str,
        length: int = 120,
        percent_X: int = 0,
        seq: str = "",
        target_seq: str = "",
        n_trials: int = 1,
        n_cycles: int = 5,
        # Optional parameters with defaults
        cyclic: bool = False,
        n_recycles: int = 3,
        n_diff_steps: int = 200,
        hysteresis_mode: str = "templates",
        repredict: bool = True,
        omit_aa: str = "",
        bias_aa: Optional[str] = None,
        temperature: float = 0.1,
        scale_temp_by_plddt: bool = True,
        render_freq: int = 100,
        use_msa_for_af3: bool = False,
        plot: bool = True,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Advanced Chai design with full parameter control.
        
        Exposes all available parameters for maximum flexibility in protein design.
        Use this when you need fine-grained control over the design process.
        Long-running task: 5-10 minutes per design on an H100 GPU.
        
        Args:
            jobname: Name for this design run
            length: Length of the designed protein chain (default: 120)
            percent_X: Percentage of X (unknown) residues in initial sequence (default: 0)
            seq: Input sequence for the binder chain (optional, default: "")
            target_seq: Target sequence (protein) or SMILES (ligand) for binder design (default: "")
            n_trials: Number of independent optimization trials (default: 1)
            n_cycles: Number of folding/design optimization cycles (default: 5)
            cyclic: Enable cyclic topology for the designed chain (default: False)
            n_recycles: Number of trunk recycles per fold step (default: 3)
            n_diff_steps: Diffusion steps for structure sampling (default: 200)
            hysteresis_mode: Strategy for template/feature reuse - "templates", "esm", "partial_diffusion", or "none" (default: "templates")
            repredict: Re-predict final best structure without templates for validation (default: True)
            omit_aa: Amino acid types to omit from design (e.g., "C") (default: "")
            bias_aa: Amino acid types to bias (e.g., "A:-2.0,P:-1.0") (default: None)
            temperature: ProteinMPNN sampling temperature (default: 0.1)
            scale_temp_by_plddt: Scale MPNN temperature inversely by pLDDT for focused design (default: True)
            render_freq: Visualization refresh frequency in diffusion steps (default: 100)
            use_msa_for_af3: Use MSA for AlphaFold3 validation (default: False)
            plot: Generate plots for design cycles (default: True)
        
        Returns:
            dict: Results with output directory contents and status
        """
        return await self._run_chai_design(
            jobname=jobname,
            length=length,
            percent_X=percent_X,
            seq=seq,
            target_seq=target_seq,
            n_trials=n_trials,
            n_cycles=n_cycles,
            gpu_id=self.gpu_id,
            cyclic=cyclic,
            n_recycles=n_recycles,
            n_diff_steps=n_diff_steps,
            hysteresis_mode=hysteresis_mode,
            repredict=repredict,
            omit_aa=omit_aa,
            bias_aa=bias_aa,
            temperature=temperature,
            scale_temp_by_plddt=scale_temp_by_plddt,
            render_freq=render_freq,
            use_msa_for_af3=use_msa_for_af3,
            plot=plot,
            ctx=ctx,
        )
    
    async def _run_chai_design(
        self,
        jobname: str,
        length: int,
        percent_X: int,
        seq: str,
        target_seq: str,
        n_trials: int,
        n_cycles: int,
        gpu_id: int,
        # Optional parameters with defaults
        cyclic: bool = False,
        n_recycles: int = 3,
        n_diff_steps: int = 200,
        hysteresis_mode: str = "templates",
        repredict: bool = True,
        omit_aa: str = "",
        bias_aa: Optional[str] = None,
        temperature: float = 0.1,
        scale_temp_by_plddt: bool = True,
        render_freq: int = 100,
        use_msa_for_af3: bool = False,
        plot: bool = True,
        ctx: Context = None,
    ) -> dict[str, str]:
        """Internal method to run Chai protein design with all optional parameters.
        
        This is the least common denominator for all Chai design tools. It handles
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
                "python", str(protein_hunter_dir / "chai_ph" / "design.py"),
                "--jobname", jobname,
                "--length", str(length),
                "--percent_X", str(percent_X),
                "--seq", seq,
                "--target_seq", target_seq,
                "--n_trials", str(n_trials),
                "--n_cycles", str(n_cycles),
                "--n_recycles", str(n_recycles),
                "--n_diff_steps", str(n_diff_steps),
                "--hysteresis_mode", hysteresis_mode,
                "--omit_aa", omit_aa,
                "--temperature", str(temperature),
                "--render_freq", str(render_freq),
                "--gpu_id", str(gpu_id),
            ]
            
            # Add optional bias_aa parameter
            if bias_aa:
                cmd.extend(["--bias_aa", bias_aa])
            
            # Add boolean flags
            if cyclic:
                cmd.append("--cyclic")
            if repredict:
                cmd.append("--repredict")
            if scale_temp_by_plddt:
                cmd.append("--scale_temp_by_plddt")
            if use_msa_for_af3:
                cmd.append("--use_msa_for_af3")
            if plot:
                cmd.append("--plot")
            
            # Report initial progress
            total_steps = n_trials * n_cycles
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
            current_trial = 0
            current_cycle = 0
            
            # Read stdout line by line to track progress
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                    
                line_str = line.decode().strip()
                
                # Parse progress from output patterns
                # Actual format: "./results_chai/{jobname}/run_X | Step Y: ..."
                if "run_" in line_str and " | Step" in line_str:
                    try:
                        # Extract run number (trial)
                        run_parts = line_str.split("run_")
                        if len(run_parts) > 1:
                            run_num = run_parts[1].split(" ")[0].split("/")[0]
                            current_trial = int(run_num)
                        
                        # Extract step number (cycle)
                        if "Step" in line_str:
                            step_parts = line_str.split("Step")
                            if len(step_parts) > 1:
                                step_num = step_parts[1].split(":")[0].strip()
                                current_cycle = int(step_num)
                                
                                progress = current_trial * n_cycles + current_cycle
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
            
            # Find the output directory (Chai stores results differently than Boltz)
            output_dir = protein_hunter_dir / "results_chai" / jobname
            
            if not output_dir.exists():
                # Try alternative path structure if the above doesn't exist
                output_dir = protein_hunter_dir / "outputs" / jobname
            
            if not output_dir.exists():
                return {
                    "status": "error",
                    "error": f"Output directory not found at {output_dir}. Design may have failed."
                }
            
            # Read results from output directory for LLM-friendly response
            try:
                results = []
                # Look for run directories
                for run_dir in sorted(output_dir.glob("run_*")):
                    if not run_dir.is_dir():
                        continue
                    
                    run_info = {"run": run_dir.name}
                    
                    # Look for final PDB file
                    pdb_files = list(run_dir.glob("*.pdb"))
                    if pdb_files:
                        run_info["pdb_file"] = str(pdb_files[-1])
                    
                    # Look for metrics JSON if available
                    metrics_file = run_dir / "metrics.json"
                    if metrics_file.exists():
                        with open(metrics_file, 'r') as f:
                            run_info["metrics"] = json.load(f)
                    
                    # Look for sequence file
                    seq_file = run_dir / "sequence.txt"
                    if seq_file.exists():
                        with open(seq_file, 'r') as f:
                            run_info["sequence"] = f.read().strip()
                    
                    results.append(run_info)
                
                return {
                    "status": "completed",
                    "output_dir": str(output_dir),
                    "jobname": jobname,
                    "num_results": len(results),
                    "results": results
                }
            except Exception as e:
                # Fallback to basic info if reading fails
                return {
                    "status": "completed",
                    "output_dir": str(output_dir),
                    "jobname": jobname,
                    "note": f"Results available but detailed parsing failed: {str(e)}"
                }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }