import json
import re
import datetime
from dateutil.relativedelta import relativedelta
import random



class Task:
    def __init__(self, assigned_date=None, id=None):

        self.init_attributes()
        self.assigned_day = assigned_date # date create task
        # self.deadline_indicator()
        # self.calc_remain_time()
        self.id = id
        self.tod_values = {
            "midnight": 1,
            "morning": 2,
            "noon": 3,
            "evening": 4,
            "night": 5
        }

    def get_random_tod(self):
        return random.choice(list(self.tod_values.keys()))

    def redetermine(self):

        time_pattern = r'^\d{2}:\d{2}:\d{2}$'  # Pattern for "hh:mm:ss" format
        if re.match(time_pattern, self.specific_time):
            hours, minutes, seconds = map(int, self.specific_time.split(":"))

            time_ranges = {
                "midnight": range(0, 6),
                "morning": range(5, 13),
                "noon": range(12, 17),
                "evening": range(16, 21),
                "night": range(20, 25)
            }

            for time_of_day, time_range in time_ranges.items():
                if hours in time_range:
                    self.time_of_the_day = time_of_day
                    break

        else:
            self.time_of_the_day = self.get_random_tod()
        if self.time_of_the_day == '':
            self.time_of_the_day = self.get_random_tod()
    def calculate_deadline(self):
        pass

    def init_attributes(self):
        try:
            # Load the JSON data from the "token_annotation.json" file
            with open(f"./token_annotation.json", "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)

            # Extract the attributes from the JSON data
            attributes = json_data["level_3"]["3.1"]["token"]

            # Create a dictionary with attribute names and empty strings as values
            attribute_dict = {attr["attribute"]: "" for attr in attributes}

            # Update the class's attributes using self.__dict__.update(param)
            self.__dict__.update(attribute_dict)

        except FileNotFoundError:
            print("token_annotation.json file not found!")
        
    def load_attributes(self, value):
        self.__dict__.update(value)
        
    def calc_remain_time(self):
        self.remain_time = self.deadline - datetime.datetime.now()

    def calc_deadline(self):
        self.redetermine()
        if self.category == "daily":
            self.deadline = ''
            exit()

        current_datetime = self.assigned_day
        self.deadline = current_datetime
        if self.number_of_date != '':
            self.deadline +=  datetime.timedelta(days=int(self.number_of_date) + 1)

        if self.number_of_week != '':
            self.deadline += datetime.timedelta(weeks=int(self.number_of_week) + 1)

        if self.number_of_month != '':
            # Get he current date and time
            # Add one month to the current date and time
            self.deadline += relativedelta(months=int(self.number_of_month) + 1)

        if self.specific_time != '':
            time_obj = datetime.datetime.strptime(self.specific_time, "%H:%M:%S").time()
            # Combine the current date with the parsed time to create a datetime object
            self.deadline = datetime.datetime.combine(self.deadline, time_obj)
        else:
            t = ''
            if self.time_of_the_day == 'midnight':
                t = "0:00:00"
            elif self.time_of_the_day == 'morning':
                t = "5:00:00"
            elif self.time_of_the_day == 'noon':
                t = "12:00:00"
            elif self.time_of_the_day == 'evening':
                t = "16:00:00"
            elif self.time_of_the_day == 'night':
                t = "20:00:00"
            
            time_obj = datetime.datetime.strptime(t, "%H:%M:%S").time()
            # Combine the current date with the parsed time to create a datetime object
            self.deadline = datetime.datetime.combine(self.deadline, time_obj)


    def getTaskString(self):
        self.redetermine()
        # Generate a task string with placeholders for attributes
        #task_string = f"<task><sum>{self.summarize}<cate>{self.category}<prio>{self.priority}<diff>{self.difficulty}<imp>{self.important}<freq>{self.frequency}<exp_min>{self.expected_minute}<totd>{self.time_of_the_day}<spec_time>{self.specific_time}<dow>{self.day_of_week}<day>{self.day}<month>{self.month}<no_date>{self.number_of_date}<no_week>{self.number_of_week}<no_month>{self.number_of_month}</task>"
        task_string = f"<task><sum>{self.summarize}<cate>{self.category}<imp>{self.important}<freq>{self.frequency}<exp_min>{self.expected_minute}<totd>{self.time_of_the_day}<spec_time>{self.specific_time}<dow>{self.day_of_week}<day>{self.day}<month>{self.month}<no_date>{self.number_of_date}<no_week>{self.number_of_week}<no_month>{self.number_of_month}<daily>{self.daily}<weekly>{self.weekly}</task>"
        return task_string

    def __str__(self):
        return self.getTaskString()
class TasksManager:
    def __init__(self):
        self.tasks = []

        # Collect existing IDs from tasks
        #self.existing_ids = {task.id for task in self.tasks}
        #for target_text in target_texts:
            

    def add_task(self, target_text):
            task_attrs = self.extract_attributes(target_text)
            new_id = len(self.tasks) + 1
            task = Task(assigned_date=datetime.datetime(2023, 9, 11), id=new_id)
            task.load_attributes(task_attrs)
            task.calc_deadline()
            task.calc_remain_time()
            self.tasks.append(task)
    
    @staticmethod
    def extract_attributes(target_text):
        # Initialize an empty dictionary to hold attributes
        attributes = {}
            
        # Define regular expressions for each tag
        tag_patterns = {
            "summarize": r"<sum>(.*?)<|<sum>(.*?)$",
            "time_of_the_day": r"<totd>(.*?)<|<totd>(.*?)$",
            "specific_time": r"<spec_time>(.*?)<|<spec_time>(.*?)$",
            "priority": r"<prio>(.*?)<|<prio>(.*?)$",
            "frequency": r"<freq>(.*?)<|<freq>(.*?)$",
            "category": r"<cate>(.*?)<|<cate>(.*?)$",
            # "difficulty": r"<diff>(.*?)<|<diff>(.*?)$",
            "important": r"<imp>(.*?)<|<imp>(.*?)$",
            "expected_minute": r"<exp_min>(.*?)<|<exp_min>(.*?)$",
            "day_of_week": r"<dow>(.*?)<|<dow>(.*?)$",
            "day": r"<day>(.*?)<|<day>(.*?)$",
            "month": r"<month>(.*?)<|<month>(.*?)$",
            "number_of_date": r"<no_date>(.*?)<|<no_date>(.*?)$",
            "number_of_week": r"<no_week>(.*?)<|<no_week>(.*?)$",
            "number_of_month": r"<no_month>(.*?)<|<no_month>(.*?)$",
            "daily": r"<daily>(.*?)<|<daily>(.*?)$",
            "weekly": r"<weekly>(.*?)<|<weekly>(.*?)$"
        }

        # Iterate through each tag and extract the corresponding value
        for tag, pattern in tag_patterns.items():
            match = re.search(pattern, target_text)
            if match:
                value = match.group(1) or match.group(2)
                if value != None: 
                    maybe_null_value = value.strip().lower()
                    if maybe_null_value in ["null", "none", ""]:
                        attributes[tag] = ''
                    elif tag in ["prio", "imp", "freq", "exp_min",
                                "totd", "dow", "day", "month", "no_date", "no_week", "no_month",
                                # "diff"
                                ]:
                        try:
                            attributes[tag] = int(value)
                        except ValueError:
                            print(f"Error converting {tag} value '{value}' to int. Skipping.")
                    else:
                        attributes[tag] = value
                else:
                    pass
            else:
                attributes[tag] = ''
        return attributes
    
    def __iter__(self):
        # Define the iterator for the 'tasks' list
        return iter(self.tasks)
    
    def __len__(self):
        return len(self.tasks)
    
    def __getitem__(self, idx):
        return self.tasks[idx]
    def get_next_id(self, existing_ids):
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        return new_id
    def __str__(self):
        task_strings = [f"Task {i+1}: {task}" for i, task in enumerate(self.tasks)]
        return '\n'.join(task_strings)

task = Task()
print(task)
