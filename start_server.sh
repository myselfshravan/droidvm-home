#!/bin/bash
# Quick start script for DroidVM Tools server

echo "Starting DroidVM Tools API server..."
echo "Press Ctrl+C to stop"
echo ""

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "No .env file found. Creating from .env.example..."
    cp .env.example .env
fi

# Start the server
uv run start-server
