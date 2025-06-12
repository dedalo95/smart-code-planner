"""Main package initialization."""

__version__ = "0.1.0"
__author__ = "Federico Antosiano"
__email__ = "federico.antosiano@gmail.com"

from .core import *
from .services import *
from .agent import *

__all__ = [
    "TaskPriority",
    "TaskComplexity",
    "SubTask", 
    "CodeOrganizationAdvice",
    "TaskAnalysisResult",
    "AgentState",
    "settings",
    "load_prompt",
    "TaskAnalyzer",
    "CodeAdvisor",
    "CoderAssistantGraph",
    "CoderAssistantNodes",
    "StateManager",
]
