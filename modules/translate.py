#!/usr/bin/env python3


# Load model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#translate function
def translate(text, model, tokenizer):

    #choose models here
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    model = AutoModelForSeq2SeqLM.from_pretrained(model)

    # Tokenize the text and prepare it for translation
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Perform the translation
    translated = model.generate(**inputs)

    # Decode the translated tokens back into text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    
    return translated_text

#code for loading bar
def load_bar(number, total, block):
    progress = round((number / total) * 40)
    bar = ""
    for i in range(progress):
        bar += '■'
    for i in range(40-progress):
        bar += '□'

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(block)
    print(bar)