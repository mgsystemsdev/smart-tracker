#!/usr/bin/env python3
"""
Main entry point for Smart Tracker application.
This file provides easy access to both the Streamlit app and CLI.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point that delegates to appropriate interface."""
    if len(sys.argv) > 1 and sys.argv[1] == "streamlit":
        # Run Streamlit app
        app_path = Path(__file__).parent / "smarttracker" / "app" / "app_streamlit.py"
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path), "--server.port=5000", "--server.address=0.0.0.0"
        ])
    else:
        # Run CLI
        from smarttracker.cli import app
        app()

if __name__ == "__main__":
    main()
