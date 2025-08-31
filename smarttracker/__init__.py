"""
Smart Tracker - A flexible tracking application.

This package provides both a web interface (Streamlit) and command-line interface (Typer)
for tracking various items, activities, or metrics.
"""

__version__ = "0.1.0"
__author__ = "Smart Tracker Team"
__description__ = "A flexible tracking application with web and CLI interfaces"

# Package-level imports for convenience
from smarttracker.cli import app as cli_app

__all__ = ["cli_app", "__version__"]
