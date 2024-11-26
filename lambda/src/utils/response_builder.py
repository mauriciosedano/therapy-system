def build_alexa_response(speech_text, card_title=None, should_end_session=False):
    response = {
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
    
    if card_title:
        response["response"]["card"] = {
            "type": "Simple",
            "title": card_title,
            "content": speech_text
        }
    
    return response

def build_error_response(error_message):
    return build_alexa_response(
        speech_text=error_message,
        card_title="Error"
    )
