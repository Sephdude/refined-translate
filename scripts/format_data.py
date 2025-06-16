#!/usr/bin/env python3

from modules import translate
import json
import os
import re
import spacy


#scripts to transform data into a hugging face compatible datasets

#format to hugging face
#translate requires boolean True or False on whether you need translation   

def create_file(data_dict):
    #serialize
    json_text = json.dumps(data_dict, indent=4)
    #check if file name exists
    file_path = "data/data-output/"
    file_name = "output.json"
    
    name_num = 0
    while os.path.exists(file_path + file_name):
        file_name ="output" + str(name_num) + '.json'
        name_num += 1

    #put data into json file
    with open(file_path + file_name, "w") as json_file:
        json_file.write(json_text)

def format(text_file):
    
    data_dict = []

    #split by periods
    with open(text_file, 'r') as file:
        data = file.read()
        

    #remove single periods or extraneous symbols
    #data = [sentence.strip() for sentence in data if sentence.strip() != '']
    #put periods back into the end of each sentence
    #data = [sentence + '.' for sentence in data]

    #use spacy to split the data into sentences and clean it up
    nlp = spacy.load("es_core_news_sm")
    nlp.add_pipe("sentencizer")
    data = str(nlp(data))
    print(data)
    #turn into list
    data = data.split('\n') 
    

    #remove extraneous stuff
    data = [sentence.strip() for sentence in data if sentence.strip() != ''] 

    #remove special characters and numbers
    data = [re.sub('r[^a-zA-Z0-9]', '', sentence) for sentence in data]
    
    #remove whitespace
    data = [sentence for sentence in data if sentence != '']
    
    for i, sentence in enumerate(data):
        sentence = sentence.strip()

        #fix problems with questions
        if sentence.startswith('¿'):
            if not sentence.endswith('?'):
                sentence += '?'
        
        #add punctuation if not present
        else:
            if not sentence.endswith(('.', '?', '?')):
                sentence += '.'
        
        #change string in list
        data[i] = sentence

    try:
        for sentence in data:


            #translate
            eng = translate.translate(sentence, "Helsinki-NLP/opus-mt-es-en", "Helsinki-NLP/opus-mt-es-en")

            #add block to json file
            block = {"es":sentence, "en":eng}
            data_dict.append(block)


    finally:
        #create file on close
        create_file(data_dict)





    

format("data/resources-PR/slrPR.tsv")