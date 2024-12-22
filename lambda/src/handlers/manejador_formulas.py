import logging
import boto3
from datetime import datetime
from utils.response_builder import constructor_respuesta

logger = logging.getLogger()

class ManejadorFormulas:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.tabla_formulas = "Formulas"
        self.tabla_pacientes = "Patients"
    
    def registrar_formula(self, event):
        """Maneja RegistrarFormulaIntent"""
        try:
            slots = event['request']['intent']['slots']
            paciente = slots.get('Paciente', {}).get('value')
            tipo_formula = slots.get('TipoFormula', {}).get('value')
            dosificacion = slots.get('Dosificacion', {}).get('value', 'estándar')
            
            if not paciente or not tipo_formula:
                return constructor_respuesta.construir_respuesta(
                    texto_respuesta="Necesito el nombre del paciente y el tipo de fórmula. ¿Podrías proporcionarlos?",
                    titulo_tarjeta="Registro de Fórmula"
                )
            
            # Verificar paciente
            response = self.dynamodb.query(
                TableName=self.tabla_pacientes,
                IndexName="NameIndex",
                KeyConditionExpression="Name = :nombre",
                ExpressionAttributeValues={
                    ':nombre': {'S': paciente}
                }
            )
            
            if not response.get('Items'):
                return constructor_respuesta.construir_respuesta(
                    texto_respuesta=f"No encontré al paciente {paciente}. ¿Deseas registrarlo primero?",
                    titulo_tarjeta="Paciente no encontrado"
                )
            
            # Registrar fórmula
            formula_id = f"F{int(datetime.utcnow().timestamp())}"
            self.dynamodb.put_item(
                TableName=self.tabla_formulas,
                Item={
                    'FormulaID': {'S': formula_id},
                    'PatientID': {'S': response['Items'][0]['PatientID']['S']},
                    'PatientName': {'S': paciente},
                    'FormulaType': {'S': tipo_formula},
                    'Dosage': {'S': dosificacion},
                    'CreatedAt': {'S': datetime.utcnow().isoformat()},
                    'Status': {'S': 'ACTIVE'}
                }
            )
            
            return constructor_respuesta.construir_respuesta(
                texto_respuesta=f"He registrado la fórmula de {tipo_formula} para {paciente} con dosificación {dosificacion}.",
                titulo_tarjeta="Fórmula Registrada"
            )
            
        except Exception as e:
            logger.error("Error registrando fórmula: %s", str(e))
            return constructor_respuesta.construir_error(
                "Hubo un error registrando la fórmula. Por favor, intenta nuevamente."
            )
    
    def consultar_formula(self, event):
        """Maneja ConsultarFormulaIntent"""
        try:
            slots = event['request']['intent']['slots']
            paciente = slots.get('Paciente', {}).get('value')
            
            # Consultar fórmulas del paciente
            response = self.dynamodb.query(
                TableName=self.tabla_formulas,
                IndexName="PatientNameIndex",
                KeyConditionExpression="PatientName = :nombre",
                ExpressionAttributeValues={
                    ':nombre': {'S': paciente}
                }
            )
            
            if not response.get('Items'):
                return constructor_respuesta.construir_respuesta(
                    texto_respuesta=f"No encontré fórmulas registradas para {paciente}.",
                    titulo_tarjeta="Consulta de Fórmulas"
                )
            
            # Formatear respuesta
            formulas = []
            for item in response['Items']:
                fecha = datetime.fromisoformat(item['CreatedAt']['S']).strftime('%d/%m/%Y')
                formulas.append(
                    f"{item['FormulaType']['S']} ({fecha})"
                )
            
            formulas_str = ", ".join(formulas)
            return constructor_respuesta.construir_respuesta(
                texto_respuesta=f"Las fórmulas de {paciente} son: {formulas_str}",
                titulo_tarjeta="Fórmulas Encontradas"
            )
            
        except Exception as e:
            logger.error("Error consultando fórmulas: %s", str(e))
            return constructor_respuesta.construir_error(
                "Hubo un error consultando las fórmulas. Por favor, intenta nuevamente."
            )
