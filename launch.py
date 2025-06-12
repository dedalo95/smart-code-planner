#!/usr/bin/env python3

"""
Simple launcher for the Streamlit app that handles imports correctly.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now we can import and run the Streamlit app
if __name__ == "__main__":
    from src.ui.streamlit_app import main
    main()
