from langgraph.graph import StateGraph
from models.state import LeadState
from config import MIN_BUDGET, MESSAGES, ERROR_MESSAGES
from services.llm_classifier import classify_event_with_llm, is_llm_available
from services.google_sheets import save_lead_to_sheets, is_sheets_available
from utils.validators import (
    collect_string, 
    collect_float, 
    collect_choice,
    collect_yes_no_describe,
    collect_contact_with_detection
)


def collect_event_type(state: LeadState) -> LeadState:
    print(MESSAGES["welcome"])
    choice, description = collect_yes_no_describe()
    
    if choice == "yes":
        state["is_corporate"] = True
        # Ask user for specific corporate event type
        state["event_type"] = input(MESSAGES["corporate_event_type_input"]).strip()
    elif choice == "no":
        state["is_corporate"] = False
        # Ask user for specific event type
        state["event_type"] = input(MESSAGES["event_type_input"]).strip()
    elif choice == "describe":
        if is_llm_available():
            print(MESSAGES["analyzing_description"])
            is_corporate, event_type = classify_event_with_llm(description)
            state["is_corporate"] = is_corporate
            state["event_type"] = event_type or "No especificado"
            
            if is_corporate:
                print(MESSAGES["description_corporate"])
            else:
                print(MESSAGES["description_not_corporate"])
        else:
            print(MESSAGES["llm_unavailable"])
            print(MESSAGES["manual_classification_prompt"])
            manual_choice = collect_choice(
                "¿Es corporativo? (sí/no)",
                choices=["sí", "si", "yes", "no", "n"],
                case_sensitive=False
            )
            is_corporate = manual_choice.lower() in ["sí", "si", "yes"]
            state["is_corporate"] = is_corporate
            
            if is_corporate:
                state["event_type"] = input(MESSAGES["corporate_event_type_input"]).strip()
            else:
                state["event_type"] = input(MESSAGES["event_type_input"]).strip()
    
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
    event_type = state["event_type"]
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
        print(MESSAGES["qualified_success"])
        state["qualified"] = True
    
    return state


def save_lead_data(state: LeadState) -> LeadState:
    if is_sheets_available():
        save_lead_to_sheets(state)
    
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(LeadState)
    
    workflow.add_node("collect_event_type", collect_event_type)
    workflow.add_node("collect_budget", collect_budget)
    workflow.add_node("collect_contact_info", collect_contact_info)
    workflow.add_node("evaluate_qualification", evaluate_qualification)
    workflow.add_node("save_lead_data", save_lead_data)
    
    workflow.set_entry_point("collect_event_type")
    
    workflow.add_edge("collect_event_type", "collect_budget")
    workflow.add_edge("collect_budget", "collect_contact_info")
    workflow.add_edge("collect_contact_info", "evaluate_qualification")
    workflow.add_edge("evaluate_qualification", "save_lead_data")
    
    return workflow.compile()