import boto3
import json
import logging
from datetime import datetime
import os

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('tests/logs/alexa_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AlexaIntegration')

class AlexaIntegrationTest:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.function_name = 'therapy-system'
        self.results = []

    def test_intent(self, payload_file):
        """Prueba un intent específico usando un payload"""
        try:
            # Cargar payload
            with open(f"tests/payloads/{payload_file}", 'r') as f:
                payload = json.load(f)
            
            # Invocar Lambda
            logger.info(f"Probando intent: {payload['request']['intent']['name']}")
            response = self.lambda_client.invoke(
                FunctionName=self.function_name,
                Payload=json.dumps(payload)
            )
            
            # Procesar respuesta
            response_payload = json.loads(response['Payload'].read())
            logger.info(f"Respuesta recibida: {json.dumps(response_payload, indent=2)}")
            
            # Verificar formato básico
            if not isinstance(response_payload, dict):
                raise ValueError(f"Respuesta no es un diccionario: {response_payload}")
            
            if 'response' not in response_payload:
                raise ValueError(f"Falta 'response' en la respuesta: {response_payload}")
            
            if 'outputSpeech' not in response_payload['response']:
                raise ValueError(f"Falta 'outputSpeech' en response: {response_payload['response']}")
            
            # Si llegamos aquí, la respuesta tiene el formato correcto
            result = {
                'intent': payload['request']['intent']['name'],
                'slots': payload['request']['intent'].get('slots', {}),
                'response': response_payload,
                'status': 'PASS',
                'timestamp': datetime.now().isoformat()
            }
            logger.info(f"✅ Intent {result['intent']} pasó la prueba")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                'intent': payload_file,
                'status': 'FAIL',
                'error': str(e),
                'raw_response': response_payload if 'response_payload' in locals() else None,
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(error_result)
            logger.error(f"❌ Error probando {payload_file}: {str(e)}")
            logger.error(f"Respuesta cruda: {json.dumps(error_result.get('raw_response', 'No disponible'), indent=2)}")
            return error_result

    def run_all_tests(self):
        """Ejecuta todas las pruebas de integración"""
        logger.info("🚀 Iniciando pruebas de integración de Alexa")
        
        # Probar cada payload en el directorio
        for filename in os.listdir('tests/payloads'):
            if filename.endswith('_payload.json'):
                self.test_intent(filename)
        
        # Guardar resultados
        results_file = f"tests/results/alexa_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Generar resumen
        summary = {
            'total_tests': len(self.results),
            'passed': len([r for r in self.results if r['status'] == 'PASS']),
            'failed': len([r for r in self.results if r['status'] == 'FAIL'])
        }
        
        logger.info(f"📊 Resumen de pruebas:")
        logger.info(f"   Total: {summary['total_tests']}")
        logger.info(f"   Exitosas: {summary['passed']}")
        logger.info(f"   Fallidas: {summary['failed']}")
        
        return summary

    def verify_dynamodb_updates(self):
        """Verifica que los cambios se reflejen en DynamoDB"""
        dynamodb = boto3.client('dynamodb')
        tables = ['AccessDelegation', 'AuditLog', 'Patients', 'Therapies']
        
        for table in tables:
            try:
                response = dynamodb.scan(
                    TableName=table,
                    Limit=1
                )
                logger.info(f"✅ Tabla {table}: {len(response.get('Items', []))} registros encontrados")
            except Exception as e:
                logger.error(f"❌ Error verificando tabla {table}: {str(e)}")

if __name__ == "__main__":
    # Crear directorios si no existen
    os.makedirs("tests/logs", exist_ok=True)
    os.makedirs("tests/results", exist_ok=True)
    
    # Ejecutar pruebas
    test_runner = AlexaIntegrationTest()
    summary = test_runner.run_all_tests()
    test_runner.verify_dynamodb_updates()
