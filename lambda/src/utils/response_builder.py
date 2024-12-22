class ConstructorRespuesta:
    def construir_respuesta(self, texto_respuesta, titulo_tarjeta=None, finalizar_sesion=False):
        """
        Construye una respuesta unificada para Alexa.
        """
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": texto_respuesta
                },
                "shouldEndSession": finalizar_sesion,
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "¿Hay algo más en lo que pueda ayudarte?"
                    }
                }
            }
        }
        
        if titulo_tarjeta:
            response["response"]["card"] = {
                "type": "Simple",
                "title": titulo_tarjeta,
                "content": texto_respuesta
            }
        
        return response

    def construir_error(self, mensaje_error):
        """
        Construye una respuesta de error unificada.
        """
        return self.construir_respuesta(
            texto_respuesta=mensaje_error,
            titulo_tarjeta="Error"
        )

# Para mantener compatibilidad con el código existente
constructor_respuesta = ConstructorRespuesta()

def build_alexa_response(speech_text, card_title=None, should_end_session=False):
    """Función legacy para mantener compatibilidad."""
    return constructor_respuesta.construir_respuesta(
        texto_respuesta=speech_text,
        titulo_tarjeta=card_title,
        finalizar_sesion=should_end_session
    )

def build_error_response(error_message):
    """Función legacy para mantener compatibilidad."""
    return constructor_respuesta.construir_error(error_message)
