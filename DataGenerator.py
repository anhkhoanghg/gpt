import os
import json
import random
class TaskGenerator():
    def __init__(self):
        self.pathToCoreData = "./data/activities"
        self.pathToStructure = "./data/structure"
        
        self.coreData = self.loadCoreData()
        self.reminder_prefix, self.description_prefix = self.loadPrefix()
        self.conjunction = self.loadConjunction()
        self.preposition = self.loadPreposition() 
        self.combinationMapping = {
            "subject": "s",
            "verb": "v",
            "object": "o",
            "gerund": "g",
            "adverb": "adv",
            "adjective": "adj",
            "noun_phrase": "np",
            "verb_phrase": "vp",
            "reminder-prefix": "r-pre",
            "description-prefix": "d-pre",
            "activities": "act",
            "hour": "h",
            "dayOfWeek": "dow",
            "day": "day",
            "month": "month",
            "preposition": "prep",
            "conjunction": "conj"
        }

        self.combination = self.loadCombination()


    def loadCoreData(self):
        json_data = {}
        for filename in os.listdir(self.pathToCoreData):
            if filename.endswith(".json"):
                with open(os.path.join(self.pathToCoreData, filename), "r") as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        json_data.update(data)
        return json_data
    def loadPrefix(self):

        with open(f"{self.pathToStructure}/pre-fix.json", "r") as json_file:
            data = json.load(json_file)
            reminder_prefix = data["reminder-prefix"]
            description_prefix = data["description-prefix"]
        return reminder_prefix, description_prefix
    def loadConjunction(self):
        conjunctions = []

        with open(f"{self.pathToStructure}/conjunction.json", "r") as json_file:
            data = json.load(json_file)
            conjunctions = data.get("conjunctions", [])

        return conjunctions
    
    def loadPreposition(self):
        preposition = []

        with open(f"{self.pathToStructure}/preposition.json", "r") as json_file:
            data = json.load(json_file)
            preposition = data.get("preposition", [])

        return preposition  
    def loadCombination(self):
        combinations_list = []

        with open(f"{self.pathToStructure}/combination.json", "r") as json_file:
            data = json.load(json_file)
            combinations = data.get("combinations", [])

            for combo in combinations:
                combination = combo.get("combination", [])
                combinations_list.append(combination)

        return combinations_list


    def countQuantityOfEachKeys(self):
        for key, sub_array in self.coreData.items():
            count = len(sub_array)
            print(f"Key: {key}, Number of elements: {count}")
    
    def generateTask(self):
        data = []
        for comb in self.combination:
            sentences = ""
            for element in comb:
                # You need to check if comb is a key in the prefix dictionary.
                if element == "r-pre":
                    prefix = self.get_random_prefix("reminder-prefix")
                else:
                    if element == "d-pre":
                        prefix = self.get_random_prefix("description-prefix")
                    if prefix:
                        sentences += prefix
            # You can add more conditions for other combinations here if needed.

            # Append the generated sentence to the data list.
            data.append(sentences)

    def get_random_prefix(self, category):
        if category == "reminder-prefix":
            return random.choice(self.reminder_prefix)
        else:
            return random.choice(self.description_prefix)

gen = TaskGenerator()
gen.generateTask()