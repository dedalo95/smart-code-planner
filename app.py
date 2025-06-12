#!/usr/bin/env python3

"""
Streamlit launcher that handles imports correctly.
"""

import sys
import os
import streamlit as st

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 Coder Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def test_imports():
    """Test if all required modules can be imported."""
    try:
        from src.core.models import SubTask, TaskAnalysisResult, AgentState
        from src.core.config import settings
        from src.services.task_analyzer import TaskAnalyzer
        from src.services.code_advisor import CodeAdvisor
        from src.agent.graph import CoderAssistantGraph
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """Main application entry point."""
    
    # Display graph visualization in terminal when starting
    try:
        from src.agent.graph import CoderAssistantGraph
        graph = CoderAssistantGraph()
        print("\n" + "="*80)
        print("🚀 STARTING CODER ASSISTANT APPLICATION")
        print("="*80)
        graph.print_graph_visualization()
        print("="*80 + "\n")
    except Exception as e:
        print(f"Warning: Could not display graph visualization: {e}")
    
    # Test imports first
    imports_ok, error = test_imports()
    
    if not imports_ok:
        st.error(f"❌ Import Error: {error}")
        st.info("This usually means the Python path is not set correctly.")
        st.code(f"Current working directory: {os.getcwd()}")
        st.code(f"Python path: {sys.path}")
        return
    
    st.success("✅ All modules imported successfully!")
    
    # Import the actual UI
    try:
        from src.ui.streamlit_app import StreamlitUI
        ui = StreamlitUI()
        ui.run()
    except Exception as e:
        st.error(f"❌ Error running UI: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
