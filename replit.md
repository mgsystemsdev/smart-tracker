# Smart Tracker

## Overview

Smart Tracker is a minimal personal learning tracker featuring a simplified workflow: just log your work and see your progress automatically. Built with a dual-interface architecture, it provides both a modern Streamlit web interface and a Typer CLI. The tracker eliminates manual progress tracking - progress is automatically calculated from hours logged. Features MG System Dev branding with golden yellow accents and a dark tech theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (October 4, 2025)

### Simplified Progress Tracking
- **Removed Manual Progress**: No more progress sliders or target hours - progress auto-calculates from logged hours
- **Card-Based Dashboard**: Replaced complex charts with simple expandable cards grouped by technology
- **Minimal Tech Stack**: Starts with just Python (Language category), user adds technologies as they progress
- **Categories**: Technologies organized as "Language" or "Library"

### Dashboard Features
- **Expandable Cards**: Each technology shows total hours, session count, and last session date
- **Full Session Details**: Cards expand to show all sessions with complete information (date, topic, notes, tags, type, difficulty, status, hours)
- **Inline Actions**: Edit and Delete buttons within expanded cards for easy management
- **Auto-Update**: Cards refresh automatically when sessions are added, edited, or deleted

## System Architecture

### Package Structure
The application follows a layered architecture pattern with clear separation of concerns:

- **Domain Layer** (`smarttracker/domain/`): Reserved for core business logic, models, and domain services
- **Application Layer** (`smarttracker/app/`): Contains user interface implementations
- **CLI Interface** (`smarttracker/cli.py`): Command-line interface using Typer framework
- **Entry Point** (`main.py`): Unified entry point that routes to appropriate interface

### Interface Architecture
**Dual Interface Design**: The application supports two distinct user interaction modes:
- **Web Interface**: Streamlit-based web application for visual interaction
- **CLI Interface**: Typer-based command-line tools for programmatic access

**Unified Entry Point**: Single `main.py` file that intelligently routes to either the Streamlit web app or CLI based on command-line arguments.

### Frontend Architecture
**Streamlit Web Application**: 
- Configured for wide layout with expandable sidebar
- Port 5000 binding with external accessibility (0.0.0.0)
- Multi-column responsive layout design
- Version information display in sidebar

**CLI Framework**:
- Typer-based with built-in help system and version callbacks
- Structured for easy command extension
- Tab completion support disabled for simplicity

### Design Patterns
**Modular Package Design**: Clean separation allows for independent development of domain logic and user interfaces. The scaffold structure supports rapid extension without architectural refactoring.

**Framework Abstraction**: Business logic remains independent of UI frameworks, enabling future interface additions without core changes.

## External Dependencies

### Core Frameworks
- **Streamlit**: Web application framework for the visual interface
- **Typer**: Modern CLI framework for command-line interface

### Runtime Environment
- **Python 3.11+**: Minimum required Python version
- **pip**: Package management for dependency installation

### Development Tools
- **pytest**: Testing framework (structure prepared in `tests/` directory)

### Data Persistence & Management
- **JSON Storage**: Learning sessions and tech stack configuration persist across sessions
- **File-based Storage**: Data saved to `data/` directory (excluded from git)
- **Automatic Backup**: Backup functionality available through storage module
- **Session Recovery**: All data automatically loaded on app startup

### CRUD Operations
- **Create**: Add new learning sessions via Smart Learning Tracker
- **Read**: View sessions with filtering and sorting in Clean Dashboard
- **Update**: Edit individual sessions with full-featured edit dialog
- **Delete**: Remove individual sessions or clear all at once
- **Export**: Download all sessions as CSV for external analysis