#!/usr/bin/env python3

#load oscar dataset and remove unwanted data

from modules import translate
import json
import os
import re
import spacy
import multiprocessing
from datasets import Dataset, load_dataset


def filter():
    #load Spanish oscar dataset
    ds = load_dataset("oscar-corpus/mOSCAR", "spa_Latn")

    #tokenizer = AutoTokenizer.from_pretrained(tokenizer)

    #slang words to filter in
    puerto_rican_slang = [
        "wepa", "Wepa", "acho", "Acho", "chacho", "Chacho", "diache", "Diache",
        "boricua", "Boricua", "nene", "Nene", "nena", "Nena", "corillo", "Corillo", "cangri", "Cangri",
        "brutal", "Brutal", "mamey", "Mamey", "zafacón", "Zafacón", "al garete", "Al garete", "jartera", "Jartera",
        "bregar", "Bregar", "breg", "Breg", "janguear", "Janguear", "jangue", "Jangue", "gufear", "Gufear", "gufe", "Gufe", "pichear", "Pichear", "piche", "Piche",
        "guagua", "Guagua", "bicho", "Bicho", "tiraera", "Tiraera", "lengua suelta", "Lengua suelta",
        "mano", "Mano", "cantazo", "Cantazo", "charro", "Charro", "jíbaro", "Jíbaro", "feca", "Feca", "taíno", "Taíno",
        "pichea", "Pichea", "jangueo", "Jangueo", "bregando", "Bregando", "gufeo", "Gufeo", "vacilón", "Vacilón", "a"
    ]   
    #remove non text columns
    cols_to_remove = [col for col in ["images", "metadata"] if col in ds.column_names]
    ds = ds.remove_columns(cols_to_remove)
    ds = ds.remove_columns(["images", "metadata"])
    
    print(ds["train"])

    #create a puerto Rican Dataset and filter
    ds = ds["train"].select(range(1000))  # Limit to first 1000 examples for testing; adjust as needed



    print(ds[0]["text"])  # See if it's a string or a list

    pr_slang = []

    #extra the Puerto Rican sentences
    for example in ds["text"]:
        for dict in example:
            for word in puerto_rican_slang:
                if word in dict["text"]:
                    print(dict["text"])
                    pr_slang.append(dict["text"])

    #pr_slang = ds.filter(lambda x: any(word in x["text"].lower() for word in puerto_rican_slang), batched=False)


    with open("data/data-output/filtered_data.txt", "w", encoding="utf-8") as f:
        #make a text file with the filtered Puerto Rican slang examples
        for example in pr_slang:
            f.write(example + "\n")

#execution
if __name__ == "__main__":
    filter()