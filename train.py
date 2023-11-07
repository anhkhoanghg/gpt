from transformers import GPT2LMHeadModel, GPT2Tokenizer
from dataset import PromptResultMergedDataset
from torch.optim import Adam, AdamW
from torch.utils.data import DataLoader
import tqdm
import torch
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
# Example usage
input_entry = {
    "prompt": "Prepare presentation for tomorrow's conference",
}


def train(dataset, model, max_length, temperature):
    training_args = TrainingArguments(
        output_dir="./output",
        num_train_epochs=1000,
        per_device_train_batch_size=1,
        save_steps=10,
        save_total_limit=2,
        overwrite_output_dir=True,
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset
    )

    # Start training
    trainer.train()

    torch.save(model.state_dict(), "model_state.pt")
    print(infer(input_entry, max_length))


def infer(entry, max_length):
    prompt = entry["prompt"]
    input_text = f"<sot><startofprompt>{prompt}<endofpromt>"
    input_encoded = tokenizer(input_text, max_length=100, truncation=True, padding="max_length", return_tensors="pt")
    input_ids = input_encoded['input_ids'].to("cuda")
    attention_mask = input_encoded['attention_mask'].to("cuda")
    
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
    generated_text = tokenizer.decode(output[0], skip_special_tokens=False)
    
    return generated_text

device = "cuda" if torch.cuda.is_available() else "cpu"
custom_tokens = [
    "<prompt>", "</prompt>", "<task>", "</task>", "<sum>", "<cate>", "<prio>", "<diff>",  "<imp>",
    "<freq>", "<exp_min>", "<totd>", "<spec_time>", "<dow>", "<day>", "<month>", "<no_date>", "<no_week>", "<no_month>"
]

special_tokens = {
    "pad_token": "<pad>",
    "bos_token": "<s>",
    "eos_token": "<\s>",
    "additional_special_tokens": custom_tokens
}

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens(special_tokens)

model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))

model = model.to(device)

dailyTaskDataset = PromptResultMergedDataset(
    "./data/single-task-data.json", tokenizer)
dailyTaskDataLoader = DataLoader(dailyTaskDataset, batch_size=64)

model.train()

optim = Adam(model.parameters(), lr=1e-2)

print("training .... ")
temperature = 0.2
max_length = 50
train(dailyTaskDataset, model, max_length, temperature)


#Bùi Đức Nhân
#I need you generate for me 10 of mix type of type 5 data (not repeated, given tasks are not duplicated in this session), below is an example of 5 taks category:
#1. Daily task:
#"input_text" :  Remind me to working out everyday at 8 pm.
#"target_text" : <sot><sum>Working out daily<totd>5<spec_time>20:00:00<prio>5<status>0<cate>daily<diff>4<imp>3<exp_min>90<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>null<eot>

#2.Intra day task
#2.1 No specific time
#"input_text" :  Remind me to remember reading email tonight.
#"target_text" : <sot><sum>Checking email<totd>5<spec_time>null<prio>1<status>0<cate>work<diff>5<imp>1<exp_min>60<dow>null<day>null<month>null<no_date>0<no_week>null<no_month>null<eot>
#2.2 Time specified
#"input_text" :  Remind me to remember reading email at 10pm.
#"target_text" : <sot><sum>Checking email<totd>5<spec_time>22:00:00<prio>1<status>0<cate>work<diff>5<imp>1<exp_min>60<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>null<eot>

#3. Within number of week task
#"input_text" :  Assistant note it down for me to prepare my cv next 2 week.
#"target_text" : <sot><sum>Prepare cv<totd>2<spec_time>null<prio>2<status>0<cate>work<diff>3<imp>2<exp_min>120<dow>null<day>null<month>null<no_date>null<no_week>2<no_month>null<eot>

#4. Task within a month task:
#"input_text" :  Finish coding my NLP model before this month.
#"target_text" : <sot><sum>Coding NLP model<totd>4<spec_time>null<prio>2<status>0<cate>work<diff>1<imp>2<exp_min>120<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>0<eot>

#5. Specified day ( day with this month or next n month)
#5.1
#"input_text" :  Remind me to submit my scholarship documents 17 this month .
#"target_text" : <sot><sum>Submit scholarship document<totd>2<spec_time>null<prio>1<status>0<cate>work<diff>2<imp>1<exp_min>60<dow>null<day>17<month>null<no_date>null<no_week>2null<no_month>0<eot>
#5.2
#"input_text" :  Remind me to submit my scholarship documents 17 next month .
#"target_text" : <sot><sum>Submit scholarship document<totd>2<spec_time>null<prio>1<status>0<cate>work<diff>2<imp>1<exp_min>60<dow>null<day>17<month>null<no_date>null<no_week>null<no_month>1<eot>

#Note that, the data begin with token <sot> and end with <eot>. The attributes <diff> (difficulty), <prior>(priority), <imp> (importance) have to value in range 1 - 5 where 1 is the highest value.
#<cate> ( category) is the type of task,
#<exp_min> is the expected amount of time the tasks should be done in minute
#<day>, <month> is specified if the user specifies the day and month the tasks should be done,
#where <no_date>, <no_week> and <no_month> is the number of next date, next week, next month the tasks should be done. Example:
#"I need to done this in the next 2 weeks", then <no_week> is 2, however "I need to done that this week", then <no_week> is 0
#<dow> (day of week) in range 1 - 7, which 1 is sunday,2 is monday (and so on), 7 is saturday. <totd> (time of the day) just follow:
#Midnight: 12:00:00 am - 03:59:59 am (value 0)
#Early Morning: 04:00:00 am - 07:59:59 am (value 1)
#Morning: 08:00:00 am - 11:59:59 am (value 2)
#Afternoon: 12:00:00 pm - 03:59:59 pm (value 3)
#Evening: 04:00:00 pm - 07:59:59 pm (value 4)
#Night: 08:00:00 pm - 11:59:59 pm (value 5)

#If any attributes are not determined, then just give it null value.