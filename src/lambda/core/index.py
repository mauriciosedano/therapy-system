import json
import os
import boto3
from datetime import datetime
from lib.natural_language.processor import find_similar_names, extract_therapy_details
from lambda.knowledge.remedies import HomeopathicKnowledge

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializar DynamoDB
dynamodb = boto3.client('dynamodb')
homeopathic = HomeopathicKnowledge(dynamodb)

def handler(event, context):
    """Main handler for Alexa Skill requests."""
    print("Evento recibido:", json.dumps(event))
    
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_response(
                "Bienvenido a Terapias Homeopáticas. Puedes registrar pacientes, "
                "terapias, consultar historiales o consultar sobre remedios. ¿Qué deseas hacer?"
            )
        
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            
            intent_handlers = {
                "RegistrarPacienteIntent": registrar_paciente,
                "RegistrarTerapiaIntent": registrar_terapia,
                "ConsultarTerapiaIntent": consultar_terapia,
                "ConsultarRemedioIntent": consultar_remedio,
                "ConsultarFormulaIntent": consultar_formula
            }
            
            if intent_name in intent_handlers:
                return intent_handlers[intent_name](event)
            
        return build_response("No entendí esa solicitud. ¿Podrías reformularla?")
            
    except Exception as e:
        print(f"Error procesando la solicitud: {str(e)}")
        return build_response(
            "Hubo un error procesando tu solicitud. Por favor, intenta de nuevo."
        )

def registrar_terapia(event):
    """Registra una nueva terapia."""
    logger.info("Iniciando registro de terapia")
    try:
        slots = event['request']['intent']['slots']
        
        # Validación de slots
        paciente = slots.get('Paciente', {}).get('value')
        if not paciente:
            return build_response("¿Para qué paciente quieres registrar la terapia?")
            
        tipo_terapia = slots.get('TipoTerapia', {}).get('value')
        if not tipo_terapia:
            return build_response("¿Qué tipo de terapia quieres registrar?")
            
        fecha = slots.get('Fecha', {}).get('value', datetime.utcnow().date().isoformat())
        
        logger.info(f"Datos validados: Paciente={paciente}, Terapia={tipo_terapia}, Fecha={fecha}")
        
        # Generar IDs
        patient_id = f"P{hash(paciente)}"
        therapy_id = f"T{int(datetime.utcnow().timestamp())}"
        
        # Registrar terapia
        item = {
            'PatientID': {'S': patient_id},
            'TherapyDate': {'S': fecha},
            'PatientName': {'S': paciente},
            'TherapyType': {'S': tipo_terapia},
            'TherapyID': {'S': therapy_id},
            'Timestamp': {'S': datetime.utcnow().isoformat()}
        }
        
        logger.info(f"Intentando registrar: {json.dumps(item)}")
        
        dynamodb.put_item(
            TableName=THERAPY_TABLE,
            Item=item
        )
        
        return build_response(f"He registrado la terapia de {tipo_terapia} para {paciente}.")
        
    except Exception as e:
        logger.error(f"Error en registrar_terapia: {str(e)}")
        logger.error(f"Event: {json.dumps(event)}")
        return build_response("Hubo un error registrando la terapia. Por favor, intenta nuevamente.")

def consultar_terapia(event):
    """Consulta terapias de un paciente."""
    logger.info("Iniciando consulta de terapia")
    try:
        slots = event.get('request', {}).get('intent', {}).get('slots', {})
        paciente = slots.get('Paciente', {}).get('value')
        
        if not paciente:
            # Consultar últimas terapias generales
            response = dynamodb.scan(
                TableName=THERAPY_TABLE,
                Limit=5
            )
        else:
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
            mensaje = (f"No encontré terapias registradas para {paciente}."
                      if paciente else "No hay terapias registradas.")
            return build_response(mensaje)
        
        # Formatear respuesta
        terapias = [
            f"{item['TherapyType']['S']} el {item['TherapyDate']['S']}"
            for item in response['Items']
        ]
        
        mensaje = (f"Las últimas terapias de {paciente} fueron: " if paciente 
                  else "Las últimas terapias registradas fueron: ")
        return build_response(f"{mensaje}{', '.join(terapias)}")
        
    except Exception as e:
        logger.error(f"Error en consultar_terapia: {str(e)}")
        logger.error(f"Event: {json.dumps(event)}")
        return build_response("Hubo un error consultando las terapias. Por favor, intenta nuevamente.")

def build_response(speech_text, should_end_session=False):
    """Construye una respuesta de Alexa."""
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech_text
            },
            "shouldEndSession": should_end_session
        }
    }
