from typing import Any, Callable, Optional
import re

from config import CORPORATE_KEYWORDS, MIN_EMAIL_LENGTH, MIN_PHONE_DIGITS, ERROR_MESSAGES


def collect_string(prompt: str, validator: Optional[Callable[[str], bool]] = None) -> str:
    """
    Collect a non-empty string from user input.
    
    Args:
        prompt: The prompt to display to the user
        validator: Optional validation function
        
    Returns:
        Validated string input
    """
    while True:
        value = input(f"{prompt}: ").strip()
        if value and (validator is None or validator(value)):
            return value
        print(ERROR_MESSAGES["invalid_input"])


def collect_float(prompt: str, min_value: float = 0.0) -> float:
    """
    Collects a valid float from user input.
    
    Args:
        prompt: The prompt to display to the user
        min_value: Minimum allowed value
        
    Returns:
        Validated float input
    """
    while True:
        try:
            value = float(input(f"{prompt}: ").strip())
            if value >= min_value:
                return value
            print(ERROR_MESSAGES["min_value"].format(min_value=min_value))
        except ValueError:
            print(ERROR_MESSAGES["invalid_number"])


def collect_yes_no_describe() -> tuple[str, str]:
    """
    Collect user choice for corporate event classification.
    
    Returns:
        Tuple of (choice, description) where:
        - choice: "yes", "no", or "describe"
        - description: empty string for yes/no, user description for describe
    """
    print("¿Tu evento es corporativo?")
    print("1. Sí - Es un evento corporativo")
    print("2. No - No es un evento corporativo") 
    print("3. Describe tu evento para que podamos clasificarlo")
    
    while True:
        choice = input("Selecciona una opción (1/2/3 o sí/no/describir): ").strip().lower()
        
        if choice in ["1", "sí", "si", "yes", "y"]:
            return "yes", ""
        elif choice in ["2", "no", "n"]:
            return "no", ""
        elif choice in ["3", "describir", "describe", "d"]:
            description = input("Describe tu evento: ").strip()
            if description:
                return "describe", description
            else:
                print("Por favor, proporciona una descripción del evento.")
        else:
            print("Por favor, selecciona una opción válida (1/2/3 o sí/no/describir).")


def collect_contact_type() -> str:
    """
    Collect contact type preference (email or phone) with numeric options.
    
    Returns:
        "email" or "phone" based on user selection
    """
    print("¿Prefieres email o teléfono?")
    print("1. Email")
    print("2. Teléfono")
    
    while True:
        choice = input("Selecciona una opción (1/2 o email/teléfono): ").strip().lower()
        
        # Handle numeric choices
        if choice in ["1", "email", "e-mail", "correo"]:
            return "email"
        elif choice in ["2", "teléfono", "telefono", "phone", "tel"]:
            return "phone"
        else:
            print("Por favor, selecciona una opción válida (1/2 o email/teléfono).")


def collect_choice(prompt: str, choices: list[str], case_sensitive: bool = False) -> str:
    """
    Collect a choice from a list of valid options.
    
    Args:
        prompt: The prompt to display to the user
        choices: List of valid choices
        case_sensitive: Whether to perform case-sensitive matching
        
    Returns:
        Valid choice from the list
    """
    while True:
        value = input(f"{prompt}: ").strip()
        if not case_sensitive:
            value = value.lower()
            choices = [choice.lower() for choice in choices]
        
        if value in choices:
            return value
        print(ERROR_MESSAGES["invalid_choice"].format(choices=', '.join(choices)))


def validate_email(email: str) -> bool:
    """
    Validate email using regex pattern.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email or len(email) < MIN_EMAIL_LENGTH:
        return False
    
    # Check for consecutive dots or special characters at start/end
    if email.startswith('.') or email.endswith('.') or '..' in email:
        return False
    
    # Check for @ symbol count
    if email.count('@') != 1:
        return False
    
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number using regex pattern.
    
    Args:
        phone: Phone string to validate
        
    Returns:
        True if phone appears valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    
    # Check minimum length
    if len(clean_phone) < MIN_PHONE_DIGITS:
        return False
    
    # Check maximum reasonable length (international numbers can be up to 15 digits)
    if len(clean_phone) > 15:
        return False
    
    # Check for valid phone patterns (basic validation)
    # Should contain only digits after cleaning
    return clean_phone.isdigit()


def normalize_email(email: str) -> str:
    """
    Normalize email by converting to lowercase and trimming whitespace.
    
    Args:
        email: Email string to normalize
        
    Returns:
        Normalized email string
    """
    return email.strip().lower()


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number by removing all non-digit characters.
    
    Args:
        phone: Phone string to normalize
        
    Returns:
        Normalized phone string with only digits
    """
    return re.sub(r'\D', '', phone)


def is_valid_email_format(email: str) -> bool:
    """
    Check if email has valid format using regex.
    
    Args:
        email: Email string to check
        
    Returns:
        True if format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone_format(phone: str) -> bool:
    """
    Check if phone has valid format.
    
    Args:
        phone: Phone string to check
        
    Returns:
        True if format is valid, False otherwise
    """
    clean_phone = re.sub(r'\D', '', phone)
    return 7 <= len(clean_phone) <= 15 and clean_phone.isdigit()


def detect_contact_type(contact_input: str) -> tuple[str, str]:
    """
    Automatically detect if the input is an email, phone, or invalid.
    
    Args:
        contact_input: The contact information entered by the user
        
    Returns:
        Tuple of (contact_type, normalized_contact) where:
        - contact_type: "email", "phone", or "invalid"
        - normalized_contact: cleaned/normalized version of the input
    """
    if not contact_input or not contact_input.strip():
        return "invalid", ""
    
    contact_input = contact_input.strip()
    
    if validate_email(contact_input):
        return "email", normalize_email(contact_input)
    
    if validate_phone(contact_input):
        return "phone", normalize_phone(contact_input)
    
    return "invalid", contact_input


def collect_contact_with_detection() -> tuple[str, str]:
    """
    Collect contact information and automatically detect if it's email or phone.
    
    Returns:
        Tuple of (contact_value, contact_type) where:
        - contact_value: The normalized contact information
        - contact_type: "email" or "phone"
    """
    while True:
        contact_input = input("Email o teléfono de contacto: ").strip()
        
        contact_type, normalized_contact = detect_contact_type(contact_input)
        
        if contact_type == "invalid":
            print("Por favor, ingresa un email válido (ej: usuario@ejemplo.com) o un teléfono válido (ej: +1234567890).")
            continue
        
        return normalized_contact, contact_type
