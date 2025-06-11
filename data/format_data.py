#!/usr/bin/env python3


#scripts to transform data into a hugging face compatible datasets

#split every sentence up into a list
def new_line(text_file):
    
    #split by periods
    with open(text_file, 'r') as file:
        data = file.read()
        data = data.split('.')

    #remove single periods or extraneous symbols
    data = [sentence.strip() for sentence in data if sentence.strip() != '']

    print(data)

new_line("resources-PR/articles.txt")    