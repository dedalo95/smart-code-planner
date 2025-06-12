"""State management for the LangGraph agent."""

from typing import Optional
from ..core.models import AgentState


class StateManager:
    """Manages the state throughout the LangGraph workflow."""
    
    def __init__(self):
        """Initialize the state manager."""
        self._state: Optional[AgentState] = None
    
    def initialize_state(self, task: str, max_depth: int = 3) -> AgentState:
        """Initialize a new agent state."""
        self._state = AgentState(
            current_task=task,
            max_depth=max_depth,
        )
        return self._state
    
    def get_state(self) -> Optional[AgentState]:
        """Get the current state."""
        return self._state
    
    def update_state(self, **kwargs) -> AgentState:
        """Update the current state with new values."""
        if not self._state:
            raise ValueError("State not initialized")
        
        for key, value in kwargs.items():
            if hasattr(self._state, key):
                setattr(self._state, key, value)
        
        return self._state
    
    def reset_state(self):
        """Reset the state."""
        self._state = None
    
    def is_processing_complete(self) -> bool:
        """Check if processing is complete."""
        return self._state is not None and self._state.processing_complete
    
    def has_error(self) -> bool:
        """Check if there's an error in the current state."""
        return self._state is not None and self._state.error_message is not None
