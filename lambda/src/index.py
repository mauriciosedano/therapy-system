"""Handler principal para la Skill de Alexa."""
import json
import logging
from utils.response_builder import constructor_respuesta
from handlers import (
    handle_delegation,
    handle_apprentice_audit,
    handle_patient_registration,
    handle_therapy_registration,
    handle_therapy_query
)
from handlers.manejador_formulas import ManejadorFormulas

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializar manejador de fórmulas
manejador_formulas = ManejadorFormulas()

def handler(event, context):
    """Main handler for Alexa Skill requests."""
    logger.info("Evento recibido: %s", json.dumps(event))
    
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return constructor_respuesta.construir_respuesta(
                texto_respuesta="Bienvenido a Terapias Homeopáticas. "
                              "Puedes registrar pacientes, terapias, "
                              "consultar historiales o registrar fórmulas. "
                              "¿Qué deseas hacer?",
                titulo_tarjeta="Bienvenido a Terapias Homeopáticas"
            )
        
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            
            intent_handlers = {
                "DelegarAccesoIntent": handle_delegation,
                "ConsultarAccionesAprendizIntent": handle_apprentice_audit,
                "RegistrarPacienteIntent": handle_patient_registration,
                "RegistrarTerapiaIntent": handle_therapy_registration,
                "ConsultarTerapiaIntent": handle_therapy_query,
                # Nuevos intents de fórmulas
                "RegistrarFormulaIntent": manejador_formulas.registrar_formula,
                "ConsultarFormulaIntent": manejador_formulas.consultar_formula,
                "AMAZON.HelpIntent": lambda e: constructor_respuesta.construir_respuesta(
                    texto_respuesta="Puedes decir: registrar paciente, registrar terapia, "
                                  "consultar terapias, o registrar fórmula. ¿Qué deseas hacer?",
                    titulo_tarjeta="Ayuda"
                ),
                "AMAZON.StopIntent": lambda e: constructor_respuesta.construir_respuesta(
                    texto_respuesta="¡Hasta luego!",
                    titulo_tarjeta="Adiós",
                    finalizar_sesion=True
                ),
                "AMAZON.CancelIntent": lambda e: constructor_respuesta.construir_respuesta(
                    texto_respuesta="Operación cancelada. ¿Hay algo más en lo que pueda ayudarte?",
                    titulo_tarjeta="Operación Cancelada"
                )
            }
            
            if intent_name in intent_handlers:
                return intent_handlers[intent_name](event)
            
            return constructor_respuesta.construir_error(
                "No entendí esa solicitud. ¿Podrías reformularla?"
            )
            
    except Exception as e:
        logger.error("Error procesando la solicitud: %s", str(e))
        return constructor_respuesta.construir_error(
            "Hubo un error procesando tu solicitud. Por favor, intenta de nuevo."
        )