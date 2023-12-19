from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import json
import spacy
from datetime import datetime as dt
from datetime import time, timedelta
import parsedatetime as pdt
import re
from modelPred.task import TasksManager
#spacy.cli.download("en_core_web_sm")
class GetDateTime():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def insert_str(self, string, str_to_insert, index):
        return string[:index] + str_to_insert + string[index:]
    
    def getDateTimeinText(self, text):
        doc = self.nlp(text)
        result = ""
        date = ""
        time = ""
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                print(f"Entity: {ent.text}, Label: {ent.label_}")
                if ent.label_ == "DATE":
                    date = self.getRemindTime(ent.text)
                    result = self.insert_str(result, " "+ent.text, len(result))
                elif ent.label_ == "TIME":
                    time = self.getRemindTime(ent.text)
                    result = self.insert_str(result, ent.text , 0)
        return result, date, time
            
    def getRemindTime(self, time_string):
        cal = pdt.Calendar()
        now = dt.now()
        # print("now: %s" % now)
        # print("%s:\t%s" % (time_string, cal.parseDT(time_string, now)[0])) 
        return cal.parseDT(time_string, now)[0]
    
class GetPrediction():
    def __init__(self):
        self.tokenAnnotationPath = './token_annotation.json'
        self.pathtoModel = "D:\KLTN\gpt\modelPred\model\checkpoint-1812600\pytorch_model.bin"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.get_specify_datetime = GetDateTime()
        self.custom_tokens = self.loadTokens()
        self.special_tokens = {
            "pad_token": "<pad>",
            "bos_token": "<s>",
            "eos_token": "<\s>",
            "additional_special_tokens": self.custom_tokens
        }
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        
        self.model = self.loadModel()
        self.model.to(self.device)
        
    
    def loadTokens(self):
        listToken = []
        with open(self.tokenAnnotationPath, 'r', encoding="utf-8") as file:
            data = json.load(file)
            level_2_tokens = data["level_2"]["token"]
            level_3_tokens = data["level_3"]["3.1"]["token"]
            for i in range(len(level_2_tokens)):
                listToken.append(level_2_tokens[i]["value"])
            for i in range(len(level_3_tokens)):
                listToken.append(level_3_tokens[i]["value"])    
        return listToken
    
    def loadModel(self):
        # Load tokenizer with custom vocabulary and tokens
        self.tokenizer.add_special_tokens(self.special_tokens)

        # Load GPT-2 model
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        model.resize_token_embeddings(len(self.tokenizer))

        # Load trained model state
        model.load_state_dict(torch.load(self.pathtoModel, map_location=torch.device(self.device)), strict=False)
        # model.load_state_dict(torch.load("./checkpoint-650/pytorch_model.bin", map_location=torch.device('cuda')))
        model.eval()
        return model
    
    def get_predict_from_model(self, entry, max_length=100):
        prompt = entry
        input_text = f"<s><prompt>{prompt}</prompt>"
        input_encoded = self.tokenizer(input_text, max_length=max_length, truncation=False, return_tensors="pt")
        input_ids = input_encoded['input_ids'].to(self.device)  # Move to the appropriate device
        attention_mask = input_encoded['attention_mask'].to(self.device)  # Move to the appropriate device
        
        # Generate text with temperature and top-k sampling
        temperature = 0.2  # Adjust this value
        top_k = 50  # Adjust this value
        output = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
        )
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=False)  # Skip special tokens
        output_text = self.cutString(generated_text)
        return output_text
    
    def cutString(self, text):
        pattern = re.compile(r'<s>(.*?)</s>')

        # Use findall to get all matches
        matches = re.search(pattern, text)

        if matches:
            content = matches.group(1)
            return content
        else:
            print("No match found.")
            return 0
    
    def extract_tag_value(self, target_text):
        attributes = {}
            
        # Define regular expressions for each tag
        tag_patterns = {
            "summarize": r"<sum>(.*?)<|<sum>(.*?)$",
            "time_of_the_day": r"<totd>(.*?)<|<totd>(.*?)$",
            "specific_time": r"<spec_time>(.*?)<|<spec_time>(.*?)$",
            # "priority": r"<prio>(.*?)<|<prio>(.*?)$",
            "frequency": r"<freq>(.*?)<|<freq>(.*?)$",
            "category": r"<cate>(.*?)<|<cate>(.*?)$",
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

    def predict(self, entry): 
        try:
            text = self.get_predict_from_model(entry)
        except Exception as e:
            excep = "An unexpected error occurred: " + str(e)
            print(excep)
        if text:
            attributes = self.extract_tag_value(text)
            string_dt, date, time = self.get_specify_datetime.getDateTimeinText(entry)     
            print(time)
            print("\n")
            print(date)
            if time != '':      
                attributes["specific_time"] = str(time.time())
            if date != '':
                attributes["day"] =str(date.day)
                attributes["month"] = str(date.month)
            else:
                attributes["day"] =str(time.day)
                attributes["month"] = str(time.month)
        else:
            attributes = []
            attributes["sum"] = entry
            string_dt, date, time = self.get_specify_datetime.getDateTimeinText(entry)        
            print(time)
            print("\n")
            print(date)   
            if time != '':      
                attributes["specific_time"] = str(time.time())
            if date != '':
                attributes["day"] =str(date.day)
                attributes["month"] = str(date.month)
            else:
                attributes["day"] =str(time.day)
                attributes["month"] = str(time.month)
            attributes["sum"] = entry

        return attributes

class OrderingTask():
    def __init__(self) -> None:
        pass

    def add_prio_tag(self, s):
        imp_idx = s.index("<imp>")
        s = s[:imp_idx] + "<prio>" + s[imp_idx:]
        return s

    # sắp xếp task theo priority
    def sort_task(self, task_list):
        return sorted(task_list, key=lambda x: x.priority)


    # Chọn task để làm trong một buổi (trong 5 buổi)
    def task_filter(self, task_in_same_period : list, start_time, end_time):
        # sắp xếp task
        task_in_same_period = self.sort_task(task_in_same_period)

        # task được chọn để làm 
        remain_task = []  

        # task quá deadline và có khả năng làm được trong ngày khác
        filtered_task = []

        for task in task_in_same_period:
            try:
                task_time = int(task.expected_minute)
            except:
                task_time = 60
                
            if start_time + task_time > end_time:
                filtered_task += [task]
                continue
            remain_task += [task]
            start_time += task_time

        return remain_task, filtered_task

    def group_task(self, task_list):
        task_list = sorted(task_list, key=lambda x : x.remain_time)

        # Define the threshold (3 days)
        threshold_days = 3
        # Initialize lists for normal and emergency dates
        normal_tasks = []
        emergency_tasks = []

        # Get the current date and time
        #current_date_time = datetime.now()


        # Iterate through the list of tasks
        for task in task_list:
            # Get the total number of days from the timedelta
            remaining_days = task.remain_time.days

            # Determine whether it's normal or emergency task
            if remaining_days > threshold_days:
                normal_tasks.append(task)
            else:
                emergency_tasks.append(task)

        return normal_tasks, emergency_tasks

    def to_do_list_in_day(self, task_list):
        tasks = [[], [], [], [], []]
        remain_task = [[], [], [],
                    
                        [], []]
        filtered_task = [[], [], [], [], []]
        mapping = { 'midnight':1,
                    'morning':2,
                    'noon':3,
                    'evening':4,
                    'night':5}
        for task in task_list:          
            tasks[mapping[task.time_of_the_day]] += [task]
        
        start_time = [0, 300, 720, 960, 1200, 1200] 
        end_time   = [300, 720, 960, 1200, 1200, 1440]
        custome_delta = [0, 60, 0, 0, 0, 0] 
        for i in range(0, 5):
            remain_task[i], filtered_task[i] = self.task_filter(tasks[i], start_time[i] + custome_delta[i], end_time[i])

        return remain_task, filtered_task

    def select_task_for_a_day(self, tasks):
        normal_tasks, emergency_tasks = self.group_task(tasks)
        remain_task_1, filtered_task_1 = self.to_do_list_in_day(emergency_tasks)
        remain_task_2, filtered_task_2 = self.to_do_list_in_day(normal_tasks)

        remain_task = [[], [], [], [], []]
        filtered_task = [[], [], [], [], []]


        for i in range(0, 5):
            remain_task[i] = remain_task_1[i] + remain_task_2[i]
            filtered_task[i] = filtered_task_1[i] + filtered_task_2[i] 
        
        ret_task = []
        for tasks in filtered_task:
            for task in tasks:
                ret_task += [task]

        return remain_task, ret_task

    def to_hour(self, minutes):
        hours = minutes // 60  # Số giờ là phần nguyên của phép chia
        remainder_minutes = minutes % 60  # Số phút dư
        time_object = time(hours, remainder_minutes)
        return time_object

    def process(self, tasks):
        ret_dict = {}
        start_time = [0, 300, 720, 960, 1200, 1200] 
        custome_delta = [0, 60, 0, 0, 0, 0]
        for i in range(0, 5):
            st = start_time[i] + custome_delta[i]
            for task in tasks[i]:
                ret_dict[str(self.to_hour(st))] = task.id
                try:
                    exp_minute = int(task.expected_minute)
                except:
                    exp_minute = 60
                st += exp_minute

        return ret_dict
    
    def ordering(self, arr):
        for text in arr:
            tasks.add_task(text)
        
        final_dict = {}
        current_date = dt.datetime.now()
        delta = 0
        while len(tasks) != 0:
            remain_task, tasks = self.select_task_for_a_day(tasks)
            task_dict = self.process(remain_task)
            final_dict[str((current_date + timedelta(days=delta)))] = task_dict
            delta += 1
            
        print(final_dict)
        return final_dict
            
# if __name__ == "__main__":
#     pred = GetPrediction()
#     text = "remind me to go to school at 5 am tomorrow"
#     att = pred.predict(text)
#     for i in att:
#         print(att[i])

