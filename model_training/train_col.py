#!/usr/bin/env python3

from datasets import load_dataset, Dataset
from transformers import TrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, DataCollatorForSeq2Seq
import numpy as np
import evaluate

#model to be trained
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")


#load dataset
dataset = load_dataset("Nicolas-BZRD/English_French_Webpages_Scraped_Translated")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")

#tokenize
def tokenize(examples):
    inputs = tokenizer(examples["en"], max_length=128, truncation=True)
    targets = tokenizer(examples["fr"], max_length=128, truncation=True)
    inputs["labels"] = targets["input_ids"]
    return inputs

dataset = dataset["train"].select(range(1000)).map(tokenize, batched=True) #adjust range to add more data

#collate data
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
    learning_rate=1e-5,
    per_device_train_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.001,
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

trainer.train()
