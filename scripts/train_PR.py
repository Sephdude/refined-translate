#!/usr/bin/env python3

from datasets import load_dataset, Dataset
from transformers import TrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, DataCollatorForSeq2Seq
import numpy as np
import evaluate
import os
import gc


def run_trainer(dataset, tokenizer, model):
    #configure memory
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

    import torch
    import transformers


    #model to be trained
    model = AutoModelForSeq2SeqLM.from_pretrained(model).to("cuda")

    #make sure its running on the gpu

    print(next(model.parameters()).device)
    #load dataset
    dataset = load_dataset("json", data_files="hf://datasets/Sephdude/esPR_en/dataset.json")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)


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


    # Example: split into train/val/test
    train_testvalid = dataset["train"].train_test_split(test_size=0.2, seed=42)
    test_valid = train_testvalid["test"].train_test_split(test_size=0.5, seed=42)

    dataset_train = train_testvalid["train"].map(tokenize, batched=True, remove_columns=["en", "es"])
    dataset_valid = test_valid["train"].map(tokenize, batched=True, remove_columns=["en", "es"])
    dataset_test  = test_valid["test"].map(tokenize, batched=True, remove_columns=["en", "es"])

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
        remove_unused_columns=False,
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
    #test performance
    test = trainer.evaluate(eval_dataset=dataset_test)
    print(test)
    
    torch.cuda.empty_cache()
    gc.collect()

    #trainer.evaluate(dataset_test)

    torch.cuda.empty_cache()
    gc.collect()

    model.save_pretrained("/home/joe/Repositories/refined-translate/model_training/model_output/")
    tokenizer.save_pretrained("/home/joe/Repositories/refined-translate/model_training/model_output/")

#execution
if __name__ == "__main__":
    run_trainer("Sephdude/esPR-en", "Helsinki-NLP/opus-mt-en-es", "Helsinki-NLP/opus-mt-en-es")
