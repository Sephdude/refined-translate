#!/usr/bin/env python3


# Load model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def load_translator(model, tokenizer):
    #preload the tokenizer and model so that it doesn't need to be reloaded during every translation
    #This is very important for performance when translating large datasets.
    
    #load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    model = AutoModelForSeq2SeqLM.from_pretrained(model)

    return model, tokenizer

#Run this when you want to translate a large dataset. You must have already run load_translator.
#Use the return values for preloaded_model, and preloaded_tokenizer created by load_translator outside your translate loop.
def translate_preloaded(text, preloaded_model, preloaded_tokenizer):

    # Tokenize the text and prepare it for translation
    inputs = preloaded_tokenizer(text, return_tensors="pt", padding=True, max_length=512, truncation=True)

    # Perform the translation
    translated = preloaded_model.generate(**inputs)

    # Decode the translated tokens back into text
    translated_text = preloaded_tokenizer.decode(translated[0], skip_special_tokens=True)
    
    return translated_text


#full translate function. Do NOT use this for large datasets, use translate_preloaded instead
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