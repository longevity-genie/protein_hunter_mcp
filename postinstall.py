#!/usr/bin/env python3
"""
Post-installation script for Protein Hunter MCP.

Run this after `uv sync`:
    uv run postinstall.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def create_pip_wrapper() -> Path:
    """
    Create a temporary pip wrapper that redirects to uv pip.
    
    Returns:
        Path to the temporary directory containing the wrapper.
    """
    print("🔧 Creating pip wrapper for uv...")
    wrapper_dir = Path(tempfile.mkdtemp(prefix="uv_pip_wrapper_"))
    pip_wrapper = wrapper_dir / "pip"
    
    # Create a wrapper script that calls uv pip
    pip_wrapper.write_text(
        """#!/bin/bash
exec uv pip "$@"
""",
        encoding="utf-8",
    )
    pip_wrapper.chmod(0o755)
    
    print(f"✅ Created pip wrapper at {pip_wrapper}")
    return wrapper_dir


def install_pyrosetta() -> None:
    """Install PyRosetta using the pip wrapper to redirect to uv pip."""
    print("\n⏳ Installing PyRosetta (this may take a while)...")
    
    wrapper_dir = create_pip_wrapper()
    old_path = os.environ.get("PATH", "")
    
    # Prepend wrapper directory to PATH
    os.environ["PATH"] = f"{wrapper_dir}:{old_path}"
    
    try:
        import pyrosetta_installer
        pyrosetta_installer.install_pyrosetta()
        print("✅ PyRosetta installed successfully!")
    except Exception as e:
        print(f"❌ Error installing PyRosetta: {e}")
        sys.exit(1)
    finally:
        # Restore original PATH
        os.environ["PATH"] = old_path
        # Clean up wrapper directory
        try:
            for file in wrapper_dir.iterdir():
                file.unlink()
            wrapper_dir.rmdir()
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up wrapper directory: {e}")


def download_boltz_weights() -> None:
    """Download Boltz weights and dependencies."""
    print("\n⬇️  Downloading Boltz weights and dependencies...")
    
    try:
        from boltz.main import download_boltz2
        
        cache = Path.home() / ".boltz"
        cache.mkdir(parents=True, exist_ok=True)
        download_boltz2(cache)
        print("✅ Boltz weights downloaded successfully!")
    except Exception as e:
        print(f"❌ Error downloading Boltz weights: {e}")
        sys.exit(1)


def download_file(url: str, output_path: Path) -> None:
    """Download a file from URL to output_path."""
    import urllib.request
    
    urllib.request.urlretrieve(url, output_path)


def setup_ligandmpnn() -> None:
    """Setup LigandMPNN model parameters if directory exists."""
    ligandmpnn_dir = Path("Protein-Hunter/LigandMPNN")
    
    if not ligandmpnn_dir.exists():
        print("\n⚠️  LigandMPNN directory not found, skipping...")
        return
    
    print("\n🧬 Setting up LigandMPNN...")
    
    model_params_dir = ligandmpnn_dir / "model_params"
    model_params_dir.mkdir(parents=True, exist_ok=True)
    
    # Model weights to download (from get_model_params.sh)
    base_url = "https://files.ipd.uw.edu/pub/ligandmpnn"
    models = [
        # Original ProteinMPNN weights
        "proteinmpnn_v_48_002.pt",
        "proteinmpnn_v_48_010.pt",
        "proteinmpnn_v_48_020.pt",
        "proteinmpnn_v_48_030.pt",
        # LigandMPNN with num_edges=32; atom_context_num=25
        "ligandmpnn_v_32_005_25.pt",
        "ligandmpnn_v_32_010_25.pt",
        "ligandmpnn_v_32_020_25.pt",
        "ligandmpnn_v_32_030_25.pt",
        # Per residue label membrane ProteinMPNN
        "per_residue_label_membrane_mpnn_v_48_020.pt",
        # Global label membrane ProteinMPNN
        "global_label_membrane_mpnn_v_48_020.pt",
        # SolubleMPNN
        "solublempnn_v_48_002.pt",
        "solublempnn_v_48_010.pt",
        "solublempnn_v_48_020.pt",
        "solublempnn_v_48_030.pt",
        # LigandMPNN for side-chain packing
        "ligandmpnn_sc_v_32_002_16.pt",
    ]
    
    print(f"  Downloading {len(models)} model files...")
    try:
        for model_file in models:
            output_path = model_params_dir / model_file
            if output_path.exists():
                print(f"    ⏭️  {model_file} (already exists)")
                continue
            
            url = f"{base_url}/{model_file}"
            print(f"    ⬇️  {model_file}...")
            download_file(url, output_path)
        
        print("✅ LigandMPNN model parameters downloaded!")
    except Exception as e:
        print(f"❌ Error setting up LigandMPNN: {e}")
        sys.exit(1)


def setup_dalphaball() -> None:
    """Make DAlphaBall.gcc executable."""
    dalphaball_path = Path("Protein-Hunter/utils/DAlphaBall.gcc")
    
    if not dalphaball_path.exists():
        print("\n⚠️  DAlphaBall.gcc not found, skipping...")
        return
    
    print("\n🔧 Making DAlphaBall.gcc executable...")
    
    try:
        dalphaball_path.chmod(0o755)
        print("✅ DAlphaBall.gcc is now executable!")
    except Exception as e:
        print(f"❌ Error making DAlphaBall.gcc executable: {e}")
        sys.exit(1)


def verify_installations() -> None:
    """Verify that key packages are importable."""
    print("\n🔍 Verifying installations...")
    
    packages = [
        "boltz",
        "chai_lab",
        "pyrosetta",
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (import failed)")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️  Warning: Some packages failed to import: {', '.join(failed)}")
        print("    This may be expected for some optional components.")


def main() -> None:
    """Run all post-installation steps."""
    print("🚀 Running Protein Hunter MCP post-installation...\n")
    
    # Step 1: Download Boltz weights
    download_boltz_weights()
    
    # Step 2: Install PyRosetta with pip wrapper
    install_pyrosetta()
    
    # Step 3: Setup LigandMPNN (if available)
    setup_ligandmpnn()
    
    # Step 4: Make DAlphaBall.gcc executable
    setup_dalphaball()
    
    # Step 5: Verify installations
    verify_installations()
    
    print("\n🎉 Post-installation complete!")
    print("\n📝 Next steps:")
    print("   1. Verify all packages imported correctly above")
    print("   2. Start using the MCP server")


if __name__ == "__main__":
    main()

