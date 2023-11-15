# chinh token
from torch.utils.data import Dataset
import json

# class DailyTaskData(Dataset):
#     def __init__(self, path:str, tokenizer):
#         self.data = json.load(open(path, "r"))
#         self.tokenizer = tokenizer

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         entry = self.data[idx]
#         prompt = entry['prompt']
#         result_str = entry['result']
        
#         # Add start and end of string tokens to the prompt and result strings
#         prompt = "<startofstring><startofprompt>" + prompt + "<endofpromt><endofstring>"

#         result_str = "<startofstring><startoftask>" + result_str + "<endoftask><endofstring>"
#         input_encoded = self.tokenizer(prompt, max_length=100, truncation=True, padding="max_length", return_tensors="pt")
#         output_encoded = self.tokenizer(result_str, max_length=100, truncation=True, padding="max_length", return_tensors="pt")

#         input_ids = input_encoded['input_ids']
#         attention_mask = input_encoded['attention_mask']
#         labels = output_encoded['input_ids']

#         return (input_ids, attention_mask, labels)

#     def _parse_result_string(self, result_str):
#         result_dict = {}
#         parts = result_str.split("<")
#         for part in parts[1:]:
#             key, value = part.split(">")
#             result_dict[key] = value
#         return result_dict

#     def _create_result_string(self, result_dict):
#         result_str = ""
#         for key, value in result_dict.items():
#             result_str += f"<{key}>{value}"
#         return result_str
    
class PromptResultMergedDataset(Dataset):
    def __init__(self, path:str, tokenizer):
        self.data = json.load(open(path, "r"))
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entry = self.data[idx]
        prompt = entry['input']
        target = entry['target']
        merge = "<s>"+ "<prompt>" + prompt + "</prompt>" +  target +  "</s>"
        # Encode the prompt
        input_encoding = self.tokenizer(
            prompt,
            max_length=50,  # Adjust as needed
            return_tensors="pt",
            truncation=True
        )

        # Encode the target
        target_encoding = self.tokenizer(
            target,
            max_length=50,  # Adjust as needed
            return_tensors="pt",
            truncation=True
        )
        # Encode the target
        merge_encoding = self.tokenizer(
            merge,
            max_length=50,  # Adjust as needed
            return_tensors="pt",
            truncation=True
        )
        input_ids = input_encoding['input_ids']
        attention_mask = input_encoding['attention_mask']
        labels = target_encoding['input_ids']  # Use 'input_ids' for language modeling
        merge_ids = merge_encoding['input_ids']
        attention_mask = merge_encoding['attention_mask']
        return {
            "input_ids": merge_ids,
            # "attention_mask": attention_mask,
            # "labels": target
        }


class DailyTaskDataset(Dataset):
    def __init__(self, target_texts: list[str], tokenizer):
        self.data = target_texts
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entry = self.data[idx]
        entry = "<s>" + entry + "</s>"
        # Encode the target
        encoding = self.tokenizer(
            entry,
            max_length=50,  # Adjust as needed
            return_tensors="pt",
            truncation=True
        )

        input_ids = encoding['input_ids']  # Use 'input_ids' for language modeling
        attention_mask = encoding['attention_mask']
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
