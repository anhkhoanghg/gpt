from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import json
import re


def loadTagToken(token_annotation_path):
    listToken = []
    with open(token_annotation_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        level_2_tokens = data["level_2"]["token"]
        level_3_tokens = data["level_3"]["3.1"]["token"]
        for i in range(len(level_2_tokens)):
            listToken.append(level_2_tokens[i]["value"])
        for i in range(len(level_3_tokens)):
            listToken.append(level_3_tokens[i]["value"])
    
    return listToken

custom_tokens = loadTagToken('./token_annotation.json')

special_tokens = {
    "pad_token": "<pad>",
    "bos_token": "<s>",
    "eos_token": "</s>",
    "additional_special_tokens": custom_tokens
}

# Load tokenizer with custom vocabulary and tokens
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens(special_tokens)

# Load GPT-2 model
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))

# Load trained model state
model.load_state_dict(torch.load("./model/output/checkpoint-1812600/pytorch_model.bin", map_location=torch.device('cuda')))
# model.load_state_dict(torch.load("./checkpoint-650/pytorch_model.bin", map_location=torch.device('cuda')))
model.eval()


def infer(entry, max_length):
    prompt = entry["prompt"]
    input_text = f"<s><prompt>{prompt}</prompt>"
    input_encoded = tokenizer(input_text, max_length=200, truncation=False, return_tensors="pt")
    input_ids = input_encoded['input_ids'].to(device)  # Move to the appropriate device
    attention_mask = input_encoded['attention_mask'].to(device)  # Move to the appropriate device
    
    # Generate text with temperature and top-k sampling
    temperature = 0.2  # Adjust this value
    top_k = 50  # Adjust this value
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
    )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=False)  # Skip special tokens
    
    return generated_text

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

input_entry = {
    "prompt": "remind me to go to school at 7 am",
}

max_length = 80  # Adjust this value
def cutString(text):
        pattern = re.compile(r'<s>(.*?)</s>')

        # Use findall to get all matches
        matches = re.search(pattern, text)

        if matches:
            content = matches.group(1)
            return content
        else:
            print("No match found.")
            return 0
response = infer(input_entry, max_length)
help = cutString(response)
print(help)
def extract_tag_value(target_text):
    attributes = {}
        
    # Define regular expressions for each tag
    tag_patterns = {
        "summarize": r"<sum>(.*?)<|<sum>(.*?)$",
        "time_of_the_day": r"<totd>(.*?)<|<totd>(.*?)$",
        "specific_time": r"<spec_time>(.*?)<|<spec_time>(.*?)$",
        "priority": r"<prio>(.*?)<|<prio>(.*?)$",
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
sum_value = extract_tag_value(help)    
print(sum_value)    


