# Conda → uv Migration Summary

This document summarizes the migration from the conda-based Protein Hunter setup to a uv-based MCP server.

## Original Setup (Conda-based)

The original `setup.sh` used:
- Conda environment with Python 3.10
- Manual pip installs for various packages
- Local Boltz installation from `boltz_ph/` directory
- Git installation of chai-lab with `--no-deps` flag
- PyRosetta installer (which internally calls pip)
- Bash scripts for downloading model weights
- Manual chmod for executables

## New Setup (uv-based)

### 1. Dependencies in pyproject.toml

All dependencies are now managed through `pyproject.toml`:

#### Resolved via PyPI/Git
- **Boltz**: `boltz[cuda]` - The local `boltz_ph/` is identical to official v2.2.1, so we use PyPI
- **Chai-lab**: `chai-lab @ git+https://github.com/sokrypton/chai-lab.git` - Git dependency
- **All other packages**: Standard PyPI dependencies

#### Version Pinning Preserved
- `rdkit~=2024.9.5` - Overrides Boltz's looser constraint for compatibility
- `logmd==0.1.45` - Exact version pinning maintained

#### Dev Dependencies
- pytest, pytest-asyncio, mypy, ruff, ipykernel moved to `[project.optional-dependencies]`

### 2. Post-Installation Script (postinstall.py)

All complex setup tasks are handled by a Python script:

#### PyRosetta Installation (The Tricky Part)
**Problem**: `pyrosetta_installer` uses `subprocess.check_call(f'pip install {url}', shell=True)`, bypassing uv.

**Solution**: PATH wrapper approach
```python
# Create temporary pip wrapper that redirects to uv pip
wrapper_dir = Path(tempfile.mkdtemp())
pip_wrapper = wrapper_dir / "pip"
pip_wrapper.write_text("#!/bin/bash\nexec uv pip \"$@\"\n")
pip_wrapper.chmod(0o755)

# Prepend to PATH before running pyrosetta_installer
os.environ["PATH"] = f"{wrapper_dir}:{old_path}"
```

#### Other Tasks (Pure Python)
- **Boltz weights**: `boltz.main.download_boltz2()` to `~/.boltz`
- **LigandMPNN models**: Pure Python downloads with `urllib.request.urlretrieve()`
  - 15 model files from `https://files.ipd.uw.edu/pub/ligandmpnn/`
  - Skips existing files
- **DAlphaBall.gcc**: `Path.chmod(0o755)` in Python
- **Verification**: Import checks for boltz, chai_lab, pyrosetta

### 3. Installation Process

Simple two-step process:

```bash
# 1. Install dependencies
uv sync

# 2. Run post-installation
uv run postinstall.py
```

For development:
```bash
uv sync --extra dev
```

## Key Benefits

1. **No Conda Required**: Pure Python packaging with uv
2. **Reproducible**: All dependencies locked in uv.lock
3. **Faster**: uv's resolver is much faster than conda
4. **Standard Tools**: Uses standard Python packaging (PEP 517/518)
5. **Transparent**: All setup steps visible in Python code
6. **Idempotent**: postinstall.py can be run multiple times safely

## Technical Details

### PATH Wrapper Strategy
The PATH wrapper works because:
1. PyRosetta installer calls `pip` as a shell command
2. Shell searches PATH from left to right
3. Our wrapper is prepended to PATH
4. Wrapper redirects all `pip` calls to `uv pip`
5. uv pip maintains the virtual environment correctly

### Deduplication
Avoided duplicate dependencies:
- `tqdm`, `pyyaml`, `requests`, `numpy`, `numba` already in Boltz
- `gemmi`, `biopython`, `modelcif` already in Boltz
- Only added unique dependencies or version overrides

### Optional Components
The postinstall script gracefully handles missing components:
- LigandMPNN directory may not exist
- DAlphaBall.gcc may not exist
- Import verification reports but doesn't fail on warnings

## Files Created/Modified

### New Files
- `postinstall.py` - Complete post-installation handler
- `MIGRATION.md` - This document

### Modified Files
- `pyproject.toml` - Complete dependency specification
- `README.md` - Updated installation instructions

### Unchanged
- `Protein-Hunter/` directory - Original codebase intact
- `setup.sh` - Kept for reference

## Testing the Migration

To verify the migration works:

1. Fresh environment test:
   ```bash
   cd /data/sources/protein_hunter_mcp
   rm -rf .venv uv.lock  # Clean slate
   uv sync
   uv run postinstall.py
   ```

2. Verify imports:
   ```bash
   uv run python -c "import boltz; import chai_lab; import pyrosetta; print('✅ All imports successful')"
   ```

3. Check model weights:
   ```bash
   ls -lh ~/.boltz/  # Boltz weights
   ls -lh Protein-Hunter/LigandMPNN/model_params/  # LigandMPNN models
   ```

## Future Considerations

1. **CI/CD**: Can now use standard Python CI tools
2. **Docker**: Easier to containerize with uv
3. **Pre-commit hooks**: ruff and mypy already configured
4. **Testing**: pytest framework ready in dev dependencies

