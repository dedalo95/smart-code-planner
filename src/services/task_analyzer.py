"""Task analysis service for breaking down complex tasks."""

import json
import uuid
from typing import List, Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from ..core.models import SubTask, TaskPriority, TaskComplexity
from ..core.config import settings, load_prompt
from .llm_service import LLMService


class TaskAnalyzer:
    """Service for analyzing and decomposing tasks."""
    
    def __init__(self):
        """Initialize the task analyzer."""
        self.llm = LLMService.get_llm()
        
        # Load prompts
        self.decomposition_prompt = load_prompt("task_decomposition")
        self.subtask_analysis_prompt = load_prompt("subtask_analysis")
    
    async def decompose_task(self, task_description: str) -> List[SubTask]:
        """Decompose a task into subtasks."""
        try:
            # Create the prompt
            messages = [
                SystemMessage(content=self.decomposition_prompt),
                HumanMessage(content=f"Task to decompose: {task_description}")
            ]
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            
            # Parse the response
            subtasks_data = self._parse_subtasks_response(response.content)
            
            # Convert to SubTask objects
            subtasks = []
            for data in subtasks_data:
                subtask = SubTask(
                    id=str(uuid.uuid4()),
                    title=data.get("title", ""),
                    description=data.get("description", ""),
                    priority=TaskPriority(data.get("priority", "medium")),
                    complexity=TaskComplexity(data.get("complexity", "moderate")),
                    estimated_time=data.get("estimated_time"),
                    dependencies=data.get("dependencies", []),
                )
                subtasks.append(subtask)
            
            return subtasks
            
        except Exception as e:
            raise Exception(f"Error decomposing task: {str(e)}")
    
    async def analyze_subtask_complexity(self, subtask: SubTask) -> SubTask:
        """Analyze if a subtask needs further decomposition."""
        try:
            # Check if subtask is complex enough to warrant further decomposition
            if subtask.complexity in [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]:
                return subtask
            
            # Create the prompt for subtask analysis
            messages = [
                SystemMessage(content=self.subtask_analysis_prompt),
                HumanMessage(content=f"""
                Subtask to analyze:
                Title: {subtask.title}
                Description: {subtask.description}
                Current Complexity: {subtask.complexity}
                """)
            ]
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            
            # Parse the response to see if further decomposition is needed
            analysis_result = self._parse_subtask_analysis_response(response.content)
            
            if analysis_result.get("needs_decomposition", False):
                # Decompose further
                sub_subtasks_data = analysis_result.get("subtasks", [])
                sub_subtasks = []
                
                for data in sub_subtasks_data:
                    sub_subtask = SubTask(
                        id=str(uuid.uuid4()),
                        title=data.get("title", ""),
                        description=data.get("description", ""),
                        priority=TaskPriority(data.get("priority", "medium")),
                        complexity=TaskComplexity(data.get("complexity", "simple")),
                        estimated_time=data.get("estimated_time"),
                        dependencies=data.get("dependencies", []),
                    )
                    sub_subtasks.append(sub_subtask)
                
                subtask.sub_subtasks = sub_subtasks
            
            return subtask
            
        except Exception as e:
            raise Exception(f"Error analyzing subtask complexity: {str(e)}")
    
    def calculate_complexity_score(self, subtasks: List[SubTask]) -> float:
        """Calculate overall complexity score for a list of subtasks."""
        if not subtasks:
            return 0.0
        
        complexity_values = {
            TaskComplexity.SIMPLE: 0.2,
            TaskComplexity.MODERATE: 0.4,
            TaskComplexity.COMPLEX: 0.7,
            TaskComplexity.VERY_COMPLEX: 1.0,
        }
        
        total_score = 0.0
        total_weight = 0
        
        for subtask in subtasks:
            score = complexity_values.get(subtask.complexity, 0.4)
            weight = 1
            
            # Consider sub-subtasks
            if subtask.sub_subtasks:
                sub_score = self.calculate_complexity_score(subtask.sub_subtasks)
                score = (score + sub_score) / 2
                weight += len(subtask.sub_subtasks)
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _parse_subtasks_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse the LLM response for subtasks."""
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                # Assume the entire response is JSON
                json_str = response.strip()
            
            data = json.loads(json_str)
            return data.get("subtasks", [])
            
        except json.JSONDecodeError:
            # Fallback: parse as plain text
            return self._parse_text_response(response)
    
    def _parse_subtask_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response for subtask analysis."""
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
            
        except json.JSONDecodeError:
            # Fallback: assume no decomposition needed
            return {"needs_decomposition": False, "subtasks": []}
    
    def _parse_text_response(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser for plain text responses."""
        # Simple text parsing logic
        # This is a basic implementation - you might want to enhance this
        lines = response.split('\n')
        subtasks = []
        
        current_subtask = {}
        for line in lines:
            line = line.strip()
            if line.startswith('Title:') or line.startswith('- '):
                if current_subtask:
                    subtasks.append(current_subtask)
                current_subtask = {
                    'title': line.replace('Title:', '').replace('- ', '').strip(),
                    'description': '',
                    'priority': 'medium',
                    'complexity': 'moderate'
                }
            elif line.startswith('Description:'):
                current_subtask['description'] = line.replace('Description:', '').strip()
            elif line.startswith('Priority:'):
                current_subtask['priority'] = line.replace('Priority:', '').strip().lower()
            elif line.startswith('Complexity:'):
                current_subtask['complexity'] = line.replace('Complexity:', '').strip().lower()
        
        if current_subtask:
            subtasks.append(current_subtask)
        
        return subtasks
