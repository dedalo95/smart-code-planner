"""Test configuration."""

import pytest
import os
from unittest.mock import Mock, patch

# Set test environment variables
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["LANGCHAIN_API_KEY"] = "test-key"

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch('langchain_openai.ChatOpenAI') as mock:
        mock_instance = Mock()
        mock_instance.ainvoke.return_value = Mock(content='{"subtasks": []}')
        mock.return_value = mock_instance
        yield mock_instance
