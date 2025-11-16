"""Shared lock for ensuring only one design process runs at a time."""

import asyncio

# Global lock shared between Boltz and Chai design processes
_design_lock: asyncio.Lock | None = None


def get_design_lock() -> asyncio.Lock:
    """Get or create the global design lock.
    
    Returns:
        asyncio.Lock: Shared lock for design processes
    """
    global _design_lock
    if _design_lock is None:
        _design_lock = asyncio.Lock()
    return _design_lock

