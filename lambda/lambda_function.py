# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from datetime import datetime
from epicstore_api import EpicGamesStoreAPI, OfferData
from deep_translator import GoogleTranslator

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bem vindo a skill da Epic Games. Diga o que você precisa."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FreeGamesIntentHandler(AbstractRequestHandler):
    """Handler for Free Epic Games Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FreeGamesIntent")(handler_input)

    def handle(self, handler_input):
        api = EpicGamesStoreAPI()
        promotions = api.get_free_games()
        
        date_format = '%Y-%m-%d'
        
        freeGames = []
        freeGamesDescription = []
        
        for game in promotions['data']['Catalog']['searchStore']['elements']:
            if game.get('promotions') != None:
                if game['promotions'].get('promotionalOffers') != None:
                    if game['promotions']['promotionalOffers'] != []:
                        if(game['title'] != 'Mystery Game'):
                            for promotionalOffer in game['promotions']['promotionalOffers'][0]['promotionalOffers']:
                                if datetime.strptime(promotionalOffer['endDate'][0:10], date_format) > datetime.today() and promotionalOffer['discountSetting']['discountPercentage'] == 0:
                                    freeGames.append(game['title'])
                                    freeGamesDescription.append(GoogleTranslator(source='auto', target='pt').translate(game['description']).replace("\n", " "))
                                
        speak_output = "Os jogos que estão de graça hoje são: " + freeGames[0] + " e " + freeGames[1] + ". " + freeGamesDescription[0] + " " + freeGamesDescription[1]
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class UpcomingFreeGamesIntentHandler(AbstractRequestHandler):
    """Handler for Free Epic Games Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("UpcomingFreeGamesIntent")(handler_input)

    def handle(self, handler_input):
        api = EpicGamesStoreAPI()
        promotions = api.get_free_games()
        
        date_format = '%Y-%m-%d'
        
        upcomingFreeGames = []
        upcomingFreeGamesDescription = []
        
        for game in promotions['data']['Catalog']['searchStore']['elements']:
            if game.get('promotions') != None:
                if game['promotions'].get('upcomingPromotionalOffers') != None:
                    if game['promotions']['upcomingPromotionalOffers'] != []:
                        if(game['title'] != 'Mystery Game'):
                            for upcomingPromotionalOffer in game['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers']:
                                if datetime.strptime(upcomingPromotionalOffer['endDate'][0:10], date_format) > datetime.today() and upcomingPromotionalOffer['discountSetting']['discountPercentage'] == 0:
                                    upcomingFreeGames.append(game['title'])
                                    upcomingFreeGamesDescription.append(GoogleTranslator(source='auto', target='pt').translate(game['description']).replace("\n", " "))
                                
        speak_output = "Os próximos jogos de graça são: " + upcomingFreeGames[0] + " e " + upcomingFreeGames[1] + ". " + upcomingFreeGamesDescription[0] + " " + upcomingFreeGamesDescription[1]
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Como posso te ajudar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Tudo bem, tchau!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, eu não tenho certeza."
        reprompt = "Eu não entendi. Como posso te ajudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Você acionou a " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, eu tive um problema ao executar o que você pediu. Por favor, tente de novo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FreeGamesIntentHandler())
sb.add_request_handler(UpcomingFreeGamesIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()