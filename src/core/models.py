"""Core models for the coder assistant application."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskComplexity(str, Enum):
    """Task complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class SubTask(BaseModel):
    """Represents a subtask within a larger task."""
    
    id: str = Field(..., description="Unique identifier for the subtask")
    title: str = Field(..., description="Brief title of the subtask")
    description: str = Field(..., description="Detailed description of the subtask")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Priority level")
    complexity: TaskComplexity = Field(default=TaskComplexity.MODERATE, description="Complexity level")
    estimated_time: Optional[str] = Field(None, description="Estimated time to complete")
    dependencies: List[str] = Field(default_factory=list, description="List of subtask IDs this depends on")
    sub_subtasks: List['SubTask'] = Field(default_factory=list, description="Nested subtasks")
    is_complete: bool = Field(default=False, description="Whether the subtask is complete")


class CodeOrganizationAdvice(BaseModel):
    """Represents advice for organizing code."""
    
    file_structure: Dict[str, str] = Field(..., description="Recommended file structure")
    classes: List[Dict[str, Any]] = Field(default_factory=list, description="Recommended classes")
    functions: List[Dict[str, Any]] = Field(default_factory=list, description="Recommended functions")
    modules: List[Dict[str, Any]] = Field(default_factory=list, description="Recommended modules")
    design_patterns: List[str] = Field(default_factory=list, description="Suggested design patterns")
    best_practices: List[str] = Field(default_factory=list, description="Best practices to follow")


class TaskAnalysisResult(BaseModel):
    """Complete result of task analysis."""
    
    original_task: str = Field(..., description="The original task description")
    main_subtasks: List[SubTask] = Field(..., description="Primary subtasks")
    code_organization: CodeOrganizationAdvice = Field(..., description="Code organization advice")
    total_estimated_time: Optional[str] = Field(None, description="Total estimated time")
    complexity_score: float = Field(..., description="Overall complexity score (0-1)")
    recommendations: List[str] = Field(default_factory=list, description="General recommendations")


class AgentState(BaseModel):
    """State management for the LangGraph agent."""
    
    current_task: str = Field(..., description="Current task being processed")
    subtasks: List[SubTask] = Field(default_factory=list, description="Generated subtasks")
    analysis_depth: int = Field(default=0, description="Current depth of analysis")
    max_depth: int = Field(default=3, description="Maximum analysis depth")
    code_advice: Optional[CodeOrganizationAdvice] = Field(None, description="Code organization advice")
    final_result: Optional[TaskAnalysisResult] = Field(None, description="Final analysis result")
    error_message: Optional[str] = Field(None, description="Error message if processing fails")
    processing_complete: bool = Field(default=False, description="Whether processing is complete")


# Update forward references
SubTask.model_rebuild()
