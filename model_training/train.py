#!/usr/bin/env python3

from datasets import load_dataset, Dataset
from transformers import TrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, DataCollatorForSeq2Seq
import numpy as np
import evaluate


#model to be trained
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")


#tokenize
dataset = load_dataset("Nicolas-BZRD/English_French_Webpages_Scraped_Translated")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
print(dataset.keys())
#def tokenize(examples):
#    return tokenizer(examples["en"], examples['fr'], padding="max_length", truncation=True)

def tokenize(examples):
    # tokenize source sentences (English)
    inputs = tokenizer(examples["en"], max_length=128, truncation=True)
    # tokenize target sentences (French)
    targets = tokenizer(examples["fr"], max_length=128, truncation=True)
    # set labels for decoder - typical Marian fine-tuning
    inputs["labels"] = targets["input_ids"]
    return inputs




dataset = dataset["train"].select(range(1000)).map(tokenize, batched=True)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)


#set up compute metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


#Training arguments
training_args = TrainingArguments(
    output_dir="model_output", #output folder
    #eval_strategy="epoch"
)

#trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    #eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
    data_collator=data_collator,
)
print('hi')
trainer.train()