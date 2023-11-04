import re
import datetime
import datetime
from dateutil.relativedelta import relativedelta


class Task:
    def __init__(self, sum=None, totd=None, spec_time=None, prio=None, status=None, cate=None,
                 diff=None, imp=None, exp_min=None, dow=None, day=None, month=None,
                 no_date=None, no_week=None, no_month=None, assigned_day=None, id = None):
        
        self.tag_order = ['sum', 'cate', 'prio', 'diff', 'imp', 'status', 'exp_min', 'totd', 'spec_time', 'dow', 'day', 'month', 'no_date', 'no_week', 'no_month']
        #self.short_to_long = {
            #'sum': 'summary', 'totd': 'time_of_day', 'spec_time': 'specific_time',
            #'prio': 'priority', 'status': 'status', 'cate': 'category',
            #'diff': 'difficulty', 'imp': 'importance', 'exp_min': 'expected_minutes',
            #'dow': 'day_of_week', 'day': 'day', 'month': 'month',
            #'no_date': 'number_of_date', 'no_week': 'number_of_week', 'no_month': 'number_of_month'
        #}
        self.short_to_long = {
            'prio': 'priority', 'exp_min': 'expected_minutes',
            'deadline' : 'deadline', 'remain_time' : 'remain_time',
        }
        self.id = id
        self.summary = sum
        self.time_of_day = totd
        self.specific_time = spec_time
        self.priority = prio
        self.status = status
        self.category = cate
        self.difficulty = diff
        self.importance = imp
        self.expected_minutes = exp_min
        self.day_of_week = dow
        self.day = day
        self.month = month
        self.number_of_date = no_date
        self.number_of_week = no_week
        self.number_of_month = no_month
        self.assigned_day = assigned_day
        self.deadline_indicator()
        self.calc_remain_time()

    def calc_remain_time(self):
        self.remain_time = self.deadline - datetime.datetime.now()

    def deadline_indicator(self):

        if self.category == "daily":
            self.deadline = None
            exit()

        current_datetime = self.assigned_day

        if self.number_of_date != None:
            self.deadline = current_datetime + datetime.timedelta(days=self.number_of_date + 1)

        if self.number_of_week != None:
            self.deadline = current_datetime + datetime.timedelta(weeks=self.number_of_week + 1)

        if self.number_of_month != None:
            # Get he current date and time
            # Add one month to the current date and time
            self.deadline = current_datetime + relativedelta(months=self.number_of_month + 1)

        if self.specific_time != None:
            time_obj = datetime.datetime.strptime(self.specific_time, "%H:%M:%S").time()
            # Combine the current date with the parsed time to create a datetime object
            self.deadline = datetime.datetime.combine(self.deadline, time_obj)
        else:
            t = None
            if self.time_of_day == 0:
                t = "0:00:00"
            elif self.time_of_day == 1:
                t = "4:00:00"
            elif self.time_of_day == 2:
                t = "8:00:00"
            elif self.time_of_day == 3:
                t = "12:00:00"
            elif self.time_of_day == 4:
                t = "16:00:00"
            elif self.time_of_day == 5:
                t = "20:00:00"
            
            time_obj = datetime.datetime.strptime(t, "%H:%M:%S").time()
            # Combine the current date with the parsed time to create a datetime object
            self.deadline = datetime.datetime.combine(self.deadline, time_obj)



    def __str__(self):
        attributes_str = f"id: {self.id}, " + ', '.join([f"{self.short_to_long[attr]}: {getattr(self, self.short_to_long[attr])}" for attr in self.short_to_long])
        return f"| {attributes_str} |"

class TasksManager:
    def __init__(self):
        self.tasks = []

        # Collect existing IDs from tasks
        #self.existing_ids = {task.id for task in self.tasks}
        #for target_text in target_texts:
            

    def add_task(self, target_text):
            task_attrs = self.extract_attributes(target_text)
            new_id = len(self.tasks) + 1
            task = Task(**task_attrs, assigned_day=datetime.datetime(2023, 9, 11), id=new_id)
            self.tasks.append(task)
    
    @staticmethod
    def extract_attributes(target_text):
        # Initialize an empty dictionary to hold attributes
        attributes = {}
            
        # Define regular expressions for each tag
        tag_patterns = {
            "sum": r"<sum>(.*?)<|<sum>(.*?)$",
            "totd": r"<totd>(.*?)<|<totd>(.*?)$",
            "spec_time": r"<spec_time>(.*?)<|<spec_time>(.*?)$",
            "prio": r"<prio>(.*?)<|<prio>(.*?)$",
            "status": r"<status>(.*?)<|<status>(.*?)$",
            "cate": r"<cate>(.*?)<|<cate>(.*?)$",
            "diff": r"<diff>(.*?)<|<diff>(.*?)$",
            "imp": r"<imp>(.*?)<|<imp>(.*?)$",
            "exp_min": r"<exp_min>(.*?)<|<exp_min>(.*?)$",
            "dow": r"<dow>(.*?)<|<dow>(.*?)$",
            "day": r"<day>(.*?)<|<day>(.*?)$",
            "month": r"<month>(.*?)<|<month>(.*?)$",
            "no_date": r"<no_date>(.*?)<|<no_date>(.*?)$",
            "no_week": r"<no_week>(.*?)<|<no_week>(.*?)$",
            "no_month": r"<no_month>(.*?)<|<no_month>(.*?)$"
        }

        # Iterate through each tag and extract the corresponding value
        for tag, pattern in tag_patterns.items():
            match = re.search(pattern, target_text)
            if match:
                value = match.group(1) or match.group(2)
                maybe_null_value = value.strip().lower()
                if maybe_null_value in ["null", "none", ""]:
                    attributes[tag] = None
                elif tag in ["prio", "diff", "imp", "status", "exp_min",
                            "totd", "dow", "day", "month", "no_date", "no_week", "no_month"]:
                    try:
                        attributes[tag] = int(value)
                    except ValueError:
                        print(f"Error converting {tag} value '{value}' to int. Skipping.")
                else:
                    attributes[tag] = value
            else:
                attributes[tag] = None
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
    
#class TaskManager:
    #def __init__(self):
        #self.tasks = []
    
    #def create_task_objects(self, target_texts, id_string):
        #id_number = 1
        
        #try:
            #id_number = int(id_string)
        #except ValueError:
            #raise ValueError("The provided id_string is not in a valid number format.")
        
        #tasks = Tasks(target_texts)
        
        #for task in tasks:
            #task.id = id_number
            #id_number += 1
        
        #self.tasks.extend(tasks)
    
    #def get_task_by_id(self, task_id):
        #for task in self.tasks:
            #if task.id == task_id:
                #return task
        #return None