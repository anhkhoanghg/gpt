import os
import json
import random
from task import Task


class TaskGenerator():
    def __init__(self):
        self.pathToCoreDataDir_v = "./data/activities-verbs"
        self.pathToCoreDataDir_n = "./data/activities-nouns"

        self.pathToStructureDir = "./data/structure"
        self.token_annotation_path = "./token_annotation.json"
        self.coreData_v = self.loadCoreData(self.pathToCoreDataDir_v)
        self.coreData_n = self.loadCoreData(self.pathToCoreDataDir_n)
        self.reminder_prefix, self.description_prefix = self.loadPrefix()
        self.conjunction = self.loadConjunction()
        self.preposition = self.loadPreposition()
        # self.priority_values, self.difficulty, self.important, self.status_values, self.tod_values, self.dow_values, self.month_values = self.loadTokenAnnotation()
        
        self.category_values, self.priority_values, _, self.important, self.status_values, self.tod_values, self.dow_values, self.month_values = self.loadTokenAnnotation()

        self.elementMapping = {
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
            "timeOfDay": "tod",
            "dayOfWeek": "dow",
            "day": "day",
            "month": "month",
            "no_date": "no_date",
            "no_week": "no_week",
            "no_month": "no_month",
            "preposition": "prep",
            "conjunction": "conj"
        }

        self.combination = self.loadCombination()

    def loadCoreData(self, path):
        json_data = {}

        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(os.path.join(path, filename), "r") as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        json_data.update(data)
        return json_data
    
    def loadPrefix(self):

        with open(f"{self.pathToStructureDir}/pre-fix.json", "r") as json_file:
            data = json.load(json_file)
            reminder_prefix = data["reminder-prefix"]
            description_prefix = data["description-prefix"]
        return reminder_prefix, description_prefix

    def loadConjunction(self):
        conjunctions = []

        with open(f"{self.pathToStructureDir}/conjunction.json", "r") as json_file:
            data = json.load(json_file)
            conjunctions = data.get("conjunctions", [])

        return conjunctions

    def loadPreposition(self):
        preposition = []

        with open(f"{self.pathToStructureDir}/preposition.json", "r") as json_file:
            data = json.load(json_file)
            preposition = data.get("preposition", [])

        return preposition

    def loadCombination(self):
        combinations_list = []

        with open(f"{self.pathToStructureDir}/combination.json", "r") as json_file:
            data = json.load(json_file)
            combinations = data.get("combinations", [])

            for combo in combinations:
                combination = combo.get("combination", [])
                combinations_list.append(combination)

        return combinations_list

    def countQuantityOfEachKeys(self, dict):
        for key, sub_array in dict.items():
            count = len(sub_array)
            print(f"Key: {key}, Number of elements: {count}")

    def generateTask_v(self):
        data = []
        total_iterations = len(self.coreData_v) * len(self.combination) * len(self.coreData_v)
        current_iteration = 0

        for activityCategory in self.coreData_v:
            for activity in self.coreData_v[activityCategory]:
                
                for comb in self.combination:
                    data_dict = {}
                    task = Task()
                    sentence = ""
                    task.category = activityCategory
                    task.frequency = "single"
                    for index, category in enumerate(comb):
                        if category == "r-pre":
                            prefix = self.get_random_prefix("reminder-prefix")
                            if prefix:
                                sentence += prefix + " "
                        # elif category == "d-pre":
                        #     prefix = self.get_random_prefix(
                        #         "description-prefix")
                        #     if prefix:
                        #         sentence += prefix + " "
                        elif category == "act":  # For "activities"
                            sentence += f"{activity[0]} "
                            task.summarize += f"{activity[0]} "
                            task.expected_minute += f"{activity[2]}"
                            task.important += f"{activity[1]}"
                        elif category == "n":  # For "activities"
                            sentence += f"{activity[0]} "
                            task.summarize += f"{activity[0]} "
                        elif category == "h":
                            label, time = self.generate_random_time()
                            sentence += time + " "
                            task.summarize += f"{time}"
                            task.specific_time += f"{label}"

                        elif category == "prep":
                            prep = self.randomPreposition(comb)
                            preposition = None
                            if index < (len(comb)-1):
                                next_cate = comb[index + 1]
                                if next_cate == "h":
                                    preposition = prep[0]
                                if next_cate == "dow":
                                    preposition = prep[1]
                                if next_cate == "tod":
                                    preposition = prep[2]
                                if next_cate == "day":
                                    preposition = prep[3]
                                if next_cate == "month":
                                    preposition = prep[4]
                            if preposition is not None:
                                sentence += preposition + " "
                        elif category == "tod":
                            tod = self.get_random_tod()
                            sentence += tod + " "

                            task.time_of_the_day += f"{tod}"
                        elif category == "dow":
                            dow = self.get_random_dow()
                            sentence += dow + " "
                            task.day_of_week += f"{dow}"
                        elif category == "day":
                            day, ordinal_day = self.get_random_day_with_word()
                            sentence += str(day) + " "

                            task.day += f"{day}"
                        elif category == "month":
                            month, value = self.get_random_month()
                            sentence += str(month) + " "
                            task.month += f"{month}"
                        elif category == "no_date":
                            value, string = self.get_random_num_of_date()
                            sentence += string + " "
                            task.number_of_date = value
                        elif category == "no_week":
                            value, string = self.get_random_num_of_week()
                            sentence += string + " "
                            task.number_of_week = value   
                        elif category == "no_month":
                            value, string = self.get_random_num_of_month()
                            sentence += string + " "
                            task.number_of_month = value  
                        elif category == "daily":
                            string, timer = self.get_random_daily()
                            sentence += string
                            task.daily = timer
                            task.frequency = 'daily'
                        elif category == "weekly":
                            string, n_dow = self.get_random_weekly()
                            sentence += string
                            task.weekly = n_dow
                            task.frequency = 'weekly'
                            
                    data_dict["input"] = sentence
                    data_dict["target"] = task.getTaskString()
                    data.append(data_dict)

                    current_iteration += 1
                    progress = (current_iteration / total_iterations) * 100
                    print(f"Progress: {progress:.2f}%")

        outputDir = "./data/prompt-target/full_data.json"
        with open(outputDir, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f'Data verbs has been written to {outputDir}')

    def generateTask_n(self):
        data = []
        total_iterations = len(self.coreData_n) * len(self.combination) * len(self.coreData_n)
        current_iteration = 0

        for activityCategory in self.coreData_n:
            for activity in self.coreData_n[activityCategory]:

                for comb in self.combination:
                    data_dict = {}
                    task = Task()
                    sentence = ""
                    task.category = activityCategory
                    task.frequency = "single"
                    for index, category in enumerate(comb):
                        # if category == "r-pre":
                        #     prefix = self.get_random_prefix("reminder-prefix")
                        #     if prefix:
                        #         sentence += prefix + " "
                        if category == "r-pre":
                            prefix = self.get_random_prefix(
                                "description-prefix")
                            if prefix:
                                sentence += prefix + " "
                        elif category == "act":  # For "activities"
                            sentence += f"{activity[0]} "
                            task.summarize += f"{activity[0]} "
                            task.expected_minute += f"{activity[2]}"
                            task.important += f"{activity[1]}"
                        elif category == "n":  # For "activities"
                            sentence += f"{activity[0]} "
                            task.summarize += f"{activity[0]} "
                        elif category == "h":
                            label, time = self.generate_random_time()
                            sentence += time + " "
                            task.summarize += f"{time}"
                            task.specific_time += f"{label}"

                        elif category == "prep":
                            prep = self.randomPreposition(comb)
                            preposition = None
                            if index < (len(comb) - 1):
                                next_cate = comb[index + 1]
                                if next_cate == "h":
                                    preposition = prep[0]
                                if next_cate == "dow":
                                    preposition = prep[1]
                                if next_cate == "tod":
                                    preposition = prep[2]
                                if next_cate == "day":
                                    preposition = prep[3]
                                if next_cate == "month":
                                    preposition = prep[4]
                            if preposition is not None:
                                sentence += preposition + " "
                        elif category == "tod":
                            tod = self.get_random_tod()
                            sentence += tod + " "

                            task.time_of_the_day += f"{tod}"
                        elif category == "dow":
                            dow = self.get_random_dow()
                            sentence += dow + " "
                            task.day_of_week += f"{dow}"
                        elif category == "day":
                            day, ordinal_day = self.get_random_day_with_word()
                            sentence += str(day) + " "

                            task.day += f"{day}"
                        elif category == "month":
                            month, value = self.get_random_month()
                            sentence += str(month) + " "
                            task.month += f"{month}"
                        elif category == "no_date":
                            value, string = self.get_random_num_of_date()
                            sentence += string + " "
                            task.number_of_date = value
                        elif category == "no_week":
                            value, string = self.get_random_num_of_week()
                            sentence += string + " "
                            task.number_of_week = value
                        elif category == "no_month":
                            value, string = self.get_random_num_of_month()
                            sentence += string + " "
                            task.number_of_month = value
                        elif category == "daily":
                            string, timer = self.get_random_daily()
                            sentence += string
                            task.daily = timer
                            task.frequency = 'daily'
                        elif category == "weekly":
                            string, n_dow = self.get_random_weekly()
                            sentence += string
                            task.weekly = n_dow
                            task.frequency = 'weekly'

                    data_dict["input"] = sentence
                    data_dict["target"] = task.getTaskString()
                    data.append(data_dict)

                    current_iteration += 1
                    progress = (current_iteration / total_iterations) * 100
                    print(f"Progress: {progress:.2f}%")

        outputDir = "./data/prompt-target/full_data.json"

        try:
            with open(outputDir, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        existing_data.extend(data)
        with open(outputDir, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)

        print(f'Data nouns has been written to {outputDir}')

    def get_random_day_with_word(self):
        # Generate a random number between 1 and 31
        random_number = random.randint(1, 31)

        # Define a list of ordinal words for the days
        ordinal_words = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh",
                         "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth",
                         "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
                         "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
                         "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth",
                         "twenty-ninth", "thirtieth", "thirty-first"]

        # Get the ordinal word corresponding to the random number
        ordinal_word = ordinal_words[random_number - 1]

        return random_number, ordinal_word

    def get_category_value(self, cate_key):
        for key, value in self.category_values.items():
            if key==cate_key:
                return value
            else:
                return "Others"
    
    def get_random_month(self):
        diction = random.choice(list(self.month_values))
        value = self.month_values[diction]
        
        return diction, value

    def get_random_dow(self):
        return random.choice(list(self.dow_values.values()))

    def get_random_tod(self):
        return random.choice(list(self.tod_values.keys()))
    
    def get_random_num_of_date(self):
        nod = random.randint(1, 30)
        if nod == 1:
            string = "tomorrow"
        else:
            string = "next " + str(nod) + " days"
        return nod, string
    
    def get_random_num_of_week(self):
        now = random.randint(1, 3)   
        if now == 1:
            string = "next " + str(now) + " week" 
        else:
            string = "next " + str(now) + " weeks" 
        return now, string
    
    def get_random_num_of_month(self):
        nom = random.randint(1, 3)   
        if nom == 1:
            string = "next " + str(nom) + " month" 
        else:
            string = "next " + str(nom) + " months" 
        return nom, string
    
    def get_random_daily(self):
        num_tod = random.randint(1, 2)
        daily = []
        string = "at "
        while num_tod>0:
            time_24_hour, speechTime = self.generate_random_time()
            daily.append(time_24_hour)
            if num_tod>1:
                string += speechTime + " and "
            else:
                string += speechTime
                
            num_tod -= 1
        timer = '&'.join(daily)
        string += " for everyday" 
        return string, timer
        
    def get_random_weekly(self):
        num_dow = random.randint(1, 3)
        weekly = []
        string = "for every "
        while num_dow>0:
            dow = self.get_random_dow()
            weekly.append(dow)
            if num_dow>1:
                string += dow + " and "
            else:
                string += dow
            num_dow -=1
        dow = '&'.join(weekly)
        return string, dow
    
    def get_random_preposition(self):
        return random.choice(self.preposition)

    def randomPreposition(self, comb):
        result = []
        preposition = ["about", "at", "by", "before", "after"]
        prep_h, prep_dow, prep_tod, prep_day, prep_month = None, None, None, None, None
        prep_indices = []
        for index, word in enumerate(comb):
            if word == "prep":
                prep_indices.append(index)
        h_index = comb.index("h") if "h" in comb else -1
        tod_index = comb.index("tod") if "tod" in comb else -1
        dow_index = comb.index("dow") if "dow" in comb else -1
        day_index = comb.index("day") if "day" in comb else -1
        month_index = comb.index("month") if "month" in comb else -1
        
                
        if len(prep_indices) >= 1:
            if h_index == -1 or any((h_index-1) == index for index in prep_indices):
                prep_h = random.choice(preposition)
            if dow_index == -1 or any((h_index-1) == index for index in prep_indices):
                prep_dow = "on"
            if tod_index == -1 or any((tod_index-1) == index for index in prep_indices):
                prep_tod = "in"
            if day_index == -1 or any((day_index-1) == index for index in prep_indices):
                prep_day = "on"
            if month_index == -1 or any((month_index-1) == index for index in prep_indices):
                prep_month = "in"
            if month_index != -1 and day_index != -1 and (day_index - month_index == 1) and any((month_index-1) == index for index in prep_indices):
                prep_month = "on"
        prep = [prep_h, prep_dow, prep_tod, prep_day, prep_month]
        for var in prep:
            result.append(var if var is not None else "")
        return result

    def get_random_prefix(self, category):
        if category == "reminder-prefix":
            return random.choice(self.reminder_prefix)
        else:
            return random.choice(self.description_prefix)

    def generate_random_time(self):
        # Randomly choose between 12-hour format and 24-hour format
        format_choice = random.choice(['12-hour', '24-hour'])

        if format_choice == '12-hour':
            # Generate a random hour from 1 to 12
            hour = random.randint(1, 12)

            # Generate a random minute that is a multiple of 5 from 0 to 55
            minute = random.choice(
                [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

            # Choose between 'AM' or 'PM' randomly
            am_pm = random.choice(['AM', 'PM'])

            # Format the time as 'h AM' or 'h PM'
            time_24_hour = f"{hour + 12 if am_pm == 'PM' else hour:02d}:{minute:02d}:00"
            speechTime = f"{hour} {minute:02d} {am_pm}"
        else:
            # Generate a random hour from 0 to 23 for 24-hour format
            hour = random.randint(0, 23)

            # Generate a random minute that is a multiple of 5 from 0 to 55
            minute = random.choice(
                [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

            # Format the time as 'hh:mm'
            time_24_hour = f"{hour:02d}:00:00"
            speechTime = f"{hour} o'clock"

        return time_24_hour, speechTime

    def loadTokenAnnotation(self):

        with open(self.token_annotation_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

        level_3_data = data["level_3"]
        category_values = level_3_data["3.1"]["token"][1]["value-range"]
        priority_values = level_3_data["3.1"]["token"][2]["value-range"]
        difficulty_values = level_3_data["3.1"]["token"][3]["value-range"]
        important_values = level_3_data["3.1"]["token"][4]["value-range"]
        status_values = level_3_data["3.1"]["token"][5]["value-range"]

        totd_values = level_3_data["3.1"]["token"][7]["value-range"]
        dow_values = level_3_data["3.1"]["token"][9]["value-range"]
        month_values = level_3_data["3.1"]["token"][11]["value-range"]
        return category_values, priority_values, difficulty_values, important_values, status_values, totd_values, dow_values, month_values
        


gen = TaskGenerator()
gen.generateTask_v()
gen.generateTask_n()
