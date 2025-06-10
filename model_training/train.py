#!/usr/bin/env python3

from datasets import load_dataset, Dataset
from transformers import TrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM
import numpy as np
import evaluate

#model to be trained
odel = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")


#data set from which to be trained
ds = load_dataset("Helsinki-NLP/opus_fiskmo")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")

#tokenize
ds = Dataset.from_dict(ds)

def tokenize(data):
    fi_tokens = tokenizer(data["fi"], padding="max_length", truncation=True)
    sv_tokens = tokenizer(data["sv"], padding="max_length", truncation=True)
    return {"en_tokens": fi_tokens, "es_tokens": sv_tokens}

ds = ds.tokenize(ds)

#set up compute metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


#Training arguments
training_args = TrainingArguments(
    output_dir="model_output", #output folder
    eval_strategy="epoch"
)

#trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["sv"],
    eval_dataset=dataset["fi"],
    compute_metrics=compute_metrics,
)
print('hi')
#trainer.train()