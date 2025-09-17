#!/usr/bin/env python3

from datasets import load_from_disk
from modules.text_manipulation import strip_accents, puerto_rican_slang
from tqdm import tqdm

if __name__ == "__main__":

    #load the dataset from disk
    ds = load_from_disk("data_files/mOSCAR_spa_Latn")

    #standardize the slang words
    clean_slang = [strip_accents(word.lower()) for word in puerto_rican_slang]
    print(clean_slang)

    #list of new sentences
    sentences_matched = []

    #choose a batch size for loading
    batch_size = 1000

    #load the dataset and filter
    for i in tqdm(range(0, len(ds), batch_size)):
        texts = ds[i: i + batch_size]["text"]

        for text_lst in texts:
            for text_dict in text_lst:
                matches = strip_accents(text_dict["text"].lower())

                matched_words = {phrase for phrase in clean_slang if phrase in matches}

                if len(matched_words) >= 2:
                    sentences_matched.append(text_dict["text"])

                #check if the list of new words is too long and if so write to a file
                if len(sentences_matched) >= 1000:
                    with open("puerto_rican_slang.txt", "a", encoding='utf-8') as f:
                        for sentence in sentences_matched:
                            f.write(sentence + "\n")
                    sentences_matched = []
