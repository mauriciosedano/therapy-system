import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
<<<<<<< Updated upstream
=======
THERAPY_TABLE = os.environ['THERAPY_TABLE']
FORMULAS_TABLE = os.environ.get('FORMULAS_TABLE', 'TherapySystem_Formulas')
>>>>>>> Stashed changes

def handler(event, context):
    try:
        if event.get('request', {}).get('type') == "LaunchRequest":
            return build_response("Bienvenido a Terapias Homeopáticas. ¿Qué deseas consultar?")
        if event.get('request', {}).get('type') == "IntentRequest":
            intent_name = event['request']['intent']['name']
<<<<<<< Updated upstream
            if intent_name == "ConsultarRemedioIntent":
                return consultar_remedio(event)
        return build_response("No entendí esa solicitud.")
=======
            logger.info("Intent recibido: %s", intent_name)
            
            handlers = {
                "RegistrarTerapiaIntent": registrar_terapia,
                "ConsultarTerapiaIntent": consultar_terapia,
                "ConsultarFormulaIntent": consultar_formula,
                "RegistrarFormulaIntent": registrar_formula,  # Agregamos esta línea
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
            
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
def build_response(speech_text):
=======
def consultar_formula(event):
    """Consulta fórmulas homeopáticas registradas."""
    logger.info("Iniciando consulta de fórmula: %s", json.dumps(event))
    
    try:
        slots = event['request']['intent']['slots']
        nombre_formula = slots.get('TipoFormula', {}).get('value')
        paciente = slots.get('Paciente', {}).get('value')
        
        # Si tenemos nombre de fórmula, buscamos por fórmula
        if nombre_formula:
            response = dynamodb.query(
                TableName=FORMULAS_TABLE,
                IndexName="FormulaNameIndex",
                KeyConditionExpression="RecipeName = :name",
                ExpressionAttributeValues={
                    ':name': {'S': nombre_formula}
                },
                ScanIndexForward=False,
                Limit=5
            )
            
            if not response.get('Items'):
                return build_response(
                    f"No encontré registros de la fórmula {nombre_formula}. "
                    "¿Deseas registrar una nueva fórmula?"
                )
            
            # Agrupar por paciente
            formulas_por_paciente = {}
            for item in response['Items']:
                paciente_nombre = item['PatientName']['S']
                fecha = item['Date']['S']
                if paciente_nombre not in formulas_por_paciente:
                    formulas_por_paciente[paciente_nombre] = []
                formulas_por_paciente[paciente_nombre].append(fecha)
            
            # Construir respuesta
            respuesta = f"La fórmula {nombre_formula} se ha usado para: "
            detalles = []
            for paciente, fechas in formulas_por_paciente.items():
                detalles.append(f"{paciente} ({len(fechas)} veces, última vez el {fechas[0]})")
            
            return build_response(respuesta + "; ".join(detalles))
            
        # Si tenemos paciente, buscamos sus fórmulas
        elif paciente:
            response = dynamodb.query(
                TableName=FORMULAS_TABLE,
                IndexName="PatientNameIndex",
                KeyConditionExpression="PatientName = :name",
                ExpressionAttributeValues={
                    ':name': {'S': paciente}
                },
                ScanIndexForward=False,
                Limit=5
            )
            
            if not response.get('Items'):
                return build_response(
                    f"No encontré fórmulas registradas para {paciente}. "
                    "¿Deseas registrar una nueva fórmula?"
                )
            
            # Agrupar por tipo de fórmula
            formulas = {}
            for item in response['Items']:
                formula_nombre = item['RecipeName']['S']
                fecha = item['Date']['S']
                if formula_nombre not in formulas:
                    formulas[formula_nombre] = []
                formulas[formula_nombre].append(fecha)
            
            # Construir respuesta
            respuesta = f"Para {paciente} hemos preparado: "
            detalles = []
            for formula, fechas in formulas.items():
                detalles.append(f"{formula} ({len(fechas)} veces, última vez el {fechas[0]})")
            
            return build_response(respuesta + "; ".join(detalles))
            
        else:
            return build_response(
                "Necesito saber qué fórmula quieres consultar o para qué paciente. "
                "¿Podrías especificarlo?"
            )
            
    except Exception as e:
        logger.error("Error consultando fórmula: %s", str(e))
        return build_response(
            "Hubo un error consultando la fórmula. Por favor, intenta nuevamente."
        )

def handle_help(event):
    """Maneja intent de ayuda."""
    return build_response(
        "Puedes pedirme que registre una terapia, consulte las terapias de un paciente, "
        "o consulte fórmulas homeopáticas. ¿Qué deseas hacer?"
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
>>>>>>> Stashed changes
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": speech_text},
            "shouldEndSession": False
        }
    }
<<<<<<< Updated upstream
=======

def registrar_formula(event):
    """Registra una nueva fórmula homeopática."""
    logger.info("Iniciando registro de fórmula: %s", json.dumps(event))
    
    try:
        slots = event['request']['intent']['slots']
        paciente = slots.get('Paciente', {}).get('value')
        tipo_formula = slots.get('TipoFormula', {}).get('value')
        
        if not paciente or not tipo_formula:
            return build_response(
                "Necesito el nombre del paciente y el tipo de fórmula. "
                "¿Podrías proporcionarlos?"
            )
        
        # Generar ID único
        formula_id = f"F{int(datetime.utcnow().timestamp())}"
        
        # Registrar fórmula
        dynamodb.put_item(
            TableName=FORMULAS_TABLE,
            Item={
                'FormulaID': {'S': formula_id},
                'PatientName': {'S': paciente},
                'RecipeName': {'S': tipo_formula},
                'Date': {'S': datetime.utcnow().date().isoformat()},
                'Timestamp': {'S': datetime.utcnow().isoformat()}
            }
        )
        
        return build_response(
            f"He registrado la fórmula {tipo_formula} para {paciente}."
        )
            
    except Exception as e:
        logger.error("Error registrando fórmula: %s", str(e))
        return build_response(
            "Hubo un error registrando la fórmula. Por favor, intenta nuevamente."
        )
>>>>>>> Stashed changes
