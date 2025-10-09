# Smart Tracker

## Overview

Smart Tracker is a minimal personal learning tracker featuring a simplified workflow: just log your work and see your progress automatically. Built with a dual-interface architecture, it provides both a modern Streamlit web interface and a Typer CLI. The tracker eliminates manual progress tracking - progress is automatically calculated from hours logged. Features MG System Dev branding with golden yellow accents and a dark tech theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### October 9, 2025 - Data Consistency Unification (Blueprint → Database Migration)
**Single Source of Truth Achieved**: Eliminated all hardcoded data conflicts by migrating PLANNING_BLUEPRINT to database
- **Bootstrap Migration** (`bootstrap_blueprint.py`):
  - One-time migration script loads all PLANNING_BLUEPRINT categories and technologies into database
  - 6 categories loaded as built-in (is_custom=0): Core Full-Stack Development, Development Tooling & DevOps, etc.
  - 37 technologies loaded with proper category relationships and goal hours
  - Uses CategorySyncService and TechnologySyncService for atomic writes to all tables
- **Dropdown Manager Refactored** (`pages/dropdown_manager.py`):
  - Now uses CategorySyncService for category additions (syncs to categories + dropdowns tables)
  - Now uses TechnologySyncService for technology additions (syncs to tech_stack + dropdowns tables)
  - Other fields (work_item, skill_topic, session_type, etc.) use direct dropdown writes
  - Cache invalidation after all additions ensures real-time updates
- **Planning Page Verified**: Already reads from database via db.get_all_tech_stack(), no hardcoded blueprint
- **Consistency Audit** (`audit_consistency.py`):
  - Automated script to verify data sync across categories, tech_stack, dropdowns, sessions tables
  - Technologies 100% consistent across all tables ✅
  - Categories mostly consistent (minor legacy subcategory names in categories table)
- **Architecture Impact**:
  - Zero conflicts between hardcoded PLANNING_BLUEPRINT and database
  - All pages (Planning, Log Session, Tech Stack, Dropdown Manager) read from same database source
  - Adding category/technology in any page now propagates to ALL tables via sync services
  - Single source of truth: Database is authoritative for all dropdown and planning data

### October 9, 2025 - Performance & Data Flow Architecture v2.0
**Critical Logic Breaks Fixed**: Eliminated 11 critical data flow issues through unified sync services, query batching, and race condition resolution
- **Unified Data Sync Services** (`services/sync_service.py`):
  - `TechnologySyncService`: Atomic writes to BOTH tech_stack AND dropdowns tables (eliminates data drift)
  - `CategorySyncService`: Syncs categories ↔ dropdowns with batch operations
  - Referential integrity checks with dependency counting before deletions
  - Rename propagation across sessions, tech_stack, and dropdowns
- **Query Performance Optimization** (`services/cached_queries.py`):
  - Batched aggregation queries eliminate N+1 patterns (reduced 700+ queries to ~7 per page load)
  - `@st.cache_data` decorators with 60-second TTL caching
  - Manual cache invalidation on ALL write operations (add/update/delete)
  - True SQL aggregation for category stats (no row limits, scales infinitely)
- **Form-Dropdown Race Condition Fixed** (`utils/cascading_dropdowns_v2.py`):
  - DropdownManagerV2 with deferred save pattern (collects values in session state)
  - Batch save only on explicit form submit (Enter key no longer triggers unwanted submit)
  - Cascading state management: auto-clear children when parent changes
- **Cache Invalidation Architecture**:
  - Log Session: Invalidates cache immediately after successful session save
  - Sessions Delete: Invalidates cache after delete operation
  - Tech Stack CRUD: Sync service handles invalidation on all writes
  - Dashboard metrics refresh in real-time after any write operation
- **Architecture Impact**:
  - Tech Stack CRUD now uses sync services (no more manual table writes)
  - Home Dashboard uses batched cached queries (instant load times)
  - Zero data drift between tech_stack and dropdowns tables
  - Referential integrity warnings prevent orphaned data

### October 9, 2025 - Simplified Log Session Form (Dropdown/Text Separation)
**User-Driven Improvement**: Redesigned Log Session form for cleaner, more intuitive data entry
- **Structured Fields (Dropdown Only)**: Category, Technology, Work Item now use dropdown-only selection
  - Removed text input boxes from these fields to eliminate confusion
  - Users must select from existing options (managed via Dropdown Manager or Tech Stack CRUD)
  - Cascading still works: child dropdowns filter based on parent selection
