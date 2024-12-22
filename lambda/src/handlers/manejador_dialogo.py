# lambda/src/handlers/manejador_dialogo.py
import logging
from datetime import datetime
from utils.response_builder import constructor_respuesta

logger = logging.getLogger()

class ManejadorDialogo:
    def __init__(self):
        self.remedios_sintomas = {
            "dolor de cabeza": ["Belladonna", "Nux Vomica"],
            "ansiedad": ["Rescue Remedy", "Ignatia"],
            "insomnio": ["Coffea", "Passiflora"],
            "golpes": ["Árnica", "Ruta"],
            "fiebre": ["Belladonna", "Aconitum"]
        }
        
        self.contexto_sesion = {}
    
    def sugerir_remedio(self, event):
        """Maneja ConsultarRemedioIntent"""
        try:
            slots = event['request']['intent']['slots']
            sintoma = slots.get('Sintoma', {}).get('value')
            
            if not sintoma:
                return constructor_respuesta.construir_respuesta(
                    texto_respuesta="¿Para qué síntoma necesitas un remedio?",
                    titulo_tarjeta="Consulta de Remedios"
                )
            
            remedios = self.remedios_sintomas.get(sintoma.lower(), [])
            
            if not remedios:
                return constructor_respuesta.construir_respuesta(
                    texto_respuesta="No tengo una recomendación específica para ese síntoma. "
                                  "¿Te gustaría consultar otros síntomas comunes?",
                    titulo_tarjeta="Remedio no encontrado"
                )
            
            # Guardar contexto para futura referencia
            session_id = event['session']['sessionId']
            self.contexto_sesion[session_id] = {
                'ultimo_sintoma': sintoma,
                'remedios_sugeridos': remedios
            }
            
            respuesta = f"Para {sintoma}, te recomiendo: {', '.join(remedios)}. "
            respuesta += "¿Te gustaría que prepare alguno de estos remedios?"
            
            return constructor_respuesta.construir_respuesta(
                texto_respuesta=respuesta,
                titulo_tarjeta=f"Remedios para {sintoma}"
            )
            
        except Exception as e:
            logger.error("Error sugiriendo remedio: %s", str(e))
            return constructor_respuesta.construir_error(
                "Hubo un error procesando tu consulta. Por favor, intenta de nuevo."
            )
    
    def registrar_formula_contextual(self, event):
        """Registra una fórmula considerando el contexto de la conversación"""
        try:
            slots = event['request']['intent']['slots']
            paciente = slots.get('Paciente', {}).get('value')
            tipo_formula = slots.get('TipoFormula', {}).get('value')
            sintoma = slots.get('Sintoma', {}).get('value')
            
            session_id = event['session']['sessionId']
            contexto = self.contexto_sesion.get(session_id, {})
            
            # Si no tenemos tipo de fórmula pero tenemos un síntoma previo
            if not tipo_formula and contexto.get('ultimo_sintoma'):
                remedios = contexto['remedios_sugeridos']
                if remedios:
                    tipo_formula = remedios[0]  # Usar primera sugerencia
            
            # Construir respuesta contextual
            if paciente and tipo_formula:
                respuesta = f"Registraré {tipo_formula} para {paciente}"
                if sintoma:
                    respuesta += f" para tratar {sintoma}"
                respuesta += ". ¿Confirmas el registro?"
            else:
                respuesta = "Necesito saber para quién es el remedio. ¿Me puedes dar el nombre del paciente?"
            
            return constructor_respuesta.construir_respuesta(
                texto_respuesta=respuesta,
                titulo_tarjeta="Registro de Fórmula"
            )
            
        except Exception as e:
            logger.error("Error en registro contextual: %s", str(e))
            return constructor_respuesta.construir_error(
                "Hubo un error procesando el registro. Por favor, intenta de nuevo."
            )
