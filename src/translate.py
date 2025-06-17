#!/usr/bin/env python3


# Load model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")





#translate function
def translate(text, model, tokenizer):
    # Tokenize the text and prepare it for translation
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Perform the translation
    translated = model.generate(**inputs)

    # Decode the translated tokens back into text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    
    return translated_text


    