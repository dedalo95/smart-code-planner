"""LangGraph workflow definition for the coder assistant."""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from ..core.models import AgentState
from .nodes import CoderAssistantNodes


class CoderAssistantGraph:
    """LangGraph workflow for the coder assistant."""
    
    def __init__(self):
        """Initialize the graph."""
        self.nodes = CoderAssistantNodes()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("decompose_task", self.nodes.decompose_task_node)
        workflow.add_node("analyze_subtasks", self.nodes.analyze_subtasks_node)
        workflow.add_node("generate_code_advice", self.nodes.generate_code_advice_node)
        workflow.add_node("finalize_result", self.nodes.finalize_result_node)
        
        # Set entry point
        workflow.set_entry_point("decompose_task")
        
        # Add edges
        workflow.add_edge("decompose_task", "analyze_subtasks")
        
        # Add conditional edges from analyze_subtasks
        workflow.add_conditional_edges(
            "analyze_subtasks",
            self.nodes.should_continue_analysis,
            {
                "continue_analysis": "analyze_subtasks",
                "generate_advice": "generate_code_advice",
                "complete": END,
                "error": END,
            }
        )
        
        # Add edges from generate_code_advice
        workflow.add_edge("generate_code_advice", "finalize_result")
        workflow.add_edge("finalize_result", END)
        
        return workflow
    
    def compile(self):
        """Compile the graph for execution."""
        return self.graph.compile()
    
    async def run(self, task: str, max_depth: int = 3) -> AgentState:
        """Run the complete workflow."""
        try:
            # Initialize state
            initial_state = AgentState(
                current_task=task,
                max_depth=max_depth,
            )
            
            # Compile and run the graph
            app = self.compile()
            final_state_dict = await app.ainvoke(initial_state)
            
            # Convert the result back to AgentState
            # LangGraph returns a dict-like object, so we need to extract the values
            return AgentState(
                current_task=final_state_dict.get("current_task", task),
                subtasks=final_state_dict.get("subtasks", []),
                analysis_depth=final_state_dict.get("analysis_depth", 0),
                max_depth=final_state_dict.get("max_depth", max_depth),
                code_advice=final_state_dict.get("code_advice"),
                final_result=final_state_dict.get("final_result"),
                error_message=final_state_dict.get("error_message"),
                processing_complete=final_state_dict.get("processing_complete", False),
            )
            
        except Exception as e:
            # Return error state
            return AgentState(
                current_task=task,
                max_depth=max_depth,
                error_message=f"Graph execution error: {str(e)}",
                processing_complete=True,
            )
    
    def get_graph_visualization(self) -> str:
        """Get a text representation of the graph structure."""
        return """
╔═══════════════════════════════════════════════════════════════════════╗
║                    Coder Assistant LangGraph Workflow                ║
╚═══════════════════════════════════════════════════════════════════════╝

    [START] 
        ↓
┌─────────────────┐
│ decompose_task  │ ← Breaks down the main task into subtasks
└─────────────────┘
        ↓
┌─────────────────┐
│ analyze_subtasks│ ← Analyzes subtasks for complexity and decomposition
└─────────────────┘
        ↓ (conditional routing)
        ├── → [analyze_subtasks] (if more analysis needed)
        ├── → [generate_code_advice] (if analysis complete)
        └── → [END] (if complete or error)

┌─────────────────────┐
│ generate_code_advice│ ← Generates code organization recommendations  
└─────────────────────┘
        ↓
┌─────────────────┐
│ finalize_result │ ← Creates the final analysis result
└─────────────────┘
        ↓
    [END]

═══════════════════════════════════════════════════════════════════════
Conditional Logic:
• Continue analysis if subtasks are complex and haven't reached max depth
• Generate advice when analysis is sufficient  
• End on error or completion
═══════════════════════════════════════════════════════════════════════
        """
    
    def print_graph_visualization(self):
        """Print the graph visualization to console."""
        print(self.get_graph_visualization())
