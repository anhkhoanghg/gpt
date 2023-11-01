import json

class Task:
    def __init__(self, assigned_date = None):

        self.load_attributes()
        self.assigned_day = assigned_date
    def calculate_deadline(self):
        pass
    def load_attributes(self):
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
    def getTaskString(self):
        
        # Generate a task string with placeholders for attributes
        task_string = f"<task><sum>{self.summarize}<cate>{self.category}<prio>{self.priority}<diff>{self.difficulty}<imp>{self.important}<status>{self.status}<exp_min>{self.expected_minute}<totd>{self.time_of_the_day}<spec_time>{self.specific_time}<dow>{self.day_of_week}<day>{self.day}<month>{self.month}<no_date>{self.number_of_date}<no_week>{self.number_of_week}<no_month>{self.number_of_month}</task>"
        
        return task_string
    def __str__(self):
        return self.getTaskString()
task = Task()
print(task)