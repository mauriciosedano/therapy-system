"""Handler principal para la Skill de Alexa."""
import json
import logging
from utils.response_builder import build_alexa_response, build_error_response
from handlers import (
    handle_delegation,
    handle_apprentice_audit,
    handle_patient_registration,
    handle_therapy_registration,
    handle_therapy_query
)

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """Main handler for Alexa Skill requests."""
    logger.info("Evento recibido: %s", json.dumps(event))
    
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_alexa_response(
                speech_text="Bienvenido a Terapias Homeopáticas. "
                          "Puedes registrar pacientes, terapias, "
                          "consultar historiales o registrar fórmulas. "
                          "¿Qué deseas hacer?",
                card_title="Bienvenido a Terapias Homeopáticas"
            )
        
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            
            intent_handlers = {
                "DelegarAccesoIntent": handle_delegation,
                "ConsultarAccionesAprendizIntent": handle_apprentice_audit,
                "RegistrarPacienteIntent": handle_patient_registration,
                "RegistrarTerapiaIntent": handle_therapy_registration,
                "ConsultarTerapiaIntent": handle_therapy_query,
                "AMAZON.HelpIntent": lambda e: build_alexa_response(
                    "Puedes decir: registrar paciente, registrar terapia, "
                    "consultar terapias, o registrar fórmula. ¿Qué deseas hacer?"
                ),
                "AMAZON.StopIntent": lambda e: build_alexa_response(
                    "¡Hasta luego!", should_end_session=True
                ),
                "AMAZON.CancelIntent": lambda e: build_alexa_response(
                    "Operación cancelada. ¿Hay algo más en lo que pueda ayudarte?"
                )
            }
            
            if intent_name in intent_handlers:
                return intent_handlers[intent_name](event)
            
            return build_error_response(
                "No entendí esa solicitud. ¿Podrías reformularla?"
            )
            
    except Exception as e:
        logger.error("Error procesando la solicitud: %s", str(e))
        return build_error_response(
            "Hubo un error procesando tu solicitud. Por favor, intenta de nuevo."
        )
