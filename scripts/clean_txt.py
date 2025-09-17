#!/usr/bin/env python3

#This script further filters non puerto rican sentences from the
# sentencized dataset saved as a txt with sentences split by new lines
# it only can use single word slang, no phrases

from modules.text_manipulation import strip_accents, puerto_rican_slang
import os
from tqdm import tqdm
import re

def open_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [strip_accents(line.strip()) for line in lines]




if __name__ == "__main__":
    
    #normalize slang words
    puerto_rican_slang = [strip_accents(word) for word in puerto_rican_slang]


    #get data
    data = open_file("/home/joe/Repositories/refined-translate/data_files/sentencized_dataset.txt")

    new_data = []

    #filter through the data
    for sentence in tqdm(data, total=len(data)):
        #normalize sentences
        words = strip_accents(sentence.lower())
        words = set(re.findall(r"\b\w+\b", words))

        #check for matches
        if any(word in puerto_rican_slang for word in words):
            new_data.append(sentence)
    
    #save to file
    with open("/home/joe/Repositories/refined-translate/data_files/cleaned_sentencized_dataset.txt", "w", encoding='utf-8') as f:
        for line in new_data:
            f.write(line + "\n")