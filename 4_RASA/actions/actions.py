# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet

import json
import os


answers = {}
with open(f'{os.path.dirname(os.path.realpath(__file__))}/answers.json', 'r') as f:
    answers = json.load(f)


class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "monitor_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['monitor']
        if tracker.get_slot('connection') != None:
            path = path['connection']
        elif tracker.get_slot('freeze') != None:
            path = path['freeze_problem']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/monitor{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/monitor{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/monitor{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/monitor{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]


class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "network_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['network']
        if tracker.get_slot('latency') != None:
            path = path['latency_problem']
        elif tracker.get_slot('connection') != None:
            path = path['connection']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/network{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/network{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/network{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/network{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]


class ActionRetriever(Action):
    def name(self) -> Text:
        return "fan_retriever"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = answers['fan']

        step = tracker.get_slot('step')
        if step == None:
            step = 0
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/fan{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/fan{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            dispatcher.utter_message(text=path['unresolved_checkout'])

        if step < len(path['steps']):
            buttons = [
                    {"payload" : "/fan{\"_\": \"Fixed\"}", "title" : "Fixed"},
                    {"payload" : "/fan{\"_\": \"_\"}", "title" : "Next Step"},
            ]
            dispatcher.utter_message(text=path['steps'][step], buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]

class ActionRetriever(Action):
    def name(self) -> Text:
        return "battery_retriever"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = answers['battery']

        step = tracker.get_slot('step')
        if step == None:
            step = 0
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/battery{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/battery{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            dispatcher.utter_message(text=path['unresolved_checkout'])

        if step < len(path['steps']):
            buttons = [
                    {"payload" : "/battery{\"_\": \"Fixed\"}", "title" : "Fixed"},
                    {"payload" : "/battery{\"_\": \"_\"}", "title" : "Next Step"},
            ]
            dispatcher.utter_message(text=path['steps'][step], buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]

class ActionRetriever(Action):
    def name(self) -> Text:
        return "overheating_retriever"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = answers['overheating']

        step = tracker.get_slot('step')
        if step == None:
            step = 0
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/overheating{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/overheating{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            dispatcher.utter_message(text=path['unresolved_checkout'])

        if step < len(path['steps']):
            buttons = [
                    {"payload" : "/overheating{\"_\": \"Fixed\"}", "title" : "Fixed"},
                    {"payload" : "/overheating{\"_\": \"_\"}", "title" : "Next Step"},
            ]
            dispatcher.utter_message(text=path['steps'][step], buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]

class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "performance_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['performance']
        if tracker.get_slot('cpu') != None:
            path = path['cpu']
        elif tracker.get_slot('gpu') != None:
            path = path['gpu']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/performance{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/performance{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/performance{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/performance{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]  

class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "filesystem_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['filesystem']
        if tracker.get_slot('restore') != None:
            path = path['restore']
        elif tracker.get_slot('permission') != None:
            path = path['permission']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/filesystem{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/filesystem{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/filesystem{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/filesystem{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]  

class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "harddrive_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['harddrive']
        if tracker.get_slot('format') != None:
            path = path['format']
        elif tracker.get_slot('copy') != None:
            path = path['copy']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/harddrive{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/harddrive{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/harddrive{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/harddrive{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]  

class ActionRetriever(Action):
    # Name of the Action
    def name(self) -> Text:
        return "mouse_keyboard_retriever"
    # Run Action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        path = answers['mouse_keyboard']
        if tracker.get_slot('mouse') != None:
            path = path['mouse']
        elif tracker.get_slot('keyboard') != None:
            path = path['keyboard']
        else:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        step = tracker.get_slot('step')
        if step == None:
            step = 0

        if "Fixed" in tracker.latest_message['text']:
            dispatcher.utter_message(text=path['resolved_checkout'])
            return [AllSlotsReset()]
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/mouse_keyboard{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/mouse_keyboard{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            path = path['unclear']
            buttons = []
            for option in path['options']:
                buttons.append({"payload" : option['path'], "title" : option['name']})
            dispatcher.utter_message(text=path['text'], buttons=buttons)
            return []

        if step < len(path['steps']):
            dispatcher.utter_message(text=path['steps'][step])
            buttons = [
                    {"payload" : "/mouse_keyboard{\"\": \"Fixed\"}", "title" : "Yes"},
                    {"payload" : "/mouse_keyboard{\"\": \"\"}", "title" : "No"},
            ]
            dispatcher.utter_message(text="Did that help you?", buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()] 


class ActionRetriever(Action):
    def name(self) -> Text:
        return "crash_retriever"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        path = answers['crash']

        step = tracker.get_slot('step')
        if step == None:
            step = 0
        if step == 0 and tracker.latest_message['text'] not in ["Right" , "Wrong"]:
            dispatcher.utter_message(text=path['init'])
            buttons = [
                    {"payload" : "/crash{\"\": \"Wrong\"}", "title" : "No"},
                    {"payload" : "/crash{\"\": \"Right\"}", "title" : "Yes"},
            ]
            dispatcher.utter_message(text="Did I identify your problem?", buttons=buttons)

        if step == 0 and tracker.latest_message['text'] not in ["Right"]:
            dispatcher.utter_message(text=path['steps'][step])
        elif step == 0 and tracker.latest_message['text'] not in ["Wrong"]:
            dispatcher.utter_message(text=path['unresolved_checkout'])

        if step < len(path['steps']):
            buttons = [
                    {"payload" : "/crash{\"_\": \"Fixed\"}", "title" : "Fixed"},
                    {"payload" : "/crash{\"_\": \"_\"}", "title" : "Next Step"},
            ]
            dispatcher.utter_message(text=path['steps'][step], buttons=buttons)
            return[SlotSet("step", step+1)]
        else:
            dispatcher.utter_message(text=path['unresolved_checkout'])
        return [AllSlotsReset()]