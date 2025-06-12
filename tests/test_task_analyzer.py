"""Tests for task analyzer service."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.task_analyzer import TaskAnalyzer
from src.core.models import SubTask, TaskPriority, TaskComplexity


class TestTaskAnalyzer:
    """Test TaskAnalyzer service."""
    
    @pytest.fixture
    def analyzer(self, mock_openai):
        """Create TaskAnalyzer instance with mocked dependencies."""
        with patch('src.services.task_analyzer.load_prompt') as mock_prompt:
            mock_prompt.return_value = "Test prompt"
            return TaskAnalyzer()
    
    @pytest.mark.asyncio
    async def test_decompose_task_success(self, analyzer, mock_openai):
        """Test successful task decomposition."""
        # Mock response
        mock_response = Mock()
        mock_response.content = '''
        {
            "subtasks": [
                {
                    "title": "Setup Environment",
                    "description": "Setup development environment",
                    "priority": "high",
                    "complexity": "simple",
                    "estimated_time": "2 hours"
                }
            ]
        }
        '''
        mock_openai.ainvoke = AsyncMock(return_value=mock_response)
        
        # Test decomposition
        subtasks = await analyzer.decompose_task("Build a web app")
        
        assert len(subtasks) == 1
        assert subtasks[0].title == "Setup Environment"
        assert subtasks[0].priority == TaskPriority.HIGH
        assert subtasks[0].complexity == TaskComplexity.SIMPLE
    
    @pytest.mark.asyncio
    async def test_analyze_subtask_complexity_simple(self, analyzer, mock_openai):
        """Test analyzing a simple subtask."""
        subtask = SubTask(
            id="test-1",
            title="Simple Task",
            description="A simple task",
            complexity=TaskComplexity.SIMPLE
        )
        
        result = await analyzer.analyze_subtask_complexity(subtask)
        
        # Simple tasks should not be further decomposed
        assert result.complexity == TaskComplexity.SIMPLE
        assert len(result.sub_subtasks) == 0
    
    @pytest.mark.asyncio
    async def test_analyze_subtask_complexity_complex(self, analyzer, mock_openai):
        """Test analyzing a complex subtask."""
        # Mock response for complex subtask analysis
        mock_response = Mock()
        mock_response.content = '''
        {
            "needs_decomposition": true,
            "subtasks": [
                {
                    "title": "Sub Task 1",
                    "description": "First sub task",
                    "priority": "medium",
                    "complexity": "simple"
                }
            ]
        }
        '''
        mock_openai.ainvoke = AsyncMock(return_value=mock_response)
        
        subtask = SubTask(
            id="test-1",
            title="Complex Task",
            description="A complex task",
            complexity=TaskComplexity.COMPLEX
        )
        
        result = await analyzer.analyze_subtask_complexity(subtask)
        
        # Complex task should be decomposed
        assert len(result.sub_subtasks) == 1
        assert result.sub_subtasks[0].title == "Sub Task 1"
    
    def test_calculate_complexity_score(self, analyzer):
        """Test complexity score calculation."""
        subtasks = [
            SubTask(
                id="1",
                title="Simple Task",
                description="Simple",
                complexity=TaskComplexity.SIMPLE
            ),
            SubTask(
                id="2", 
                title="Complex Task",
                description="Complex",
                complexity=TaskComplexity.COMPLEX
            )
        ]
        
        score = analyzer.calculate_complexity_score(subtasks)
        
        # Score should be between simple (0.2) and complex (0.7)
        assert 0.2 < score < 0.7
    
    def test_parse_subtasks_response_json(self, analyzer):
        """Test parsing JSON response."""
        response = '''
        {
            "subtasks": [
                {
                    "title": "Test Task",
                    "description": "A test task",
                    "priority": "medium",
                    "complexity": "moderate"
                }
            ]
        }
        '''
        
        result = analyzer._parse_subtasks_response(response)
        
        assert len(result) == 1
        assert result[0]["title"] == "Test Task"
        assert result[0]["priority"] == "medium"
    
    def test_parse_subtasks_response_fallback(self, analyzer):
        """Test fallback parsing for non-JSON response."""
        response = '''
        Title: Test Task
        Description: A test task
        Priority: high
        Complexity: simple
        '''
        
        result = analyzer._parse_subtasks_response(response)
        
        assert len(result) == 1
        assert result[0]["title"] == "Test Task"
        assert result[0]["priority"] == "high"
