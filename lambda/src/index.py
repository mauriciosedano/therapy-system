import boto3
import os
from datetime import datetime
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
THERAPY_TABLE = os.environ['THERAPY_TABLE']

def handler(event, context):
    """Handler principal."""
    logger.info("Evento recibido: %s", json.dumps(event))
    
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_response(
                "Bienvenido a memoria de terapias. ¿Qué deseas recordar?"
            )
        
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            logger.info("Intent recibido: %s", intent_name)
            
            handlers = {
                "RegistrarTerapiaIntent": registrar_terapia,
                "ConsultarTerapiaIntent": consultar_terapia,
                "AMAZON.HelpIntent": handle_help,
                "AMAZON.StopIntent": handle_stop,
                "AMAZON.CancelIntent": handle_cancel
            }
            
            if intent_name in handlers:
                return handlers[intent_name](event)
            
        logger.warning("Tipo de request no manejado: %s", 
                      event.get('request', {}).get('type'))
        return build_response(
            "No entendí esa solicitud. ¿Podrías reformularla?"
        )
            
    except Exception as e:
        logger.error("Error procesando evento: %s", str(e))
        return build_response(
            "Hubo un error procesando tu solicitud. Por favor, intenta de nuevo."
        )

def registrar_terapia(event):
    """Registra una nueva terapia."""
    logger.info("Iniciando registro de terapia")
    try:
        slots = event['request']['intent']['slots']
        paciente = slots.get('Paciente', {}).get('value')
        tipo_terapia = slots.get('TipoTerapia', {}).get('value')
        fecha = slots.get('Fecha', {}).get('value', 
                                         datetime.utcnow().date().isoformat())
        
        # Generar IDs
        patient_id = f"P{hash(paciente)}"
        therapy_id = f"T{int(datetime.utcnow().timestamp())}"
        
        # Registrar terapia
        dynamodb.put_item(
            TableName=THERAPY_TABLE,
            Item={
                'PatientID': {'S': patient_id},
                'TherapyDate': {'S': fecha},
                'PatientName': {'S': paciente},
                'TherapyType': {'S': tipo_terapia},
                'TherapyID': {'S': therapy_id},
                'Timestamp': {'S': datetime.utcnow().isoformat()}
            }
        )
        
        return build_response(
            f"He registrado la terapia de {tipo_terapia} para {paciente}."
        )
        
    except Exception as e:
        logger.error("Error en registrar_terapia: %s", str(e))
        return build_response(
            "Hubo un error registrando la terapia. Por favor, intenta nuevamente."
        )

def consultar_terapia(event):
    """Consulta terapias de un paciente."""
    logger.info("Iniciando consulta de terapia")
    try:
        slots = event['request']['intent']['slots']
        paciente = slots['Paciente']['value']
        
        # Consultar por nombre de paciente
        response = dynamodb.query(
            TableName=THERAPY_TABLE,
            IndexName='PatientNameIndex',
            KeyConditionExpression='PatientName = :name',
            ExpressionAttributeValues={
                ':name': {'S': paciente}
            },
            ScanIndexForward=False,
            Limit=5
        )
        
        if not response.get('Items'):
            return build_response(
                f"No encontré terapias registradas para {paciente}."
            )
        
        # Formatear respuesta
        terapias = [
            f"{item['TherapyType']['S']} el {item['TherapyDate']['S']}"
            for item in response['Items']
        ]
        
        return build_response(
            f"Las últimas terapias de {paciente} fueron: {', '.join(terapias)}"
        )
        
    except Exception as e:
        logger.error("Error en consultar_terapia: %s", str(e))
        return build_response(
            "Hubo un error consultando las terapias. Por favor, intenta nuevamente."
        )

def handle_help(event):
    """Maneja intent de ayuda."""
    return build_response(
        "Puedes pedirme que registre una terapia o consulte las terapias de un paciente. "
        "¿Qué deseas hacer?"
    )

def handle_stop(event):
    """Maneja intent de parada."""
    return build_response("¡Hasta luego!", True)

def handle_cancel(event):
    """Maneja intent de cancelación."""
    return build_response(
        "De acuerdo, ¿hay algo más en lo que pueda ayudarte?"
    )

def build_response(speech_text, should_end_session=False):
    """Construye respuesta para Alexa."""
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

