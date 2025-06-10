#!/usr/bin/env python3


# Load model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#choose models here
tokenizer = AutoTokenizer.from_pretrained("./models/model4")
model = AutoModelForSeq2SeqLM.from_pretrained("./models/model4")

#translate function
def translate(text, model, tokenizer):
    # Tokenize the text and prepare it for translation
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Perform the translation
    translated = model.generate(**inputs)

    # Decode the translated tokens back into text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    
    return translated_text

print(translate("t shades of amber and crimson, whispered gently in the breeze. A soft mist clung to the valleys, rising slowly as the sun warmed the earth. In the distance, a river meandered through the fields, its silver waters glistening like a winding ribbon of light.ple pleasures and took pride in their close-knit community. The land, the river, and the hills had been there long before them and would endure long after, holding the memories of generations past.", model, tokenizer))