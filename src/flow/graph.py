from langgraph.graph import StateGraph
from models.state import LeadState
from config import MIN_BUDGET, MESSAGES, ERROR_MESSAGES
from utils.validators import (
    collect_string, 
    collect_float, 
    collect_choice,
    is_corporate_event,
    validate_email,
    validate_phone
)


def collect_event_type(state: LeadState) -> LeadState:
    print(MESSAGES["welcome"]) 
    event_type = collect_string("Respuesta")
    state["is_corporate"] = is_corporate_event(event_type)
    return state


def collect_budget(state: LeadState) -> LeadState:
    print(MESSAGES["budget_question"])
    state["budget"] = collect_float("Respuesta", min_value=0.0)
    return state


def collect_contact_info(state: LeadState) -> LeadState:
    print(MESSAGES["contact_question"])
    state["name"] = collect_string("Nombre")
    
    contact_type = collect_choice(
        "¿Prefieres email o teléfono? (email/teléfono)",
        choices=["email", "correo","teléfono", "telefono"],
        case_sensitive=False
    )
    
    if contact_type.lower() in ["email", "e-mail", "correo"]:
        state["contact"] = collect_string("Email", validator=validate_email)
    else:
        state["contact"] = collect_string("Teléfono", validator=validate_phone)
    
    return state


def evaluate_qualification(state: LeadState) -> LeadState:
    print(MESSAGES["evaluation_header"])
    
    is_corporate = state["is_corporate"]
    budget = state["budget"]
    name = state["name"]
    contact = state["contact"]
    
    if not is_corporate:
        print(ERROR_MESSAGES["not_corporate"])
        state["qualified"] = False
    elif budget < MIN_BUDGET:
        print(ERROR_MESSAGES["insufficient_budget"].format(min_budget=MIN_BUDGET))
        state["qualified"] = False
    elif not name.strip():
        print(ERROR_MESSAGES["missing_name"])
        state["qualified"] = False
    elif not contact.strip():
        print(ERROR_MESSAGES["missing_contact"])
        state["qualified"] = False
    else:
        # Lead is qualified
        state["qualified"] = True
        print(MESSAGES["qualified_success"])
        print(MESSAGES["qualified_summary"])
        print(f"   • Tipo de evento: Corporativo")
        print(f"   • Presupuesto: ${budget:,.2f} USD")
        print(f"   • Nombre: {name}")
        print(f"   • Contacto: {contact}")
        print(MESSAGES["contact_followup"])
    
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(LeadState)
    
    workflow.add_node("collect_event_type", collect_event_type)
    workflow.add_node("collect_budget", collect_budget)
    workflow.add_node("collect_contact_info", collect_contact_info)
    workflow.add_node("evaluate_qualification", evaluate_qualification)
    
    workflow.set_entry_point("collect_event_type")
    
    workflow.add_edge("collect_event_type", "collect_budget")
    workflow.add_edge("collect_budget", "collect_contact_info")
    workflow.add_edge("collect_contact_info", "evaluate_qualification")
    
    return workflow.compile()