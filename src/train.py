from transformers import AutoModelForSeq2SeqLM
from transformers import TrainingArguments

#load English to Spanish model
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")


#training arguments
training_args = TrainingArguments(
    output_dir="./output",
    eval_strategy="epoch",
    push_to_hub=False,
)

#trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
)
trainer.train() #train model