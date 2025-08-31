"""
Smart Tracker Streamlit Web Application.

A web-based interface for the Smart Tracker application using Streamlit.
"""

import streamlit as st
from smarttracker import __version__

def main():
    """Main Streamlit application function."""
    # Page configuration
    st.set_page_config(
        page_title="Smart Tracker",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main header
    st.title("📊 Smart Tracker")
    st.subheader("Your Personal Tracking Application")
    
    # Version info in sidebar
    with st.sidebar:
        st.info(f"Version: {__version__}")
        st.markdown("---")
        st.markdown("### Navigation")
        st.markdown("Welcome to Smart Tracker! This is a scaffold application ready for development.")
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## Hello, world! 👋")
        st.markdown("""
        Welcome to Smart Tracker! This is the foundation of your tracking application.
        
        ### Ready for Development
        - ✅ Streamlit web interface
        - ✅ Typer CLI interface  
        - ✅ Organized package structure
        - ✅ Domain and app layers
        - ✅ Testing framework ready
        
        ### Next Steps
        1. Implement your tracking models in `smarttracker/domain/`
        2. Add business logic and services
        3. Expand the web interface with tracking features
        4. Enhance the CLI with tracking commands
        5. Add comprehensive tests
        """)
        
        # Interactive demo section
        st.markdown("### Quick Demo")
        if st.button("🎉 Click me!", type="primary"):
            st.balloons()
            st.success("Smart Tracker is working perfectly!")
        
        # Info about the application
        with st.expander("📖 About This Application"):
            st.markdown("""
            This Smart Tracker application is built with:
            - **Streamlit** for the web interface
            - **Typer** for the command-line interface
            - **Pydantic** for data validation (ready to use)
            - **Python 3.11+** compatibility
            
            The application follows a clean architecture with separated concerns:
            - `domain/` - Business logic and models
            - `app/` - User interface implementations
            - `cli.py` - Command-line interface
            """)

if __name__ == "__main__":
    main()
