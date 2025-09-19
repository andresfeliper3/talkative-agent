"""
Configuration constants for the lead qualification system.

This module centralizes all configuration values and constants
"""

# Qualification criteria
MIN_BUDGET = 1000.0

MIN_EMAIL_LENGTH = 5
MIN_PHONE_DIGITS = 7

# Google Sheets configuration
SHEETS_CONFIG = {
    "spreadsheet_name": "Lead Qualification System",
    "worksheet_name": "Leads",
    "headers": [
        "Es Corporativo",
        "Tipo de Evento", 
        "Presupuesto",
        "Nombre",
        "Contacto",
        "Tipo de Contacto",
        "Calificado",
        "Fecha de Registro"
    ]
}

MESSAGES = {
    "welcome": "¡Hola! 👋\n\nBienvenido a nuestro sistema de calificación de eventos corporativos. Estamos aquí para ayudarte a organizar el evento perfecto para tu empresa.\n\n¿Qué tipo de evento corporativo te gustaría organizar?",
    "budget_question": "¿Cuál es tu presupuesto estimado en USD?",
    "contact_question": "Perfecto. ¿Me compartes tu nombre y un email o teléfono de contacto?",
    "evaluation_header": "\n--- Evaluando tu solicitud ---",
    "qualified_success": "¡Perfecto!\n",
    "conversation_end": "\n--- Conversación terminada ---",
    "event_type_question": "¿Tu evento es corporativo?",
    "event_type_options": [
        "1. Sí - Es un evento corporativo",
        "2. No - No es un evento corporativo", 
        "3. Describe tu evento para que podamos clasificarlo"
    ],
    "analyzing_description": "Analizando tu descripción...",
    "description_corporate": "Basado en tu descripción, tu evento es corporativo.",
    "description_not_corporate": "Basado en tu descripción, tu evento no es corporativo.",
    "llm_unavailable": "Servicio de IA no disponible. Usando clasificación manual.",
    "manual_classification_prompt": "Por favor, responde si tu evento es corporativo: ",
    "event_type_input": "¿Qué tipo de evento quieres organizar? ",
    "corporate_event_type_input": "¿Qué tipo de evento corporativo quieres organizar? ",
    "event_selection_prompt": "Selecciona una opción (1/2/3 o sí/no/describir): ",
    "event_description_prompt": "Describe tu evento: ",
    "contact_input_prompt": "Email o teléfono de contacto: ",
    "final_state": "Estado final: {final_state}"
}

ERROR_MESSAGES = {
    "not_corporate": "Lo sentimos, nuestro trabajo se enfoca principalmente en eventos corporativos.",
    "insufficient_budget": "Lo sentimos, no podemos trabajar con presupuestos menores a ${min_budget:,.0f} USD.",
    "missing_name": "Ingresa tu nombre.",
    "missing_contact": "Ingresa tu email o teléfono de contacto.",
    "invalid_input": "Por favor, ingresa un valor válido.",
    "invalid_number": "Por favor, ingresa un número válido.",
    "invalid_choice": "Por favor, elige una de estas opciones: {choices}",
    "min_value": "Por favor, ingresa un valor mayor o igual a {min_value}.",
    "provide_description": "Por favor, proporciona una descripción del evento.",
    "invalid_event_option": "Por favor, selecciona una opción válida (1/2/3 o sí/no/describir).",
    "invalid_contact": "Por favor, ingresa un email válido (ej: usuario@ejemplo.com) o un teléfono válido (ej: +1234567890).",
    "llm_classification_error": "Error en clasificación LLM: {error}"
}
