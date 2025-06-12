#!/usr/bin/env python3

"""
Integration test and demo script for the Smart Code Planner.
This script tests the core functionality without requiring API keys.
"""

import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch

# Add src to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.models import SubTask, TaskPriority, TaskComplexity, AgentState
from src.services.task_analyzer import TaskAnalyzer
from src.services.code_advisor import CodeAdvisor
from src.agent.graph import CoderAssistantGraph


def test_models():
    """Test the core models."""
    print("🧪 Testing core models...")

    # Test SubTask creation
    subtask = SubTask(
        id="test-1",
        title="Test Subtask",
        description="A test subtask for validation",
        priority=TaskPriority.MEDIUM,
        complexity=TaskComplexity.MODERATE,
        estimated_time="2 hours"
    )

    assert subtask.title == "Test Subtask"
    assert subtask.priority == TaskPriority.MEDIUM
    assert not subtask.is_complete

    # Test AgentState
    state = AgentState(
        current_task="Build a web app",
        subtasks=[subtask],
        max_depth=3
    )

    assert state.current_task == "Build a web app"
    assert len(state.subtasks) == 1
    assert not state.processing_complete

    print("✅ Models test passed!")


async def test_task_analyzer_mock():
    """Test task analyzer with mocked LLM."""
    print("🧪 Testing task analyzer...")

    mock_response = Mock()
    mock_response.content = json.dumps({
        "subtasks": [
            {
                "title": "Setup Development Environment",
                "description": "Configure development tools and environment",
                "priority": "high",
                "complexity": "simple",
                "estimated_time": "2 hours"
            },
            {
                "title": "Design Database Schema",
                "description": "Create database tables and relationships",
                "priority": "high",
                "complexity": "moderate",
                "estimated_time": "4 hours"
            }
        ]
    })

    with patch('src.services.task_analyzer.ChatOpenAI') as mock_llm:
        with patch('src.core.config.load_prompt') as mock_prompt:
            mock_prompt.return_value = "Test prompt"
            mock_instance = Mock()
            mock_instance.ainvoke = AsyncMock(return_value=mock_response)
            mock_llm.return_value = mock_instance

            analyzer = TaskAnalyzer()
            subtasks = await analyzer.decompose_task("Build a simple web application")

            assert len(subtasks) == 2
            assert subtasks[0].title == "Setup Development Environment"
            assert subtasks[1].complexity == TaskComplexity.MODERATE

            # Test complexity calculation
            complexity_score = analyzer.calculate_complexity_score(subtasks)
            assert 0.0 <= complexity_score <= 1.0

    print("✅ Task analyzer test passed!")


async def test_code_advisor_mock():
    """Test code advisor with mocked LLM."""
    print("🧪 Testing code advisor...")

    mock_response = Mock()
    mock_response.content = json.dumps({
        "file_structure": {
            "src/": "Main source code directory",
            "src/models/": "Data models"
        },
        "classes": [
            {
                "name": "User",
                "description": "User model class",
                "file_location": "src/models/user.py"
            }
        ],
        "design_patterns": ["MVC Pattern", "Repository Pattern"],
        "best_practices": ["Use type hints", "Write tests"]
    })

    with patch('src.services.code_advisor.ChatOpenAI') as mock_llm:
        with patch('src.core.config.load_prompt') as mock_prompt:
            mock_prompt.return_value = "Test prompt"
            mock_instance = Mock()
            mock_instance.ainvoke = AsyncMock(return_value=mock_response)
            mock_llm.return_value = mock_instance

            advisor = CodeAdvisor()
            subtasks = [
                SubTask(id="1", title="Setup", description="Setup project")
            ]

            advice = await advisor.generate_advice("Build web app", subtasks)

            assert "src/" in advice.file_structure
            assert len(advice.classes) == 1
            assert "MVC Pattern" in advice.design_patterns
            assert "Use type hints" in advice.best_practices

    print("✅ Code advisor test passed!")


def test_graph_structure():
    """Test graph structure and compilation."""
    print("🧪 Testing graph structure...")

    graph = CoderAssistantGraph()

    # Test graph compilation
    compiled_graph = graph.compile()
    assert compiled_graph is not None

    # Test visualization
    viz = graph.get_graph_visualization()
    assert "decompose_task" in viz
    assert "analyze_subtasks" in viz
    assert "generate_code_advice" in viz

    print("✅ Graph structure test passed!")


def test_configuration():
    """Test configuration loading."""
    print("🧪 Testing configuration...")

    # Set test environment variables
    os.environ.setdefault("OPENAI_API_KEY", "test-key")

    from src.core.config import settings

    # Test that settings loads without error
    assert hasattr(settings, 'model_name')
    assert hasattr(settings, 'temperature')
    assert hasattr(settings, 'max_analysis_depth')

    print("✅ Configuration test passed!")


def demo_functionality():
    """Demonstrate the key functionality."""
    print("🎯 Demo: Core functionality showcase")

    # Create sample data
    subtasks = [
        SubTask(
            id="1",
            title="Setup Development Environment",
            description="Install and configure development tools",
            priority=TaskPriority.HIGH,
            complexity=TaskComplexity.SIMPLE,
            estimated_time="2 hours"
        ),
        SubTask(
            id="2",
            title="Design System Architecture",
            description="Plan the overall system design and components",
            priority=TaskPriority.HIGH,
            complexity=TaskComplexity.COMPLEX,
            estimated_time="1 day",
            dependencies=["Setup Development Environment"]
        ),
        SubTask(
            id="3",
            title="Implement Core Features",
            description="Build the main application features",
            priority=TaskPriority.MEDIUM,
            complexity=TaskComplexity.VERY_COMPLEX,
            estimated_time="1 week",
            dependencies=["Design System Architecture"]
        )
    ]

    # Test complexity calculation
    analyzer = TaskAnalyzer()
    complexity_score = analyzer.calculate_complexity_score(subtasks)

    print(f"📊 Sample Analysis Results:")
    print(f"   Total Subtasks: {len(subtasks)}")
    print(f"   Complexity Score: {complexity_score:.2f}")
    print(f"   High Priority Tasks: {len([t for t in subtasks if t.priority == TaskPriority.HIGH])}")
    print(f"   Tasks with Dependencies: {len([t for t in subtasks if t.dependencies])}")

    # Display task breakdown
    print(f"\n📋 Task Breakdown:")
    for i, task in enumerate(subtasks, 1):
        print(f"   {i}. {task.title}")
        print(f"      Priority: {task.priority.value}")
        print(f"      Complexity: {task.complexity.value}")
        print(f"      Time: {task.estimated_time}")
        if task.dependencies:
            print(f"      Dependencies: {', '.join(task.dependencies)}")
        print()


async def main():
    """Run all tests and demo."""
    print("🚀 Smart Code Planner - Integration Test & Demo")
    print("=" * 60)

    try:
        # Run tests
        test_models()
        test_configuration()
        test_graph_structure()
        await test_task_analyzer_mock()
        await test_code_advisor_mock()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")

        # Run demo
        print("\n" + "=" * 60)
        demo_functionality()

        print("\n" + "=" * 60)
        print("🎉 Integration test and demo completed successfully!")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Run: poetry run streamlit run src/ui/streamlit_app.py")
        print("3. Or use: ./run.sh")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
