from langgraph.graph import StateGraph
from models.state import LeadState
from config import MIN_BUDGET, MESSAGES, ERROR_MESSAGES
from services.llm_classifier import classify_event_with_llm, is_llm_available
from utils.validators import (
    collect_string, 
    collect_float, 
    collect_choice,
    collect_yes_no_describe,
    collect_contact_with_detection
)


def collect_event_type(state: LeadState) -> LeadState:
    choice, description = collect_yes_no_describe()
    
    if choice == "yes":
        state["is_corporate"] = True
    elif choice == "no":
        state["is_corporate"] = False
    elif choice == "describe":
        if is_llm_available():
            print("Analizando tu descripción...")
            is_corporate = classify_event_with_llm(description)
            state["is_corporate"] = is_corporate
            
            if is_corporate:
                print("Basado en tu descripción, tu evento es corporativo.")
            else:
                print("Basado en tu descripción, tu evento no es corporativo.")
        else:
            print("Servicio de IA no disponible. Usando clasificación manual.")
            print("Por favor, responde si tu evento es corporativo:")
            manual_choice = collect_choice(
                "¿Es corporativo? (sí/no)",
                choices=["sí", "si", "yes", "no", "n"],
                case_sensitive=False
            )
            state["is_corporate"] = manual_choice.lower() in ["sí", "si", "yes"]
    
    return state


def collect_budget(state: LeadState) -> LeadState:
    print(MESSAGES["budget_question"])
    state["budget"] = collect_float("Respuesta", min_value=0.0)
    return state


def collect_contact_info(state: LeadState) -> LeadState:
    print(MESSAGES["contact_question"])
    state["name"] = collect_string("Nombre")
    
    contact_value, contact_type = collect_contact_with_detection()
    state["contact"] = contact_value
    state["contact_type"] = contact_type
    
    return state


def evaluate_qualification(state: LeadState) -> LeadState:
    print(MESSAGES["evaluation_header"])
    
    is_corporate = state["is_corporate"]
    budget = state["budget"]
    name = state["name"]
    contact = state["contact"]
    contact_type = state["contact_type"]
    
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
        print(f"   • Contacto ({contact_type}): {contact}")
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