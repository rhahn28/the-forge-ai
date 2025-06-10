# state.py
from typing import TypedDict, Optional

class ForgeState(TypedDict):
    """
    This is the central memory of our system.
    Agents read from and write to this dictionary.
    """
    # The initial instruction from the user. For Phase 1, this will
    # simply be the name of the file we want the agent to read.
    task: str

    # A field to store the successful result of an agent's operation.
    # For example, "File 'plan.txt' written successfully."
    result: Optional[str]

    # A field to store any error message if an agent's operation fails.
    # This is crucial for debugging and for conditional routing in later phases.
    error: Optional[str]