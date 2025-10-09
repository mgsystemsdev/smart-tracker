# Smart Tracker

## Overview
Smart Tracker is a personal learning tracker with a dual-interface architecture, offering both a Streamlit web interface and a Typer CLI. Its core purpose is to simplify progress tracking by automatically calculating progress from logged hours. The project aims to provide a robust, user-friendly system for logging and visualizing learning efforts, incorporating a hierarchical data model and a comprehensive KPI dashboard. It features MG System Dev branding with golden yellow accents and a dark tech theme.

**Current State:** Blank canvas - database is initialized but contains no pre-loaded categories or technologies. Users start with an empty system and add their own custom data through the Dropdown Manager.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture
The application is built around a single Streamlit web interface with a wide layout and multi-page navigation. It follows a modular page design, where each page is a separate Python file, simplifying development and maintenance. The core data management adheres to a database-first approach, utilizing SQLite as the primary data store, ensuring all data operations are handled consistently.

**Key Architectural Decisions & Design Patterns:**
-   **Modular Page Design**: Each page (`home_dashboard.py`, `log_session.py`, etc.) is a standalone module, making the application scalable and easy to navigate.
-   **Database-First Approach**: All data persistence is handled via SQLite, migrating away from file-based storage to ensure data integrity and consistency.
-   **Service Layer Architecture**: Business logic is encapsulated in dedicated services, such as `TechnologySyncService` and `CategorySyncService` for atomic data synchronization across tables, and `CachedQueryService` for optimizing read performance.
-   **Performance Patterns**: Includes query batching, aggressive caching with manual invalidation on writes, and deferred saves for form submissions to enhance responsiveness and data consistency.
-   **Hierarchical Data Model**: Employs a 4-level cascading dropdown system (Category → Technology → Work Item → Skill/Topic) for structured data entry and management.
-   **UI/UX**: Features a professional "SYSTEM DEV | Real-Time Operations Dashboard" branding, with sections defaulting to collapsed for a cleaner interface and critical metrics always visible at the top.

**Core Features & Implementations:**
-   **Database Schema**: Comprises `sessions`, `tech_stack`, `categories`, and `dropdowns` tables.
-   **Enhanced Session Model**: Sessions include 13 fields with hierarchical categories, work items, and skill topics, supporting tracking of "Studying" and "Practice" session types.
-   **Cascading Dropdowns**: Fixed dropdown dependency filtering - child dropdowns now show empty options (not all) when parent is unselected, ensuring proper hierarchical filtering.
-   **KPI Dashboard**: Provides real-time metrics including total sessions, hours, technology count, and overall progress.
-   **Analytics Dashboard**: Advanced performance dashboard with hierarchical data breakdowns:
    - Categories Analytics: Time distribution and technology breakdown per category
    - Technologies Analytics: Work item distribution and hours per technology
    - Work Items Analytics: Skill breakdown and session type split per work item
-   **Dropdown Manager**: Consolidated data management hub with 4 tabs:
    - Manage Categories: Add, rename, delete, merge categories
    - Manage Technologies: Add, edit, delete technologies with category assignment
    - Manage Dropdowns: Work items and other dropdown values
    - Statistics: Overview of all data
-   **Tech Stack Dashboard**: Visual-only dashboard displaying technology cards with KPIs, progress metrics, and category grouping. Read-only interface for viewing learning progress.
-   **Workload Calculator**: A dedicated page for estimating workload with flexible unit conversions.
-   **Data Consistency**: Unified sync services ensure referential integrity and propagate changes across all related tables, eliminating data drift.

## External Dependencies
-   **Streamlit**: For building the interactive web user interface.
-   **Typer**: For developing the command-line interface.
-   **Python 3.11+**: The minimum required Python version.
-   **pip**: For managing project dependencies.
-   **SQLite Database**: The primary data persistence layer (`data/smart_tracker.db`), configured with `check_same_thread=False` for Streamlit compatibility.
-   **pytest**: The testing framework used for development (though tests directory is currently minimal).