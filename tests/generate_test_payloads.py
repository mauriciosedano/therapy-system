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
