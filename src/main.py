from models.state import LeadState
from flow.graph import build_graph
from config import MESSAGES


def run_cli():
    """Run the lead qualification workflow via CLI."""
    graph = build_graph()
    
    initial_state: LeadState = {
        "is_corporate": None,
        "budget": None,
        "name": None,
        "contact": None,
        "qualified": None
    }
    
    final_state = graph.invoke(initial_state)
    print(MESSAGES["conversation_end"])
    print(f"Estado final: {final_state}")


if __name__ == "__main__":
    run_cli()
