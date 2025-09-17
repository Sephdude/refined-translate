#!/usr/bin/env python3

from modules import translate
from modules import text_manipulation
import json
import os
import re
import spacy
from multiprocessing import Pool, Lock, Manager
from tqdm import tqdm

#scripts to transform data into a hugging face compatible datasets
#format to hugging face
#translate requires boolean True or False on whether you need translation   


#execute
if __name__ == "__main__":

    #file to read from
    text_file = "/home/joe/Repositories/refined-translate/puerto_rican_slang.txt"

    #load text from file
    with open(text_file, 'r') as file:
        text = file.read().split('\n') #split up so that nlp.pipe can handle it

    nlp = spacy.load("es_core_news_sm")
    nlp.add_pipe("sentencizer")
    nlp.max_length = 1000000000

    #write sentences to a new file

    sentence_str = ""
    batch_size = 1000


    with open("sentencized_dataset.txt", 'w') as file:   
        for doc in tqdm(nlp.pipe(text, batch_size=batch_size), total=len(text)):
            for sent in doc.sents:
                sentence_str += str(sent) + '\n'
                
                
            if len(sentence_str) >= 1000:
                file.write(sentence_str)
                sentence_str = ""
        
        file.write(sentence_str)
        


