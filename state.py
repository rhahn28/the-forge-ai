# state.py
from typing import TypedDict, List, Optional, Any, Dict

class ForgeState(TypedDict, total=False):
    """
    Enhanced state with recursion protection and progress tracking
    """
    # Core task info
    task: str
    plan: Optional[List[Dict[str, Any]]]
    current_step: int
    
    # Error handling and progress tracking
    error: Optional[str]
    retry_count: int
    debug_cycle: int
    error_history: List[str]
    
    # Workflow control
    human_approved: bool
    skip_review: bool
    auto_approve: bool
    force_failure: bool
    progress_check: Optional[str]
    
    # Final status
    final_status: Optional[str]
    failure_reason: Optional[str]
    
    # Additional metadata
    result: Optional[str]
    
    def get_progress_summary(self) -> str:
        """Get a human-readable progress summary"""
        retry = self.get("retry_count", 0)
        debug = self.get("debug_cycle", 0)
        total_errors = len(self.get("error_history", []))
        
        return f"Iteration {retry + 1}, Debug Cycle {debug + 1}, Total Errors: {total_errors}"
    
    def is_stuck_in_loop(self, window: int = 3) -> bool:
        """Check if we're repeating the same errors"""
        history = self.get("error_history", [])
        if len(history) < window:
            return False
        
        recent = history[-window:]
        return len(set(recent)) <= 1  # Same error(s) repeating
    
    def should_give_up(self, max_retries: int = 3, max_total_errors: int = 10) -> bool:
        """Determine if we should stop trying"""
        retry_count = self.get("retry_count", 0)
        total_errors = len(self.get("error_history", []))
        
        return (retry_count >= max_retries or 
                total_errors >= max_total_errors or
                self.is_stuck_in_loop())