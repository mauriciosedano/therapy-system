import boto3
import json
import logging
from datetime import datetime, timedelta

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TestScenarios')

class TestScenarios:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.logs = boto3.client('logs')
        self.test_results = []

    def run_all_tests(self):
        """Ejecuta todas las pruebas y registra los resultados"""
        tests = [
            self.test_delegation_table,
            self.test_audit_table,
            self.test_patient_lookup,
            self.test_therapy_registration,
            self.test_access_verification
        ]

        for test in tests:
            try:
                test()
                self.test_results.append({
                    'test': test.__name__,
                    'status': 'PASS',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                self.test_results.append({
                    'test': test.__name__,
                    'status': 'FAIL',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                logger.error(f"Error en {test.__name__}: {str(e)}")

        self.save_results()

    def test_delegation_table(self):
        """Prueba la tabla de delegación de accesos"""
        logger.info("Probando tabla AccessDelegation...")
        
        # Insertar delegación de prueba
        delegation_id = f"D{int(datetime.now().timestamp())}"
        try:
            self.dynamodb.put_item(
                TableName='AccessDelegation',
                Item={
                    'DelegationID': {'S': delegation_id},
                    'MasterID': {'S': 'TEST_MASTER'},
                    'ApprenticeID': {'S': 'TEST_APPRENTICE'},
                    'Permissions': {'SS': ['consultar_pacientes']},
                    'ExpirationDate': {'S': (datetime.now() + timedelta(days=1)).isoformat()},
                    'Status': {'S': 'ACTIVE'}
                }
            )
            
            # Verificar inserción
            response = self.dynamodb.get_item(
                TableName='AccessDelegation',
                Key={'DelegationID': {'S': delegation_id}}
            )
            
            if 'Item' not in response:
                raise Exception("Delegación no encontrada después de inserción")
                
            logger.info("✅ Prueba de tabla AccessDelegation exitosa")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de AccessDelegation: {str(e)}")
            raise

    def test_audit_table(self):
        """Prueba la tabla de auditoría"""
        logger.info("Probando tabla AuditLog...")
        
        # Insertar entrada de auditoría de prueba
        audit_id = f"A{int(datetime.now().timestamp())}"
        try:
            self.dynamodb.put_item(
                TableName='AuditLog',
                Item={
                    'AuditID': {'S': audit_id},
                    'ActionType': {'S': 'TEST_ACTION'},
                    'PerformedBy': {'S': 'TEST_USER'},
                    'Timestamp': {'S': datetime.now().isoformat()},
                    'Details': {'S': json.dumps({'test': 'data'})}
                }
            )
            
            # Verificar inserción
            response = self.dynamodb.get_item(
                TableName='AuditLog',
                Key={'AuditID': {'S': audit_id}}
            )
            
            if 'Item' not in response:
                raise Exception("Entrada de auditoría no encontrada después de inserción")
                
            logger.info("✅ Prueba de tabla AuditLog exitosa")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de AuditLog: {str(e)}")
            raise

    def test_patient_lookup(self):
        """Prueba la búsqueda de pacientes"""
        logger.info("Probando búsqueda de pacientes...")
        
        try:
            # Buscar en la tabla de pacientes
            response = self.dynamodb.scan(
                TableName='Patients',
                Limit=1
            )
            
            logger.info(f"Encontrados {len(response.get('Items', []))} pacientes")
            logger.info("✅ Prueba de búsqueda de pacientes exitosa")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de búsqueda de pacientes: {str(e)}")
            raise

    def test_therapy_registration(self):
        """Prueba el registro de terapias"""
        logger.info("Probando registro de terapias...")
        
        therapy_id = f"T{int(datetime.now().timestamp())}"
        try:
            self.dynamodb.put_item(
                TableName='Therapies',
                Item={
                    'TherapyID': {'S': therapy_id},
                    'PatientID': {'S': 'TEST_PATIENT'},
                    'TherapyType': {'S': 'TEST_THERAPY'},
                    'Date': {'S': datetime.now().date().isoformat()},
                    'Timestamp': {'S': datetime.now().isoformat()}
                }
            )
            
            logger.info("✅ Prueba de registro de terapias exitosa")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de registro de terapias: {str(e)}")
            raise

    def test_access_verification(self):
        """Prueba la verificación de accesos"""
        logger.info("Probando verificación de accesos...")
        
        try:
            # Verificar delegaciones activas
            response = self.dynamodb.query(
                TableName='AccessDelegation',
                IndexName='ApprenticeIndex',
                KeyConditionExpression='ApprenticeID = :aid',
                ExpressionAttributeValues={
                    ':aid': {'S': 'TEST_APPRENTICE'}
                }
            )
            
            logger.info(f"Encontradas {len(response.get('Items', []))} delegaciones")
            logger.info("✅ Prueba de verificación de accesos exitosa")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de verificación de accesos: {str(e)}")
            raise

    def save_results(self):
        """Guarda los resultados de las pruebas"""
        filename = f"tests/results/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        logger.info(f"Resultados guardados en {filename}")

if __name__ == "__main__":
    # Crear directorio de resultados si no existe
    import os
    os.makedirs("tests/results", exist_ok=True)
    
    # Ejecutar pruebas
    test_runner = TestScenarios()
    test_runner.run_all_tests()
