# Smart Tracker

A professional personal learning tracker with persistent PostgreSQL database, simplified session entry UX, Excel-style hierarchical dropdown system, and comprehensive KPI dashboard. Features MG System Dev branding with golden yellow accents and dark tech theme.

## Features

- 🎯 **Automatic Progress Tracking**: Log hours and watch progress calculate automatically
- 📊 **Technology Management**: Organize technologies by categories with hierarchical structure
- 🌐 **Streamlit Web Interface**: Modern, responsive dashboard with multi-page navigation
- 🗄️ **PostgreSQL Database**: Permanent data persistence using Replit's managed PostgreSQL (Neon-backed)
- 📋 **Simplified Session Entry**: Free-form session logging with background auto-pairing
- 🔧 **Dropdown Manager**: Unified data management hub for categories, technologies, work items, and skills
- 📈 **Analytics Dashboard**: Hierarchical data breakdowns (Categories → Technologies → Work Items → Skills)
- 🎨 **Professional UI**: "SYSTEM DEV | Real-Time Operations Dashboard" branding
- ✅ **Data Integrity**: Atomic sync services ensure referential integrity across all tables

## Architecture

### Database Schema
- **PostgreSQL** (migrated from SQLite for permanent persistence in Replit)
- Tables: `sessions`, `tech_stack`, `categories`, `dropdowns`, `work_items`, `skills`
- 4-level hierarchical model: Category → Technology → Work Item → Skill/Topic

### Project Structure
```
smart-tracker/
├── src/
│   ├── core/           # Core app logic and configuration
│   │   ├── app.py     # Main Streamlit application
│   │   └── config.py  # Configuration and constants
│   ├── database/       # Database operations
│   │   └── operations.py
│   ├── pages/          # Streamlit pages
│   │   ├── home_dashboard.py
│   │   ├── log_session.py
│   │   ├── dropdown_manager.py
│   │   ├── tech_stack.py
│   │   ├── analytics.py
│   │   └── ...
│   ├── services/       # Business logic services
│   │   ├── sync_service.py
│   │   └── cached_queries.py
│   └── utils/          # Utility functions
│       └── dropdowns.py
├── scripts/            # Utility scripts
│   ├── bootstrap_blueprint.py
│   └── audit_consistency.py
├── main.py             # Entry point
└── requirements.txt    # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (automatically configured in Replit)

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit web interface:

```bash
streamlit run src/core/app.py --server.port=5000 --server.address=0.0.0.0
```

Or use the main entry point:

```bash
python main.py
```

## Database

The application uses **PostgreSQL** for permanent data persistence:

- **Development Database**: Managed by Replit, accessible via `DATABASE_URL` environment variable
- **Migration**: Successfully migrated from SQLite to prevent data loss on app sleep/restart
- **Connection**: Uses `psycopg2-binary` with connection pooling

## Core Pages

### 📊 Home Dashboard
- Real-time KPI metrics
- Total sessions, hours, technologies
- Overall progress tracking

### ✏️ Log Session
- Simplified session entry form
- All options shown without parent filtering
- Background auto-pairing of relationships
- Session types: Studying, Practice

### 🔧 Dropdown Manager
- Unified data management hub
- 4 tabs: Categories, Technologies, Dropdowns, Statistics
- Hierarchical management with Excel-style filtering
- Add, rename, delete, merge operations

### 📈 Analytics Dashboard
- Categories Analytics: Time distribution and technology breakdown
- Technologies Analytics: Work item distribution and hours
- Work Items Analytics: Skill breakdown and session type split

### 🎯 Tech Stack
- Visual technology cards with KPIs
- Progress metrics and category grouping
- Read-only display interface

## Data Management

### Session Entry UX
- **Simplified**: Show all technologies (no category selection required)
- **Free-form**: Show all work items and skills (no parent filtering)
- **Smart**: Category is auto-paired from selected technology in background
- **Analytics-ready**: Relationships preserved for proper data grouping

### Dropdown System
- **Hierarchical Management**: Dropdown Manager uses parent-child filtering
- **Direct Table Reads**: Queries read from source tables (categories, tech_stack, sessions)
- **Hybrid Population**: Work items and skills support both manual definition and auto-population
- **Single Source of Truth**: Eliminates sync issues between tables

## Technology Stack

- **Frontend**: Streamlit 1.49+
- **Database**: PostgreSQL (psycopg2-binary)
- **Python**: 3.11+
- **Data Processing**: Pandas

## Development

### Database Operations
All database operations are in `src/database/operations.py` using PostgreSQL syntax (`%s` placeholders).

### Service Layer
- `TechnologySyncService`: Atomic data synchronization across tables
- `CategorySyncService`: Category management with cascading updates
- `CachedQueryService`: Optimized read performance with manual cache invalidation

### Adding New Pages
1. Create page file in `src/pages/`
2. Import in `src/core/app.py`
3. Add to page navigation dictionary

## Contributing

This is a personal project built for learning tracking. Feel free to fork and customize for your own needs!

## License

MIT
