"""LangGraph nodes for the coder assistant agent."""

import asyncio
from typing import Dict, Any, List
from langgraph.graph import StateGraph

from ..core.models import AgentState, TaskAnalysisResult
from ..services.task_analyzer import TaskAnalyzer
from ..services.code_advisor import CodeAdvisor


class CoderAssistantNodes:
    """Collection of nodes for the coder assistant LangGraph."""
    
    def __init__(self):
        """Initialize the nodes."""
        self.task_analyzer = TaskAnalyzer()
        self.code_advisor = CodeAdvisor()
    
    async def decompose_task_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to decompose the main task into subtasks."""
        try:
            # Decompose the main task
            subtasks = await self.task_analyzer.decompose_task(state.current_task)
            
            return {
                "subtasks": subtasks,
                "analysis_depth": state.analysis_depth + 1,
                "error_message": None,
            }
            
        except Exception as e:
            return {
                "error_message": f"Error in task decomposition: {str(e)}",
                "processing_complete": True,
            }
    
    async def analyze_subtasks_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to analyze subtasks for further decomposition."""
        try:
            if not state.subtasks:
                return {"error_message": "No subtasks to analyze"}
            
            # Check if we've reached maximum depth
            if state.analysis_depth >= state.max_depth:
                return {"analysis_depth": state.analysis_depth}
            
            # Analyze each subtask for complexity
            analyzed_subtasks = []
            for subtask in state.subtasks:
                analyzed_subtask = await self.task_analyzer.analyze_subtask_complexity(subtask)
                analyzed_subtasks.append(analyzed_subtask)
            
            return {
                "subtasks": analyzed_subtasks,
                "analysis_depth": state.analysis_depth + 1,
                "error_message": None,
            }
            
        except Exception as e:
            return {
                "error_message": f"Error in subtask analysis: {str(e)}",
                "processing_complete": True,
            }
    
    async def generate_code_advice_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to generate code organization advice."""
        try:
            if not state.subtasks:
                return {"error_message": "No subtasks available for code advice"}
            
            # Generate code organization advice
            code_advice = await self.code_advisor.generate_advice(
                state.current_task, 
                state.subtasks
            )
            
            return {
                "code_advice": code_advice,
                "error_message": None,
            }
            
        except Exception as e:
            return {
                "error_message": f"Error generating code advice: {str(e)}",
                "processing_complete": True,
            }
    
    async def finalize_result_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to finalize the analysis result."""
        try:
            if not state.subtasks or not state.code_advice:
                return {"error_message": "Missing required data for finalization"}
            
            # Calculate complexity score
            complexity_score = self.task_analyzer.calculate_complexity_score(state.subtasks)
            
            # Generate recommendations
            recommendations = self.code_advisor.generate_recommendations(
                state.subtasks, 
                complexity_score
            )
            
            # Calculate total estimated time
            total_time = self._calculate_total_time(state.subtasks)
            
            # Create final result
            final_result = TaskAnalysisResult(
                original_task=state.current_task,
                main_subtasks=state.subtasks,
                code_organization=state.code_advice,
                total_estimated_time=total_time,
                complexity_score=complexity_score,
                recommendations=recommendations,
            )
            
            return {
                "final_result": final_result,
                "processing_complete": True,
                "error_message": None,
            }
            
        except Exception as e:
            return {
                "error_message": f"Error finalizing result: {str(e)}",
                "processing_complete": True,
            }
    
    def should_continue_analysis(self, state: AgentState) -> str:
        """Conditional node to determine if analysis should continue."""
        # Check for errors
        if state.error_message:
            return "error"
        
        # Check if processing is complete
        if state.processing_complete:
            return "complete"
        
        # Check if we have subtasks and haven't reached max depth
        if state.subtasks and state.analysis_depth < state.max_depth:
            # Check if any subtasks need further analysis
            needs_analysis = any(
                subtask.complexity.value in ["complex", "very_complex"] and not subtask.sub_subtasks
                for subtask in state.subtasks
            )
            if needs_analysis:
                return "continue_analysis"
        
        return "generate_advice"
    
    def _calculate_total_time(self, subtasks: List) -> str:
        """Calculate total estimated time for all subtasks."""
        time_mapping = {
            "minutes": 1,
            "hour": 60,
            "hours": 60,
            "day": 480,  # 8 hours
            "days": 480,
            "week": 2400,  # 5 days * 8 hours
            "weeks": 2400,
        }
        
        total_minutes = 0
        has_estimates = False
        
        def extract_time_from_subtasks(subtask_list):
            nonlocal total_minutes, has_estimates
            
            for subtask in subtask_list:
                if subtask.estimated_time:
                    has_estimates = True
                    # Simple parsing of time estimates
                    time_str = subtask.estimated_time.lower()
                    for unit, multiplier in time_mapping.items():
                        if unit in time_str:
                            try:
                                # Extract number before the unit
                                parts = time_str.split(unit)[0].strip().split()
                                if parts:
                                    number = float(parts[-1])
                                    total_minutes += number * multiplier
                                    break
                            except (ValueError, IndexError):
                                continue
                
                # Process sub-subtasks recursively
                if subtask.sub_subtasks:
                    extract_time_from_subtasks(subtask.sub_subtasks)
        
        extract_time_from_subtasks(subtasks)
        
        if not has_estimates:
            return "Not estimated"
        
        # Convert back to human-readable format
        if total_minutes < 60:
            return f"{int(total_minutes)} minutes"
        elif total_minutes < 480:
            hours = total_minutes / 60
            return f"{hours:.1f} hours"
        elif total_minutes < 2400:
            days = total_minutes / 480
            return f"{days:.1f} days"
        else:
            weeks = total_minutes / 2400
            return f"{weeks:.1f} weeks"
