#!/usr/bin/env python3

#################################
#Script translates Spanish text examples into english and puts them into a json file.
#To run the script your spanish sentence file must be split by new lines per sentence.
#example:
#sentence 1
#sentence 2
#sentence 3
#################################

from modules import translate
import json
import os
from transformers import pipeline
from datasets import load_dataset
from tqdm import tqdm
import unicodedata, re

def clean_text(text):
    #manage accents
    text= unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")

    #remove sepcial characters
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)
    return text.strip()

#execute
if __name__ == "__main__":

    #file to read from
    text_file = "/home/joe/Repositories/refined-translate/data_files/cleaned_sentencized_dataset.txt"

    text_dataset = load_dataset("text", data_files={"train": text_file})


    #adjust batch size based on your GPU memory
    batch_size = 32

    #initialize translator
    translator = pipeline("translation", 
                          model="Helsinki-NLP/opus-mt-es-en", 
                          device=0, 
                          batch_size=batch_size,
                          max_length=512,
                          truncation=True)

    #list to hold the text and translation dictionaries
    data_list = []

    #load text file into list
    #batch and translate
    current_batch = []

    text_dataset.map()


    for  line in tqdm(text_dataset["train"]["text"], total=len(text_dataset["train"]["text"])):
        
        #clean the line up
        line = clean_text(line)
        
        if len(line) > 512:
            line = line[:512] #truncate if too long
            
        current_batch.append(line)
        if len(current_batch) == batch_size:
            translations = translator(current_batch)
            #add to dictionary the text and translations
            
            translation_lst = [t['translation_text'].replace('.', '') for t in translations]

            translation_dict_lst = [{"es": es, "en": en} for es, en in zip(current_batch, translation_lst)]


            data_list.extend(translation_dict_lst)
            
            current_batch = []
    
    # Write JSON to a file
    with open("dataset.json", "w") as file:
        json.dump(data_list, file, indent=4)
