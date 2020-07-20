# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import Restarted, SlotSet, AllSlotsReset
from rasa_sdk.events import UserUtteranceReverted

from api.career import career_api


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
            resp_buttons = map(
                lambda value: {'title': value, 'payload': value.lower()}, career_paths["data"])
            message = {"type": "paths",
                       "data": career_paths["data"], "buttons": resp_buttons}
            dispatcher.utter_message(json_message=message)

        return []


class ActionRespondTechnologies(Action):
    def name(self):
        return "action_respond_technologies"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        career_path_slot = str(tracker.get_slot('career_path_slot'))
        career_path_entity = next(
            tracker.get_latest_entity_values('career_path_entity'), None)
        career_path = ""
        if (career_path_entity is None):
            career_path = career_path_slot
        else:
            career_path = career_path_entity
        career_path_details = career_api.getCareerPathDetails(career_path)
        print(career_path_details)
        if(career_path_details is None):
            dispatcher.utter_message("Sorry I couldn't get career path info")
            return []
        else:
            resp_buttons = map(lambda value: {
                               "title": value, "payload": value.lower()}, career_path_details["data"]["tech"])
            message = {"type": "technologies",
                       "data": career_path_details["data"], "buttons": resp_buttons}
            dispatcher.utter_message(json_message=message)
            return [SlotSet("career_path_slot", None)]


class FormActionCareerPath(FormAction):
    def name(self):
        return "form_action_career_path"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["career_path_slot"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"career_path_slot": [self.from_text()]}

    @staticmethod
    def career_path_format() -> List[Text]:
        return ["devops", "Devops", "Machine Learning", "python", "java", "Java"]

    def validate_stock_symbol(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
        career_path_slot = tracker.get_slot("career_path_slot")
        if (career_path_slot is None):
            if value:
                return {"career_path_slot": value}
            else:
                dispatcher.utter_message(text="Please enter career path")
                return {"career_path_slot": None}
        else:
            return {"career_path_slot": value}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []
