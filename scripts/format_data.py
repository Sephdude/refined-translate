#!/usr/bin/env python3

from modules import translate
import json
import os
import re
import spacy
import multiprocessing


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

#code for loading bar
def load_bar(number, total):
    progress = round((number / total) * 40)
    bar = ""
    for i in range(progress):
        bar += '■'
    for i in range(40-progress):
        bar += '□'

    print(bar)



def format(data, translated_lst,num_complete, total, set):
    
    
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

    for sentence in data:

        #translate
        eng = translate.translate(sentence, "Helsinki-NLP/opus-mt-es-en", "Helsinki-NLP/opus-mt-es-en")

        #add block to main dictionary
        block = {"set":set, "es":sentence, "en":eng}
        translated_lst.append(block)
        
        #indicate that a new sentence has been translated
        num_complete.value += 1

        #display loading bar
        load_bar(int(num_complete.value),total)



#format using multiprocessing
def format_multi(text_file, process_count, set):

    try:
        with open(text_file, 'r') as file:
            text = file.read()


        #use spacy to split the data into sentences and clean it up
        nlp = spacy.load("es_core_news_sm")
        nlp.add_pipe("sentencizer")
        doc = nlp(text)



        #remove extraneous stuff
        data = [sent.text.strip() for sent  in doc.sents if sent.text.strip() != ''] 

        #remove special characters and numbers
        data = [re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ¡¿,.?! ]', '', sentence) for sentence in data]

        #remove whitespace
        data = [sentence for sentence in data if sentence != '']

        #find total number of sentences
        sent_total = 0
        for sent in data:
            sent_total += 1
        
        #partition off pieces of text to be processed
        data_dict  = {}
        for num in range(process_count):
            start = round((num/process_count) * sent_total)
            print(start)
            end = round(((num+1)/process_count) * sent_total)
            data_dict[f"block_{num}"] = data[start:end]

        
        #create processes and pass in list
        translated_lst = multiprocessing.Manager().list()
        num_complete = multiprocessing.Manager().Value('i',0)
        process_list = []
        for key, data in data_dict.items():
            process_list.append(multiprocessing.Process(target=format, args=(data, translated_lst, num_complete,sent_total, set)))
        
        #start processs
        for process in process_list:
            process.start()
        #stop processs once done
        for process in process_list:
            process.join()
    
    #make file
    finally:

        print('exiting')

        #create file on close
        create_file(list(translated_lst))

        print("finished")
#execution
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    format_multi("/home/joe/Documents/Resources PR/set1.txt", 8, 1)
