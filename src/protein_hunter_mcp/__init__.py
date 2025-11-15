#!/usr/bin/env python3
"""Protein Hunter MCP Server - Protein design and analysis tools."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("protein-hunter-mcp")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__"]

