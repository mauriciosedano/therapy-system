import boto3
import os
from datetime import datetime
import json
import logging
from handlers.patient_handler import PatientHandler

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializar clientes y handlers
dynamodb = boto3.client('dynamodb')
patient_handler = PatientHandler()

# Variables de ambiente
PATIENTS_TABLE = os.getenv("PATIENTS_TABLE", "Patients")
TERAPIAS_TABLE = os.getenv("TERAPIAS_TABLE", "Terapias")
FORMULAS_TABLE = os.getenv("FORMULAS_TABLE", "Formulas")

def handler(event, context):
    """Main handler for Alexa Skill requests."""
    print("Evento recibido:", json.dumps(event))
    
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_response(
                "Bienvenido a Terapias Homeopáticas. Puedes registrar pacientes, "
                "consultar información o registrar terapias. ¿Qué deseas hacer?"
            )
        
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            
            # Mapeo de intents a handlers
            intent_handlers = {
                "RegistrarPacienteIntent": patient_handler.handle_register_patient,
                "ConsultarPacienteIntent": patient_handler.handle_query_patient,
                "AMAZON.HelpIntent": handle_help,
                "AMAZON.CancelIntent": handle_cancel,
                "AMAZON.StopIntent": handle_stop
            }
            
            if intent_name in intent_handlers:
                return intent_handlers[intent_name](event['request'])
            
            return build_response("No entendí esa solicitud. ¿Podrías reformularla?")
            
    except Exception as e:
        print(f"Error procesando la solicitud: {str(e)}")
        return build_response(
            "Hubo un error procesando tu solicitud. Por favor, intenta de nuevo."
        )

def handle_help(event):
    """Handle AMAZON.HelpIntent."""
    return build_response(
        "Puedes decir: registrar paciente, consultar paciente, "
        "o registrar terapia. ¿Qué deseas hacer?"
    )

def handle_cancel(event):
    """Handle AMAZON.CancelIntent."""
    return build_response("Operación cancelada. ¿Hay algo más en lo que pueda ayudarte?")

def handle_stop(event):
    """Handle AMAZON.StopIntent."""
    return build_response("¡Hasta luego!", should_end_session=True)

def build_response(speech_text, should_end_session=False):
    """Build the Alexa response with the correct format."""
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech_text
            },
            "shouldEndSession": should_end_session,
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "¿Hay algo más en lo que pueda ayudarte?"
                }
            }
        }
    }
