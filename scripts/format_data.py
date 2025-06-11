#!/usr/bin/env python3

from modules import translate

#scripts to transform data into a hugging face compatible datasets

#format to hugging face
#translate requires boolean True or False on whether you need translation
def format(text_file, make_eng):
    
    #split by periods
    with open(text_file, 'r') as file:
        data = file.read()
        data = data.split('.','\n')

    #remove single periods or extraneous symbols
    data = [sentence.strip() for sentence in data if sentence.strip() != '']

    if make_eng:
        #translate to english
        eng_data = [translate.translate(sentence, "Helsinki-NLP/opus-mt-es-en", "Helsinki-NLP/opus-mt-es-en") for sentence in data]
        print(eng_data)
    x = 0
    for sentence in data:
        print(sentence)
        x += 1

    print(x)

    

format("data/resources-PR/articles.txt", True)