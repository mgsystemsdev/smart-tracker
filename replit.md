# Smart Tracker

## Overview

Smart Tracker is a minimal personal learning tracker featuring a simplified workflow: just log your work and see your progress automatically. Built with a dual-interface architecture, it provides both a modern Streamlit web interface and a Typer CLI. The tracker eliminates manual progress tracking - progress is automatically calculated from hours logged. Features MG System Dev branding with golden yellow accents and a dark tech theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (October 8, 2025)

### 🎉 Smart Tracker v2.0 - Complete Platform Redesign
Major architectural upgrade transitioning from JSON-based storage to SQLite database with enhanced hierarchical data model and comprehensive KPI dashboard system.

#### Database Migration & Infrastructure
- **SQLite Database**: Migrated from JSON files to SQLite (`data/smart_tracker.db`) with 4-table schema (sessions, tech_stack, categories, dropdowns)
- **Threading Fix**: Implemented `check_same_thread=False` for Streamlit multi-threaded compatibility
- **Data Migration**: Successfully migrated existing data (5 sessions, 3 technologies, 13.2 hours) from JSON to SQLite
- **Auto Backup**: Migration creates timestamped backups before conversion for data safety

#### Enhanced Session Model (13 Fields)
- **Hierarchical Structure**: Category Name → Technology → Work Item → Skill/Topic cascade system
- **New Fields**: session_id, session_date, category_name, technology, work_item, skill_topic, notes, tags, session_type, difficulty, status, hours_logged, date_added
- **Session Types**: Integrated "Studying" and "Practice" tracking for 20/80 rule monitoring
- **Smart Validation**: Hours (0-12), no future dates, required technology field

#### New Page Architecture
- **Home KPI Dashboard** (`home_kpi_dashboard.py`): Real-time metrics with Total Sessions, Total Hours, Technologies count, Overall Progress percentage
- **Tech Stack CRUD** (`tech_stack_crud_page.py`): Dedicated technology management interface (removed from Home)
- **Calculator** (`calculator_page.py`): Workload estimation with flexible unit conversion (hours/days/weeks/months) and scenario planning
- **Dropdown Manager** (`dropdown_manager_page.py`): Centralized dropdown data management for cascading selectors with type-to-add functionality

#### Cascading Dropdown System
- **4-Level Hierarchy**: Category Name (root) → Technology → Work Item → Skill/Topic (leaf)
- **Auto-Population**: Child dropdowns populate based on parent selection
- **Type-to-Add**: Create new dropdown options on-the-fly during session entry
- **Centralized Management**: Single source of truth in dropdown_manager page

#### UI/UX Improvements
- **Professional Branding**: "SYSTEM DEV | Real-Time Operations Dashboard" subtitle on header
- **Default Collapsed**: All sections start collapsed except Grand Total for cleaner interface
- **Top-Load Behavior**: Critical metrics and controls always visible at page top
- **Cross-Page Sync**: Database ensures data consistency across all pages automatically

#### Navigation Structure
New streamlined navigation with dedicated pages:
1. 🏠 Home Dashboard (KPI metrics only)
2. 📚 Sessions (view/manage)
3. 📝 Log Session (create new)
4. 🎯 Tech Stack CRUD (manage technologies)
5. 📋 Planning (roadmap view)
6. 🧮 Calculator (workload estimation)
7. ⚙️ Dropdown Manager (data management)

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
- **SQLite Database**: Primary storage in `data/smart_tracker.db` with 4-table relational schema
- **Database Tables**: 
  - `sessions`: Learning session records with 13 fields
  - `tech_stack`: Technology inventory with goals and progress tracking
  - `categories`: Category definitions with emojis and metadata
  - `dropdowns`: Hierarchical dropdown options for cascading selectors
- **Threading Support**: Configured with `check_same_thread=False` for Streamlit multi-threading
- **Automatic Backup**: Migration utility creates timestamped JSON backups before database conversion
- **Data Migration**: Built-in utility (`migrate_to_db.py`) converts legacy JSON data to SQLite

### CRUD Operations (Database-Driven)
- **Create**: Add sessions via Log Session page with cascading dropdowns and auto-save to database
- **Read**: View sessions in Sessions page with real-time database queries
- **Update**: Edit sessions/technologies through dedicated CRUD pages with instant database sync
- **Delete**: Remove records with database cascade handling for referential integrity
- **Export**: CSV export functionality for external analysis and reporting