# Smart Tracker

A minimal personal learning tracker with automatic goal-based progress tracking. Built with Streamlit web interface and Typer CLI, featuring MG System Dev branding with golden yellow accents and dark tech theme.

## Features

- 🎯 **Goal-Based Progress**: Set target hours for each technology and track progress automatically
- 📊 **Technology Objects**: Each technology (Python, React, etc.) is a complete object with name, category, goal hours, and progress tracking
- 🌐 **Web Interface**: Modern Streamlit-based dashboard with expandable cards
- 💻 **CLI Interface**: Typer-based command-line tools
- 📦 **Persistent Storage**: JSON-based data persistence for sessions and tech stack
- 🔒 **Data Safety**: Protected clear operations with double confirmation

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install .
   ```
   Or using uv:
   ```bash
   uv pip install -e .
   ```

### Running the Web Application

Start the Streamlit web interface:

```bash
python main.py streamlit
