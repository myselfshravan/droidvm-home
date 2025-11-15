"""Tests for the FastAPI server."""

import pytest
from fastapi.testclient import TestClient

from droidvm_tools.server import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DroidVM Tools API"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"
    assert "timestamp" in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_system_info_endpoint(client):
    """Test the system info endpoint."""
    response = client.get("/system/info")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "hostname" in data["data"]
    assert "platform" in data["data"]


def test_cpu_info_endpoint(client):
    """Test the CPU info endpoint."""
    response = client.get("/system/cpu")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "cpu_usage_percent" in data["data"]


def test_memory_info_endpoint(client):
    """Test the memory info endpoint."""
    response = client.get("/system/memory")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "total" in data["data"]
    assert "percentage" in data["data"]


def test_disk_info_endpoint(client):
    """Test the disk info endpoint."""
    response = client.get("/system/disk")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "partitions" in data["data"]


def test_network_stats_endpoint(client):
    """Test the network stats endpoint."""
    response = client.get("/network/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_full_status_endpoint(client):
    """Test the full status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "system" in data["data"]
    assert "cpu" in data["data"]
    assert "memory" in data["data"]
    assert "network" in data["data"]
