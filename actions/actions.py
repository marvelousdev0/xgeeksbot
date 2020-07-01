# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from api import career_api

class ActionGreetUser(Action):
    """Revertible mapped action for utter_greet"""

    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_greet", tracker)
        return [UserUtteranceReverted()]


class ActionConfused(Action):

    def name(self) -> Text:
        return "action_respond_confused"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = {
            "type": "text", "data": "We have a comprehensive list of courses. Please refer our [Career Guidance](http://digitalxgeeks.com/careerguidance/) to get more details."}
        dispatcher.utter_message(json_message=message)

        return []


class ActionShowCareerPaths(Action):
    def name(self) -> Text:
        return "action_respond_career_paths"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        career_paths = career_api.getCareerPaths()
        if(career_paths is None):
            dispatcher.utter_message("Sorry I couldn't get career paths")
        else:
            message = {"payload": "paths", "data": career_paths}
            dispatcher.utter_message(json_message=message)

        return []


class ActionTechnologies(Action):
    def name(self) -> Text:
        return "action_respond_technologies"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ return list of technologies """
        message = {
            "type": "text", "data": "List of all technologies as buttons!"
        }
        dispatcher.utter_message(json_message=message)

        return []
