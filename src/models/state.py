from typing import TypedDict, Optional


class LeadState(TypedDict):
    """State for lead qualification workflow."""
    is_corporate: Optional[bool]
    budget: Optional[float]
    name: Optional[str]
    contact: Optional[str]
    qualified: Optional[bool]

