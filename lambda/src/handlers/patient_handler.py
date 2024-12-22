import boto3
from datetime import datetime
from difflib import SequenceMatcher
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
PATIENTS_TABLE = os.getenv("PATIENTS_TABLE", "Patients")

class PatientHandler:
    def __init__(self):
        self.dynamodb = dynamodb

    def handle_register_patient(self, intent_request):
        """
        Maneja el registro de pacientes con validación de nombres similares
        y diálogo natural.
        """
        slots = intent_request['intent']['slots']
        name = slots.get('Nombre', {}).get('value')
        phone = slots.get('Telefono', {}).get('value')
        
        # Validación básica
        if not name or not phone:
            return self.build_response(
                "Necesito el nombre y teléfono del paciente. ¿Podrías proporcionarlos?"
            )
        
        try:
            # Verificar nombres similares
            similar_patients = self.find_similar_patients(name)
            if similar_patients:
                patients_info = "; ".join(
                    f"{p['name']} con teléfono {p['phone']}"
                    for p in similar_patients
                )
                return self.build_response(
                    f"Encontré pacientes con nombres similares: {patients_info}. "
                    "¿Deseas continuar con el registro o revisar estos registros primero?"
                )
            
            # Registrar nuevo paciente
            patient_id = f"P{int(datetime.utcnow().timestamp())}"
            self.dynamodb.put_item(
                TableName=PATIENTS_TABLE,
                Item={
                    "PatientID": {"S": patient_id},
                    "Name": {"S": name},
                    "Phone": {"S": phone},
                    "RegisterDate": {"S": datetime.utcnow().isoformat()},
                    "LastUpdate": {"S": datetime.utcnow().isoformat()}
                }
            )
            return self.build_response(
                f"He registrado a {name} con teléfono {phone}. "
                "¿Quieres registrar una terapia ahora?"
            )
            
        except Exception as e:
            logger.error(f"Error registrando paciente: {str(e)}")
            return self.build_response(
                "Hubo un error al registrar el paciente. Por favor, inténtalo nuevamente."
            )

    def find_similar_patients(self, name):
        """
        Busca pacientes con nombres similares usando diflib.
        Retorna lista de pacientes similares o lista vacía.
        """
        try:
            response = self.dynamodb.scan(
                TableName=PATIENTS_TABLE,
                ProjectionExpression="#n, Phone, PatientID",
                ExpressionAttributeNames={
                    "#n": "Name"
                }
            )

            similar_patients = []
            for item in response.get('Items', []):
                stored_name = item['Name']['S']
                if SequenceMatcher(None, name.lower(), stored_name.lower()).ratio() > 0.8:
                    similar_patients.append({
                        'name': stored_name,
                        'phone': item['Phone']['S'],
                        'id': item['PatientID']['S']
                    })
            
            return similar_patients
            
        except Exception as e:
            logger.error(f"Error buscando pacientes similares: {str(e)}")
            return []

    def handle_query_patient(self, intent_request):
        """
        Maneja consultas sobre pacientes existentes.
        """
        slots = intent_request['intent']['slots']
        name = slots.get('Nombre', {}).get('value')
        
        if not name:
            return self.build_response(
                "¿Qué paciente quieres consultar?"
            )
            
        try:
            # Buscar paciente por nombre
            similar_patients = self.find_similar_patients(name)
            
            if not similar_patients:
                return self.build_response(
                    f"No encontré ningún paciente con el nombre {name}. "
                    "¿Quieres registrarlo?"
                )
                
            if len(similar_patients) == 1:
                patient = similar_patients[0]
                return self.build_response(
                    f"Encontré a {patient['name']} con teléfono {patient['phone']}. "
                    "¿Qué más quieres saber?"
                )
                
            # Múltiples coincidencias
            patients_info = "; ".join(
                f"{p['name']} con teléfono {p['phone']}"
                for p in similar_patients
            )
            return self.build_response(
                f"Encontré varios pacientes similares: {patients_info}. "
                "¿Podrías ser más específico?"
            )
            
        except Exception as e:
            logger.error(f"Error consultando paciente: {str(e)}")
            return self.build_response(
                "Hubo un error al consultar el paciente. Por favor, inténtalo nuevamente."
            )

    def build_response(self, speech_text, should_end_session=False):
        """Construye la respuesta para Alexa."""
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
