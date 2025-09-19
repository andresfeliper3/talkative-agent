from models.state import LeadState
from flow.graph import build_graph


def run_cli():
    """Run the lead qualification workflow via CLI."""
    graph = build_graph()
    
    initial_state: LeadState = {
        "is_corporate": None,
        "event_type": None,
        "budget": None,
        "name": None,
        "contact": None,
        "contact_type": None,
        "qualified": None
    }
    
    final_state = graph.invoke(initial_state)


if __name__ == "__main__":
    run_cli()