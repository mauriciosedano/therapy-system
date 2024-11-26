import json
import logging
from datetime import datetime
from utils.response_builder import build_alexa_response, build_error_response
import boto3

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Clientes AWS
dynamodb = boto3.client('dynamodb')

def handle_delegation(event):
    """Handler para DelegarAccesoIntent"""
    try:
        slots = event['request']['intent']['slots']
        aprendiz = slots['Aprendiz']['value']
        permiso = slots['Permiso']['value']
        
        # Generar IDs únicos
        delegation_id = f"D{int(datetime.now().timestamp())}"
        apprentice_id = f"A{hash(aprendiz)}"
        master_id = event['session']['user']['userId']
        
        # Registrar delegación
        dynamodb.put_item(
            TableName='AccessDelegation',
            Item={
                'DelegationID': {'S': delegation_id},
                'MasterID': {'S': master_id},
                'ApprenticeID': {'S': apprentice_id},
                'Permissions': {'SS': [permiso]},
                'ExpirationDate': {'S': (datetime.now().isoformat())},
                'Status': {'S': 'ACTIVE'}
            }
        )
        
        return build_alexa_response(
            speech_text=f"He autorizado a {aprendiz} para {permiso}",
            card_title="Delegación de Acceso"
        )
        
    except Exception as e:
        logger.error(f"Error en delegación: {str(e)}")
        return build_error_response(
            "Hubo un error procesando la delegación. Por favor, intenta nuevamente."
        )

def handle_apprentice_audit(event):
    """Handler para ConsultarAccionesAprendizIntent"""
    try:
        slots = event['request']['intent']['slots']
        aprendiz = slots['Aprendiz']['value']
        apprentice_id = f"A{hash(aprendiz)}"
        
        # Consultar acciones del aprendiz
        response = dynamodb.query(
            TableName='AuditLog',
            IndexName='UserActionsIndex',
            KeyConditionExpression='PerformedBy = :pid',
            ExpressionAttributeValues={
                ':pid': {'S': apprentice_id}
            },
            ScanIndexForward=False,
            Limit=5
        )
        
        if not response.get('Items'):
            return build_alexa_response(
                speech_text=f"No encontré acciones registradas para {aprendiz}",
                card_title="Consulta de Acciones"
            )
        
        acciones = [item['ActionType']['S'] for item in response['Items']]
        return build_alexa_response(
            speech_text=f"{aprendiz} ha realizado {len(acciones)} acciones recientes: {', '.join(acciones)}",
            card_title="Consulta de Acciones"
        )
        
    except Exception as e:
        logger.error(f"Error en consulta de acciones: {str(e)}")
        return build_error_response(
            "Hubo un error consultando las acciones. Por favor, intenta nuevamente."
        )

def handle_patient_registration(event):
    """Handler para RegistrarPacienteIntent"""
    try:
        slots = event['request']['intent']['slots']
        nombre = slots['Nombre']['value']
        telefono = slots['Telefono']['value']
        
        # Generar ID único
        patient_id = f"P{int(datetime.now().timestamp())}"
        
        # Registrar paciente
        dynamodb.put_item(
            TableName='Patients',
            Item={
                'PatientID': {'S': patient_id},
                'Name': {'S': nombre},
                'Phone': {'S': telefono},
                'RegisterDate': {'S': datetime.now().isoformat()}
            }
        )
        
        return build_alexa_response(
            speech_text=f"He registrado al paciente {nombre} con teléfono {telefono}",
            card_title="Registro de Paciente"
        )
        
    except Exception as e:
        logger.error(f"Error en registro de paciente: {str(e)}")
        return build_error_response(
            "Hubo un error registrando al paciente. Por favor, intenta nuevamente."
        )

def handle_therapy_registration(event):
    """Handler para RegistrarTerapiaIntent"""
    try:
        slots = event['request']['intent']['slots']
        paciente = slots['Paciente']['value']
        tipo_terapia = slots['TipoTerapia']['value']
        fecha = slots.get('Fecha', {}).get('value', datetime.now().date().isoformat())
        
        # Generar ID único
        therapy_id = f"T{int(datetime.now().timestamp())}"
        
        # Registrar terapia
        dynamodb.put_item(
            TableName='Therapies',
            Item={
                'TherapyID': {'S': therapy_id},
                'PatientName': {'S': paciente},
                'TherapyType': {'S': tipo_terapia},
                'Date': {'S': fecha},
                'Timestamp': {'S': datetime.now().isoformat()}
            }
        )
        
        return build_alexa_response(
            speech_text=f"He registrado la terapia de {tipo_terapia} para {paciente}",
            card_title="Registro de Terapia"
        )
        
    except Exception as e:
        logger.error(f"Error en registro de terapia: {str(e)}")
        return build_error_response(
            "Hubo un error registrando la terapia. Por favor, intenta nuevamente."
        )

def handle_therapy_query(event):
    """Handler para ConsultarTerapiaIntent"""
    try:
        slots = event['request']['intent']['slots']
        paciente = slots['Paciente']['value']
        
        # Consultar terapias
        response = dynamodb.query(
            TableName='Therapies',
            IndexName='PatientIndex',
            KeyConditionExpression='PatientName = :pname',
            ExpressionAttributeValues={
                ':pname': {'S': paciente}
            },
            ScanIndexForward=False,
            Limit=5
        )
        
        if not response.get('Items'):
            return build_alexa_response(
                speech_text=f"No encontré terapias registradas para {paciente}",
                card_title="Consulta de Terapias"
            )
        
        terapias = [f"{item['TherapyType']['S']} el {item['Date']['S']}" 
                   for item in response['Items']]
        
        return build_alexa_response(
            speech_text=f"Las últimas terapias de {paciente} fueron: {', '.join(terapias)}",
            card_title="Consulta de Terapias"
        )
        
    except Exception as e:
        logger.error(f"Error en consulta de terapia: {str(e)}")
        return build_error_response(
            "Hubo un error consultando las terapias. Por favor, intenta nuevamente."
        )
