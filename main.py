#!/usr/bin/env python3
"""
Main entry point for Smart Tracker application.
Runs the Streamlit web application.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Streamlit web application."""
    app_path = Path(__file__).parent / "src" / "core" / "app.py"
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        str(app_path), "--server.port=5000", "--server.address=0.0.0.0"
    ])

if __name__ == "__main__":
    main()
