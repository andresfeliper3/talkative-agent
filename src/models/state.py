from typing import TypedDict, Optional


class LeadState(TypedDict):
    """State for lead qualification workflow."""
    is_corporate: Optional[bool]
    event_type: Optional[str]
    budget: Optional[float]
    name: Optional[str]
    contact: Optional[str]
    contact_type: Optional[str]  
    qualified: Optional[bool]

