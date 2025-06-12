"""Code organization advisor service."""

import json
from typing import Dict, Any, List
from langchain.schema import SystemMessage, HumanMessage

from ..core.models import CodeOrganizationAdvice, SubTask
from ..core.config import settings, load_prompt
from .llm_service import LLMService


class CodeAdvisor:
    """Service for providing code organization advice."""
    
    def __init__(self):
        """Initialize the code advisor."""
        self.llm = LLMService.get_llm()
        
        # Load prompt
        self.organization_prompt = load_prompt("code_organization")
    
    async def generate_advice(
        self, 
        original_task: str, 
        subtasks: List[SubTask]
    ) -> CodeOrganizationAdvice:
        """Generate code organization advice based on task and subtasks."""
        try:
            # Prepare subtasks summary
            subtasks_summary = self._prepare_subtasks_summary(subtasks)
            
            # Create the prompt
            messages = [
                SystemMessage(content=self.organization_prompt),
                HumanMessage(content=f"""
                Original Task: {original_task}
                
                Subtasks Summary:
                {subtasks_summary}
                
                Please provide comprehensive code organization advice.
                """)
            ]
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            
            # Parse the response
            advice_data = self._parse_advice_response(response.content)
            
            # Create CodeOrganizationAdvice object
            advice = CodeOrganizationAdvice(
                file_structure=advice_data.get("file_structure", {}),
                classes=advice_data.get("classes", []),
                functions=advice_data.get("functions", []),
                modules=advice_data.get("modules", []),
                design_patterns=advice_data.get("design_patterns", []),
                best_practices=advice_data.get("best_practices", [])
            )
            
            return advice
            
        except Exception as e:
            raise Exception(f"Error generating code organization advice: {str(e)}")
    
    def _prepare_subtasks_summary(self, subtasks: List[SubTask]) -> str:
        """Prepare a formatted summary of subtasks."""
        summary = []
        
        for i, subtask in enumerate(subtasks, 1):
            summary.append(f"{i}. {subtask.title}")
            summary.append(f"   Description: {subtask.description}")
            summary.append(f"   Complexity: {subtask.complexity}")
            summary.append(f"   Priority: {subtask.priority}")
            
            if subtask.sub_subtasks:
                summary.append("   Sub-subtasks:")
                for j, sub_subtask in enumerate(subtask.sub_subtasks, 1):
                    summary.append(f"   - {j}. {sub_subtask.title}")
                    summary.append(f"     Description: {sub_subtask.description}")
            
            summary.append("")  # Empty line for separation
        
        return "\n".join(summary)
    
    def _parse_advice_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response for code organization advice."""
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                # Assume the entire response is JSON
                json_str = response.strip()
            
            return json.loads(json_str)
            
        except json.JSONDecodeError:
            # Fallback: parse as structured text
            return self._parse_text_advice(response)
    
    def _parse_text_advice(self, response: str) -> Dict[str, Any]:
        """Fallback parser for text-based advice."""
        advice = {
            "file_structure": {},
            "classes": [],
            "functions": [],
            "modules": [],
            "design_patterns": [],
            "best_practices": []
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "file structure" in line.lower():
                current_section = "file_structure"
            elif "classes" in line.lower():
                current_section = "classes"
            elif "functions" in line.lower():
                current_section = "functions"
            elif "modules" in line.lower():
                current_section = "modules"
            elif "design patterns" in line.lower():
                current_section = "design_patterns"
            elif "best practices" in line.lower():
                current_section = "best_practices"
            elif line.startswith('- ') or line.startswith('* '):
                # List item
                item = line[2:].strip()
                if current_section in ["classes", "functions", "modules"]:
                    advice[current_section].append({"name": item, "description": ""})
                elif current_section in ["design_patterns", "best_practices"]:
                    advice[current_section].append(item)
            elif ':' in line and current_section == "file_structure":
                # File structure entry
                parts = line.split(':', 1)
                if len(parts) == 2:
                    advice["file_structure"][parts[0].strip()] = parts[1].strip()
        
        return advice
    
    def generate_recommendations(
        self, 
        subtasks: List[SubTask], 
        complexity_score: float
    ) -> List[str]:
        """Generate general recommendations based on analysis."""
        recommendations = []
        
        # Complexity-based recommendations
        if complexity_score > 0.8:
            recommendations.append(
                "Consider breaking down the most complex subtasks further before implementation"
            )
            recommendations.append(
                "Use a phased approach - implement core functionality first, then add features"
            )
            recommendations.append(
                "Implement comprehensive testing from the beginning"
            )
        elif complexity_score > 0.6:
            recommendations.append(
                "Plan the architecture carefully before starting implementation"
            )
            recommendations.append(
                "Consider using established design patterns for complex components"
            )
        else:
            recommendations.append(
                "This project has moderate complexity - focus on clean, maintainable code"
            )
        
        # Task-specific recommendations
        high_priority_tasks = [t for t in subtasks if t.priority == "high"]
        if high_priority_tasks:
            recommendations.append(
                f"Prioritize these high-priority tasks: {', '.join([t.title for t in high_priority_tasks[:3]])}"
            )
        
        # Dependency recommendations
        dependent_tasks = [t for t in subtasks if t.dependencies]
        if dependent_tasks:
            recommendations.append(
                "Pay attention to task dependencies - some tasks must be completed before others"
            )
        
        # Sub-subtask recommendations
        nested_tasks = [t for t in subtasks if t.sub_subtasks]
        if nested_tasks:
            recommendations.append(
                "Some tasks have been further decomposed - review the sub-subtasks for detailed implementation steps"
            )
        
        return recommendations
