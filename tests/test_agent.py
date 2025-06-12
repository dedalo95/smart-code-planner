"""Tests for the LangGraph agent."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.agent.graph import CoderAssistantGraph
from src.core.models import AgentState


class TestCoderAssistantGraph:
    """Test CoderAssistantGraph."""
    
    @pytest.fixture
    def graph(self):
        """Create graph instance."""
        return CoderAssistantGraph()
    
    def test_graph_initialization(self, graph):
        """Test graph initialization."""
        assert graph.graph is not None
        assert graph.nodes is not None
    
    def test_graph_compilation(self, graph):
        """Test graph compilation."""
        compiled_graph = graph.compile()
        assert compiled_graph is not None
    
    def test_get_graph_visualization(self, graph):
        """Test graph visualization."""
        viz = graph.get_graph_visualization()
        assert "Coder Assistant LangGraph Workflow" in viz
        assert "decompose_task" in viz
        assert "analyze_subtasks" in viz
    
    @pytest.mark.asyncio
    async def test_run_graph_success(self, graph):
        """Test successful graph execution."""
        with patch.object(graph, 'compile') as mock_compile:
            # Mock the compiled app
            mock_app = Mock()
            mock_final_state = AgentState(
                current_task="test task",
                processing_complete=True
            )
            mock_app.ainvoke = AsyncMock(return_value=mock_final_state)
            mock_compile.return_value = mock_app
            
            # Test execution
            result = await graph.run("Build a web app")
            
            assert result.current_task == "test task"
            assert result.processing_complete is True
            assert result.error_message is None
    
    @pytest.mark.asyncio
    async def test_run_graph_error(self, graph):
        """Test graph execution with error."""
        with patch.object(graph, 'compile') as mock_compile:
            # Mock compilation error
            mock_compile.side_effect = Exception("Compilation failed")
            
            # Test execution
            result = await graph.run("Build a web app")
            
            assert result.error_message is not None
            assert "Graph execution error" in result.error_message
            assert result.processing_complete is True
