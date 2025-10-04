# Smart Tracker

A minimal personal learning tracker with automatic goal-based progress tracking. Built with Streamlit web interface and Typer CLI, featuring MG System Dev branding with golden yellow accents and dark tech theme.

## Features

- 🎯 **Goal-Based Progress**: Set target hours for each technology and track progress automatically
- 📊 **Technology Objects**: Each technology (Python, React, etc.) is a complete object with name, category, goal hours, and progress tracking
- 🌐 **Web Interface**: Modern Streamlit-based dashboard with expandable cards
- 💻 **CLI Interface**: Typer-based command-line tools
- 📦 **Persistent Storage**: JSON-based data persistence for sessions and tech stack
- 🔒 **Data Safety**: Protected clear operations with double confirmation
- ✅ **Data Integrity**: Input validation ensures accurate tracking
- 🪵 **Activity Logging**: Complete audit trail of all operations

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
```

## Data Integrity & Logging

Smart Tracker includes built-in validation and logging to ensure data accuracy and provide an audit trail.

### Validation Rules

The app enforces these rules when adding or editing sessions:

- ✅ **Hours**: Must be between 0 and 12 (inclusive) - allows quick logs or placeholder entries
- ✅ **Dates**: Cannot be in the future (prevents accidental future entries)
- ✅ **Technology**: Cannot be empty; custom technologies are automatically added to your tech stack

If validation fails, you'll see a clear error message explaining the issue, and no invalid data will be saved.

### Activity Logging

All actions are automatically logged to `/logs/activity.log` for debugging and audit purposes:

- **Added sessions**: `Added session: 2h Python (2025-10-04)`
- **Edited sessions**: `Edited session #3: 3.5h Pandas (2025-10-03)`
- **Deleted sessions**: `Deleted session #7: 1.5h SQL (2025-10-02)`
- **Validation failures**: `Validation failed: ⚠️ Hours must be between 0 and 12 | ...`

Logs include timestamps, operation type, and relevant details for complete traceability
