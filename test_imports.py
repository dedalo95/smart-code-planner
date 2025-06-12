#!/usr/bin/env python3

"""
Test script to identify import issues
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

try:
    print("Testing imports...")
    
    # Test core imports
    from src.core.models import SubTask
    print("✅ Core models imported successfully")
    
    from src.core.config import settings
    print("✅ Configuration imported successfully")
    
    from src.services.task_analyzer import TaskAnalyzer
    print("✅ Task analyzer imported successfully")
    
    from src.agent.graph import CoderAssistantGraph
    print("✅ Agent graph imported successfully")
    
    print("🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
