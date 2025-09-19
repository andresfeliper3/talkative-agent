"""
Configuration constants for the lead qualification system.

This module centralizes all configuration values and constants
"""

# Qualification criteria
MIN_BUDGET = 1000.0

CORPORATE_KEYWORDS = {
    "corporativo", 
    "corporate", 
    "empresarial", 
    "business",
    "empresa"
}

MIN_EMAIL_LENGTH = 5
MIN_PHONE_DIGITS = 7

MESSAGES = {
    "welcome": "Hola, gracias por escribirnos. ¿Qué tipo de evento quieres organizar?",
    "budget_question": "¿Cuál es tu presupuesto estimado en USD?",
    "contact_question": "Perfecto. ¿Me compartes tu nombre y un email o teléfono de contacto?",
    "evaluation_header": "\n--- Evaluando tu solicitud ---",
    "qualified_success": "¡Perfecto!",
    "qualified_summary": "Resumen de tu solicitud:",
    "contact_followup": "\nPronto te contactará nuestro equipo comercial.",
    "conversation_end": "\n--- Conversación terminada ---"
}

ERROR_MESSAGES = {
    "not_corporate": "Lo sentimos, nuestro trabajo se enfoca principalmente en eventos corporativos.",
    "insufficient_budget": "Lo sentimos, no podemos trabajar con presupuestos menores a ${min_budget:,.0f} USD.",
    "missing_name": "Ingresa tu nombre.",
    "missing_contact": "Ingresa tu email o teléfono de contacto.",
    "invalid_input": "Por favor, ingresa un valor válido.",
    "invalid_number": "Por favor, ingresa un número válido.",
    "invalid_choice": "Por favor, elige una de estas opciones: {choices}",
    "min_value": "Por favor, ingresa un valor mayor o igual a {min_value}."
}
