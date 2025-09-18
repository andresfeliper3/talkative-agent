import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def load_prompt_template() -> str:
    """Load the prompt template from markdown file."""
    prompt_file = Path(__file__).parent.parent / "prompts" / "event_classification.md"
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the template part (everything after the last ##)
    sections = content.split('## Instrucciones de Respuesta')
    if len(sections) >= 2:
        template_section = sections[1].strip()
        return template_section
    else:
        # Fallback to the entire content if structure is different
        return content


class EventClassifier:
    """Service for classifying events using LLM."""
    
    def __init__(self):
        self.llm = None
        self.prompt_template = None
        self.output_parser = StrOutputParser()
        self._initialize_llm()
    
    def _initialize_llm(self) -> None:
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1, 
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Load prompt template from markdown file
            template_content = load_prompt_template()
            self.prompt_template = ChatPromptTemplate.from_template(template_content)
            
        except Exception as e:
            print(f"Error inicializando LLM: {e}")
            self.llm = None
    
    def is_available(self) -> bool:
        return self.llm is not None and os.getenv("OPENAI_API_KEY") is not None

    
    def classify_event(self, event_description: str) -> Optional[bool]:
        """
        Classify an event as corporate or not using LLM.
        
        Args:
            event_description: Description of the event
            
        Returns:
            True if corporate, False if not corporate, None if error
        """
        if not self.is_available():
            return None
        
        try:
            chain = self.prompt_template | self.llm | self.output_parser
            response = chain.invoke({"event_description": event_description})
            response_clean = response.strip().upper()
            
            if "CORPORATIVO" in response_clean and "NO CORPORATIVO" not in response_clean:
                return True
            elif "NO CORPORATIVO" in response_clean:
                return False
            else:
                # Fallback: try to extract meaning
                if any(word in response_clean for word in ["CORPORATIVO", "EMPRESARIAL", "NEGOCIO"]):
                    return True
                else:
                    return False
                    
        except Exception as e:
            print(f"Error en clasificación LLM: {e}")
            return None


# Global instance
event_classifier = EventClassifier()


def classify_event_with_llm(event_description: str) -> Optional[bool]:
    return event_classifier.classify_event(event_description)


def is_llm_available() -> bool:
    return event_classifier.is_available()
