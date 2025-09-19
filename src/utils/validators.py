from typing import Callable, Optional
import re

from config import MIN_EMAIL_LENGTH, MIN_PHONE_DIGITS, ERROR_MESSAGES, MESSAGES


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
    print(MESSAGES["event_type_question"])
    for option in MESSAGES["event_type_options"]:
        print(option)
    
    while True:
        choice = input(MESSAGES["event_selection_prompt"]).strip().lower()
        
        if choice in ["1", "sí", "si", "yes", "y"]:
            return "yes", ""
        elif choice in ["2", "no", "n"]:
            return "no", ""
        elif choice in ["3", "describir", "describe", "d"]:
            description = input(MESSAGES["event_description_prompt"]).strip()
            if description:
                return "describe", description
            else:
                print(ERROR_MESSAGES["provide_description"])
        else:
            print(ERROR_MESSAGES["invalid_event_option"])


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
        contact_input = input(MESSAGES["contact_input_prompt"]).strip()
        
        contact_type, normalized_contact = detect_contact_type(contact_input)
        
        if contact_type == "invalid":
            print(ERROR_MESSAGES["invalid_contact"])
            continue
        
        return normalized_contact, contact_type
