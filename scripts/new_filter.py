#!/usr/bin/env python3

#load oscar dataset and remove unwanted data
#the formatting for this dataset is different than many others on hugging Face, so it might be different if using a seperate dataset

from modules import translate
from modules import text_manipulation
import json
import os
import re
from multiprocessing import Pool, Lock, Manager
from datasets import Dataset, load_dataset
from urllib.parse import urlparse
from itertools import islice
from tqdm import tqdm

#filter out the Puerto Rican spanish from the dataset
#type of data lets you choose whether you want slang found in puerto_rican_slang or domain specific data
#put type of data as "slang" or "domain"

#check if a domain is from Puerto Rico
def pr_domain(domain):
    parse = urlparse(domain)
    return parse.hostname.endswith(".pr")


def make_batch(streaming_set, size):
    """Batch data into chunks of size."""
    it = iter(streaming_set)
    while True:
        batch = list(islice(it, size))
        batch = Dataset.from_list(batch)
        if not batch:
            break
        yield batch

#format dataset to be run through the filter
def dataset_format(ds):
     #remove non text columns
    ds = ds.map(lambda x: {"text": x["text"]})
    ds = ds.map(lambda example: {k: v for k, v in example.items() if k != "images"})

    return ds



#filter through individual blocks of data
def filter_words(block):
     
    #list of Puerto Rican sentences found in block
    sentences_matched = []



    #extract the Puerto Rican sentences
    for example, metadata in tqdm(zip(block["text"], block["metadata"]), total=len(block["text"])):

        #strip accents and special characters from the text
        clean_slang = [text_manipulation.strip_accents(word.lower()) for word in puerto_rican_slang]

                    
        for text_dict in example:
            
            if data_type == "domain":
                #check if the domain is from Puerto Rico
                if "domain" in metadata and pr_domain(metadata["domain"]):
                    sentences_matched.append(text_dict["text"])
                    continue
            
            if data_type == "slang":
                #only append if there are two Puerto Rican slang words in the sample
                matched_words = set()

                #strip accents from the text to avoid false positives
                stripped_text = text_manipulation.strip_accents(text_dict["text"]).lower()

                #for word in clean_slang:    
                   #check if the word is in the text if the same word has not been already found
                #    if word in stripped_text:
                #        if word not in matched_words:
                #            matched_words.add(word)
                
                matches = set(stripped_text.lower().split())
                matched_words = matches & set(clean_slang)

                if len(matched_words) >= 2:
                    sentences_matched.append(text_dict["text"])


    
    #write the sentences to the text file
    if sentences_matched:
        with open("puerto_rican_slang.txt", "a") as f:
            for sentence in sentences_matched:
                f.write(sentence + "\n")
     


#execution
if __name__ == "__main__":
    #load Spanish oscar dataset
    ds = load_dataset("oscar-corpus/mOSCAR", "spa_Latn", streaming=True)

    puerto_rican_slang = text_manipulation.puerto_rican_slang
    
    #sort the list so regex doesn't falsely identify words
    puerto_rican_slang = sorted(puerto_rican_slang, key=lambda x: -len(x))
    
    #set up lock  so the txt file is not corrupted
    manager = Manager()
    lock = manager.Lock()

    batch_size = 50000  # Size of each batch
    dataset_size = 20600000 # Approximate size of the dataset

    process_count = os.cpu_count()  # Number of processes to use

    #set this to change the type of data to filter
    data_type = "slang"
    
    #track how many batches have been done
    batches_complete = 0

    #format the dataset
    formatted_ds = dataset_format(ds["train"])


    #chunk up batches and filter in multiprocessing
    for batch in make_batch(formatted_ds, batch_size):
        
        #load bar
        translate.load_bar(batches_complete * batch_size, dataset_size, "Batches complete: \n")

        #set up filter arguments
        args = []
        for i in range(process_count):
            start = i * (len(batch) // process_count)
            end = start + (len(batch) // process_count)
            args.append(batch.select(range(start, end)))


        #set up multiprocessing pool
        with Pool(process_count) as pool:
                pool.map(filter_words, args)

        batches_complete += 1