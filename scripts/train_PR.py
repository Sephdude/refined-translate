#!/usr/bin/env python3

from datasets import load_dataset, Dataset
from transformers import TrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, DataCollatorForSeq2Seq
import numpy as np
import evaluate
import os
import gc
#configure memory
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

import torch
import transformers
print(transformers.__version__)


#model to be trained
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")

model.to("cuda")

print(next(model.parameters()).device)
#load dataset
dataset = load_dataset("Sephdude/esPR-en")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")

#filter out the style markers
dataset = dataset.remove_columns("style")
print(dataset)

#tokenize
def tokenize(examples):
    inputs = tokenizer(examples["en"], max_length=128, truncation=True, padding="max_length")
    targets = tokenizer(examples["es"], max_length=128, truncation=True, padding="max_length")
    
    labels = targets["input_ids"]
    labels = [
        [(token if token != tokenizer.pad_token_id else -100) for token in label] 
        for label in labels
    ]

    inputs["labels"] = labels
    return inputs

#put in two datasets, one for more formal writing, two for common phrases
dataset_train = dataset["train"].map(tokenize, batched=True, remove_columns=["es", "en"])
dataset_valid = dataset["validation"].map(tokenize, batched=True, remove_columns=["es", "en"])
dataset_test = dataset["test"].map(tokenize, batched=True, remove_columns=["es", "en"])


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
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=1,
    eval_accumulation_steps=2,
    num_train_epochs=3,
    weight_decay=0.001,
    remove_unused_columns=True,
    fp16=True,
)

#trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset_train,
    eval_dataset=dataset_valid,
    compute_metrics=None,
    data_collator=data_collator,
    
)

trainer.train()
torch.cuda.empty_cache() #empty cache so dont crash
gc.collect()
trainer.evaluate()#eval_dataset=dataset_valid.select(range(100),))

torch.cuda.empty_cache()
gc.collect()

trainer.evaluate(dataset_test)

torch.cuda.empty_cache()
gc.collect()

model.save_pretrained("~/Repositories/refined-translate/model_training/model_output/")
tokenizer.save_pretrained("~/Repositories/refined-translate/model_training/model_output/")