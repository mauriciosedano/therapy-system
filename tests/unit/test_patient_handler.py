import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../lambda/src'))
from handlers.patient_handler import PatientHandler
from datetime import datetime

class TestPatientHandler(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.patient_handler = PatientHandler()
        self.mock_dynamo_patcher = patch('handlers.patient_handler.dynamodb')
        self.mock_dynamo = self.mock_dynamo_patcher.start()

    def tearDown(self):
        """Limpieza después de cada prueba."""
        self.mock_dynamo_patcher.stop()

    def test_register_patient_success(self):
        """Prueba el registro exitoso de un paciente."""
        # Configurar el mock de DynamoDB
        self.mock_dynamo.put_item = MagicMock()
        self.mock_dynamo.scan = MagicMock(return_value={'Items': []})

        # Crear request de prueba
        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'},
                    'Telefono': {'value': '1234567890'}
                }
            }
        }

        # Ejecutar la función
        response = self.patient_handler.handle_register_patient(test_request)

        # Verificar respuesta
        self.assertIn('Juan Pérez', response['response']['outputSpeech']['text'])
        self.assertIn('1234567890', response['response']['outputSpeech']['text'])
        self.mock_dynamo.put_item.assert_called_once()

    def test_register_patient_missing_data(self):
        """Prueba el manejo de datos faltantes."""
        # Request sin teléfono
        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'},
                    'Telefono': {}
                }
            }
        }

        response = self.patient_handler.handle_register_patient(test_request)
        self.assertIn('Necesito el nombre y teléfono', 
                     response['response']['outputSpeech']['text'])

    def test_register_patient_similar_exists(self):
        """Prueba la detección de nombres similares."""
        # Configurar mock para retornar un paciente similar
        self.mock_dynamo.scan = MagicMock(return_value={
            'Items': [{
                'Name': {'S': 'Juan Peres'},
                'Phone': {'S': '9876543210'},
                'PatientID': {'S': 'P123'}
            }]
        })

        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'},
                    'Telefono': {'value': '1234567890'}
                }
            }
        }

        response = self.patient_handler.handle_register_patient(test_request)
        self.assertIn('nombres similares', response['response']['outputSpeech']['text'])

    def test_query_patient_found(self):
        """Prueba la búsqueda exitosa de un paciente."""
        self.mock_dynamo.scan = MagicMock(return_value={
            'Items': [{
                'Name': {'S': 'Juan Pérez'},
                'Phone': {'S': '1234567890'},
                'PatientID': {'S': 'P123'}
            }]
        })

        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'}
                }
            }
        }

        response = self.patient_handler.handle_query_patient(test_request)
        self.assertIn('Juan Pérez', response['response']['outputSpeech']['text'])
        self.assertIn('1234567890', response['response']['outputSpeech']['text'])

    def test_query_patient_not_found(self):
        """Prueba la búsqueda de un paciente inexistente."""
        self.mock_dynamo.scan = MagicMock(return_value={'Items': []})

        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'}
                }
            }
        }

        response = self.patient_handler.handle_query_patient(test_request)
        self.assertIn('No encontré ningún paciente', 
                     response['response']['outputSpeech']['text'])

    def test_query_patient_multiple_matches(self):
        """Prueba el manejo de múltiples coincidencias."""
        self.mock_dynamo.scan = MagicMock(return_value={
            'Items': [
                {
                    'Name': {'S': 'Juan Pérez'},
                    'Phone': {'S': '1234567890'},
                    'PatientID': {'S': 'P123'}
                },
                {
                    'Name': {'S': 'Juan Pablo Pérez'},
                    'Phone': {'S': '0987654321'},
                    'PatientID': {'S': 'P124'}
                }
            ]
        })

        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'}
                }
            }
        }

        response = self.patient_handler.handle_query_patient(test_request)
        self.assertIn('varios pacientes similares', 
                     response['response']['outputSpeech']['text'])

    def test_dynamo_error_handling(self):
        """Prueba el manejo de errores de DynamoDB."""
        self.mock_dynamo.put_item.side_effect = Exception("DynamoDB Error")

        test_request = {
            'intent': {
                'slots': {
                    'Nombre': {'value': 'Juan Pérez'},
                    'Telefono': {'value': '1234567890'}
                }
            }
        }

        response = self.patient_handler.handle_register_patient(test_request)
        self.assertIn('error', response['response']['outputSpeech']['text'])

if __name__ == '__main__':
    unittest.main()