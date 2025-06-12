"""Tests for core models."""

import pytest
from src.core.models import (
    SubTask, 
    TaskPriority, 
    TaskComplexity,
    CodeOrganizationAdvice,
    TaskAnalysisResult,
    AgentState
)


class TestSubTask:
    """Test SubTask model."""
    
    def test_subtask_creation(self):
        """Test creating a SubTask."""
        subtask = SubTask(
            id="test-1",
            title="Test Task",
            description="A test task",
            priority=TaskPriority.HIGH,
            complexity=TaskComplexity.MODERATE
        )
        
        assert subtask.id == "test-1"
        assert subtask.title == "Test Task"
        assert subtask.priority == TaskPriority.HIGH
        assert subtask.complexity == TaskComplexity.MODERATE
        assert subtask.is_complete is False
    
    def test_subtask_with_nested_subtasks(self):
        """Test SubTask with nested sub-subtasks."""
        sub_subtask = SubTask(
            id="sub-1",
            title="Sub Task",
            description="A sub task"
        )
        
        main_subtask = SubTask(
            id="main-1",
            title="Main Task", 
            description="A main task",
            sub_subtasks=[sub_subtask]
        )
        
        assert len(main_subtask.sub_subtasks) == 1
        assert main_subtask.sub_subtasks[0].title == "Sub Task"


class TestCodeOrganizationAdvice:
    """Test CodeOrganizationAdvice model."""
    
    def test_code_advice_creation(self):
        """Test creating CodeOrganizationAdvice."""
        advice = CodeOrganizationAdvice(
            file_structure={"src/": "Source code"},
            classes=[{"name": "TestClass", "description": "Test class"}],
            design_patterns=["Factory Pattern"],
            best_practices=["Use type hints"]
        )
        
        assert advice.file_structure["src/"] == "Source code"
        assert len(advice.classes) == 1
        assert "Factory Pattern" in advice.design_patterns
        assert "Use type hints" in advice.best_practices


class TestTaskAnalysisResult:
    """Test TaskAnalysisResult model."""
    
    def test_analysis_result_creation(self):
        """Test creating TaskAnalysisResult."""
        subtask = SubTask(
            id="test-1",
            title="Test Task",
            description="A test task"
        )
        
        advice = CodeOrganizationAdvice(
            file_structure={"src/": "Source code"}
        )
        
        result = TaskAnalysisResult(
            original_task="Build a web app",
            main_subtasks=[subtask],
            code_organization=advice,
            complexity_score=0.5
        )
        
        assert result.original_task == "Build a web app"
        assert len(result.main_subtasks) == 1
        assert result.complexity_score == 0.5


class TestAgentState:
    """Test AgentState model."""
    
    def test_agent_state_creation(self):
        """Test creating AgentState."""
        state = AgentState(
            current_task="Test task",
            max_depth=3
        )
        
        assert state.current_task == "Test task"
        assert state.max_depth == 3
        assert state.analysis_depth == 0
        assert state.processing_complete is False
        assert state.error_message is None