- **Freeform Field (Text Only)**: Skill/Topic now uses text input only
  - Removed dropdown for Skill/Topic (it's specific to each session)
  - Pure text input for flexible, session-specific details
- **Clearer Workflow**:
  1. Select Category from dropdown
  2. Select Technology from filtered dropdown
  3. Select Work Item from filtered dropdown
  4. Type Skill/Topic directly (freeform text)
- **Benefits**: Less visual clutter, faster data entry, clear separation between structured hierarchy and freeform details

### October 9, 2025 - Architecture Simplification & Excel-Style Dropdowns
**Beginner-Friendly Restructure**: Complete reorganization from nested smarttracker/app/ to flat, intuitive structure
- **Page Extraction**: Moved all page functions from monolithic app.py (1365 lines) to dedicated modules in pages/ directory
- **Clean Routing**: app.py reduced to 374 lines, now serves as lightweight router with page imports
- **Legacy Cleanup**: Removed smarttracker/ folder, JSON files, backup folders, empty tests/ directory
- **Excel-Style Dropdowns**: Implemented always-visible cascading dropdowns with inline write functionality
  - All 4 hierarchical fields visible simultaneously (Category → Technology → Work Item → Skill/Topic)
  - Smart filtering: Child dropdowns filter based on parent selection (like Excel data validation)
  - Helper tooltips when parent not selected
- **Dropdown Data Migration**: Populated dropdowns table with existing technologies from sessions
- **Path Fixes**: Updated main.py to reference app.py instead of deleted smarttracker paths
- **Verification**: All imports tested, database structure validated, no orphaned references
- **Deployment Note**: Streamlit Cloud deployment requires manual update to use app.py as main module

### October 8, 2025 - Smart Tracker v2.0 Platform Redesign
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

### Beginner-Friendly Folder Structure
The application uses a simple, flat structure that's easy to understand:

```
smart-tracker/
├── app.py                         # Main Streamlit application
├── main.py                        # Entry point (workflow runner)
├── database/
│   └── operations.py              # All database operations
├── services/
│   ├── sync_service.py            # TechnologySyncService, CategorySyncService
│   └── cached_queries.py          # CachedQueryService with batched queries
├── pages/
│   ├── home_dashboard.py          # KPI dashboard
│   ├── sessions.py                # View/edit sessions
│   ├── log_session.py             # Create new session
│   ├── tech_stack.py              # Tech stack management
│   ├── planning.py                # Planning & roadmap
│   ├── calculator.py              # Workload calculator
│   └── dropdown_manager.py        # Dropdown data manager
├── utils/
│   ├── cascading_dropdowns_v2.py  # DropdownManagerV2 (race condition fixed)
│   └── cascading_dropdowns.py     # Legacy dropdown logic
├── data/                          # SQLite database
└── logs/                          # Application logs
```

### Interface Architecture
**Single Streamlit Interface**: The application is a web-based Streamlit app with:
- Wide layout with expandable sidebar
- Port 5000 binding with external accessibility (0.0.0.0)
- Multi-page navigation system
- MG System Dev branding with golden yellow accents

### Design Patterns
**Modular Page Design**: Each page is a separate Python file with a single function that renders that page. This makes it easy to:
- Find and edit specific features
- Understand what each page does
- Add new pages without touching existing code

**Database-First Approach**: All data operations go through the `DatabaseStorage` class in `database/operations.py`. No JSON files, no legacy storage - just clean SQLite operations.

**Service Layer Architecture**: Business logic organized in service modules:
- **Sync Services** (`services/sync_service.py`): Ensure data consistency across tech_stack, dropdowns, and sessions tables with atomic operations
- **Cached Queries** (`services/cached_queries.py`): Optimize read performance with batched aggregations and intelligent caching
- **Dropdown Management** (`utils/cascading_dropdowns_v2.py`): Handle form state and cascading logic with race condition prevention

**Performance Patterns**:
- Query Batching: Single aggregated query instead of N individual queries
- Aggressive Caching: 60-second TTL with manual invalidation on writes
- Deferred Saves: Collect form values in session state, batch save on submit
- Real-time Refresh: Cache invalidation ensures dashboard updates immediately after writes

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