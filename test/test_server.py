#!/usr/bin/env python3
"""Tests for Protein Hunter MCP Server."""

import pytest
from protein_hunter_mcp.server import ProteinHunterMCP


@pytest.fixture
def server():
    """Create a test server instance."""
    return ProteinHunterMCP(transport_mode="stdio")


@pytest.mark.asyncio
async def test_hello_world_default(server):
    """Test hello_world with default parameters."""
    result = await server.hello_world()
    
    assert "message" in result
    assert "Hello, World!" in result["message"]
    assert "version" in result
    assert "transport" in result
    assert result["transport"] == "stdio"
    assert "output_dir" in result


@pytest.mark.asyncio
async def test_hello_world_custom_name(server):
    """Test hello_world with custom name."""
    result = await server.hello_world(name="Protein Hunter")
    
    assert "message" in result
    assert "Hello, Protein Hunter!" in result["message"]
    assert "version" in result


@pytest.mark.asyncio
async def test_server_initialization():
    """Test server initialization with different modes."""
    # Test stdio mode
    server_stdio = ProteinHunterMCP(transport_mode="stdio")
    assert server_stdio.transport_mode == "stdio"
    assert server_stdio.prefix == "ph_"
    
    # Test http mode
    server_http = ProteinHunterMCP(transport_mode="streamable-http")
    assert server_http.transport_mode == "streamable-http"
    
    # Test sse mode
    server_sse = ProteinHunterMCP(transport_mode="sse")
    assert server_sse.transport_mode == "sse"


def test_server_output_directory(tmp_path):
    """Test custom output directory."""
    custom_dir = tmp_path / "custom_output"
    server = ProteinHunterMCP(transport_mode="stdio", output_dir=str(custom_dir))
    
    assert server.output_dir == custom_dir
    assert server.output_dir.exists()

