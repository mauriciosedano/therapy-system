import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')

def handler(event, context):
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_response("Bienvenido a Terapias Homeopáticas. ¿Qué deseas consultar?")
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
            if intent_name == "ConsultarRemedioIntent":
                return consultar_remedio(event)
        return build_response("No entendí esa solicitud.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return build_response("Hubo un error. Por favor, intenta de nuevo.")

def consultar_remedio(event):
    try:
        remedio = event['request']['intent']['slots']['Remedio']['value']
        logger.info(f"Consultando remedio: {remedio}")
        
        response = dynamodb.query(
            TableName="TherapySystem_Homeopathy",
            IndexName="RemedyNameIndex",
            KeyConditionExpression="RemedyName = :name",
            ExpressionAttributeValues={":name": {"S": remedio}}
        )
        
        items = response.get('Items', [])
        if not items:
            return build_response(f"No encontré información sobre {remedio}.")
        
        item = items[0]
        respuesta = f"{remedio} se usa para: {item['Properties']['S']}"
        return build_response(respuesta)
        
    except Exception as e:
        logger.error(f"Error en consultar_remedio: {str(e)}")
        return build_response("Error consultando el remedio.")

def build_response(speech_text):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": speech_text},
            "shouldEndSession": False
        }
    }
