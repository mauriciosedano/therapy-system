#!/bin/bash

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p tests/{payloads,results,logs}

# Crear archivo generate_test_payloads.py
echo "📝 Creando archivo de generación de payloads..."
cat > tests/generate_test_payloads.py << 'EOL'
import json
from datetime import datetime
import uuid
import os

def generate_intent_request(intent_name, slots=None):
    return {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": f"amzn1.echo-api.session.{uuid.uuid4()}",
            "application": {
                "applicationId": "amzn1.ask.skill.028ef8b0-b7cd-45e7-bc9c-08a4a213921e"
            },
            "user": {
                "userId": "amzn1.ask.account.TEST_USER"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": f"amzn1.echo-api.request.{uuid.uuid4()}",
            "timestamp": datetime.utcnow().isoformat(),
            "locale": "es-ES",
            "intent": {
                "name": intent_name,
                "slots": slots or {}
            }
        }
    }

def main():
    # Crear directorio si no existe
    os.makedirs("tests/payloads", exist_ok=True)
    
    # Definir casos de prueba
    test_cases = {
        "DelegarAcceso": {
            "intent": "DelegarAccesoIntent",
            "slots": {
                "Aprendiz": {"name": "Aprendiz", "value": "Ana"},
                "Permiso": {"name": "Permiso", "value": "consultar pacientes"}
            }
        },
        "ConsultarAcciones": {
            "intent": "ConsultarAccionesAprendizIntent",
            "slots": {
                "Aprendiz": {"name": "Aprendiz", "value": "Ana"}
            }
        },
        "RegistrarPaciente": {
            "intent": "RegistrarPacienteIntent",
            "slots": {
                "Nombre": {"name": "Nombre", "value": "María López"},
                "Telefono": {"name": "Telefono", "value": "555-123-4567"}
            }
        },
        "RegistrarTerapia": {
            "intent": "RegistrarTerapiaIntent",
            "slots": {
                "Paciente": {"name": "Paciente", "value": "María López"},
                "TipoTerapia": {"name": "TipoTerapia", "value": "Acupuntura"},
                "Fecha": {"name": "Fecha", "value": datetime.now().strftime("%Y-%m-%d")}
            }
        },
        "ConsultarTerapia": {
            "intent": "ConsultarTerapiaIntent",
            "slots": {
                "Paciente": {"name": "Paciente", "value": "María López"}
            }
        }
    }
    
    # Generar y guardar payloads
    for name, case in test_cases.items():
        payload = generate_intent_request(case["intent"], case["slots"])
        filename = f"tests/payloads/{name}_payload.json"
        with open(filename, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"✅ Generado: {filename}")

if __name__ == "__main__":
    print("🚀 Generando payloads de prueba...")
    main()
    print("✨ Generación completada")
EOL

# Crear archivo test_alexa_integration.py
echo "📝 Creando archivo de pruebas de integración..."
cat > tests/test_alexa_integration.py << 'EOL'
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
        try:
            with open(f"tests/payloads/{payload_file}", 'r') as f:
                payload = json.load(f)
            
            logger.info(f"Probando intent: {payload['request']['intent']['name']}")
            response = self.lambda_client.invoke(
                FunctionName=self.function_name,
                Payload=json.dumps(payload)
            )
            
            response_payload = json.loads(response['Payload'].read())
            
            if 'response' in response_payload and 'outputSpeech' in response_payload['response']:
                result = {
                    'intent': payload['request']['intent']['name'],
                    'slots': payload['request']['intent'].get('slots', {}),
                    'response_text': response_payload['response']['outputSpeech']['text'],
                    'status': 'PASS',
                    'timestamp': datetime.now().isoformat()
                }
                logger.info(f"✅ Intent {result['intent']} respondió: {result['response_text']}")
            else:
                result = {
                    'intent': payload['request']['intent']['name'],
                    'status': 'FAIL',
                    'error': 'Formato de respuesta inválido',
                    'timestamp': datetime.now().isoformat()
                }
                logger.error(f"❌ Intent {result['intent']} falló: Formato de respuesta inválido")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                'intent': payload_file,
                'status': 'FAIL',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(error_result)
            logger.error(f"❌ Error probando {payload_file}: {str(e)}")
            return error_result

    def run_all_tests(self):
        logger.info("🚀 Iniciando pruebas de integración de Alexa")
        
        for filename in os.listdir('tests/payloads'):
            if filename.endswith('_payload.json'):
                self.test_intent(filename)
        
        results_file = f"tests/results/alexa_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"✨ Pruebas completadas. Resultados guardados en {results_file}")
        
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
    os.makedirs("tests/logs", exist_ok=True)
    os.makedirs("tests/results", exist_ok=True)
    
    test_runner = AlexaIntegrationTest()
    summary = test_runner.run_all_tests()
    test_runner.verify_dynamodb_updates()
EOL

# Dar permisos de ejecución
chmod +x run-complete-tests.sh

echo "✅ Estructura de pruebas creada exitosamente"
echo "🚀 Ahora puedes ejecutar: ./run-complete-tests.sh"
