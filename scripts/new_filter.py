#!/usr/bin/env python3

#load oscar dataset and remove unwanted data
#the formatting for this dataset is different than many others on hugging Face, so it might be different if using a seperate dataset

from modules import translate
import json
import os
import re
import unicodedata
from multiprocessing import Pool, Lock, Manager
from datasets import Dataset, load_dataset
from urllib.parse import urlparse
from itertools import islice

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

#strip accents to avoid false positives
def strip_accents(text):
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

#filter through individual blocks of data
def filter_words(block):
     
    #list of Puerto Rican sentences found in block
    sentences_matched = []



    #extract the Puerto Rican sentences
    for example, metadata in zip(block["text"], block["metadata"]):
        for text_dict in example:
            
            if data_type == "domain":
                #check if the domain is from Puerto Rico
                if "domain" in metadata and pr_domain(metadata["domain"]):
                    sentences_matched.append(text_dict["text"])
                    continue
            
            if data_type == "slang":
                #only append if there are two Puerto Rican slang words in the sample
                matched_words = set()
                for word in puerto_rican_slang:
                    #strip accents and special characters from the text
                    pattern = r'\b' + strip_accents(re.escape(word)).replace(r'\ ', r'\s+') + r'\b'
                    print(pattern)

                    #strip accents from the text to avoid false positives
                    stripped_text = strip_accents(text_dict["text"])
                    print(stripped_text)
                    
                    #check if the word is in the text if the same word has not been already found
                    if re.search(pattern, stripped_text, re.IGNORECASE):
                        if word not in matched_words:
                            matched_words.add(word)
                
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

        #slang words to filter in
        puerto_rican_slang = [
    "Acho", "Wepa", "Chévere", "Nene", "Nena", "Boricua", "Janguear", "Guagua", "Corillo", "Chavo",
    "perreo", "perrea", "cabrón", "Puerto Rico", "Mofongo", "Brutal", "Pichea", "Fren", "Chinchorro",
    "Tato", "Nítido", "Bregar", "Al garete", "Jartera", "Ñangotarse", "Zafacón", "Gufear", "Mandilón",
    "Jibaro", "Cangri", "Jíbaro", "Guillao", "Tiguere", "Guilla", "Chombo", "Coro", "Chavos", "Pato",
    "Vacilón", "Chota", "Chinchorreo", "To’", "Mamey", "Bayunco", "Naco", "Changuería",
    "La Jeva", "Chulear", "Ponte las pilas", "Estoy ready", "Tirar la toalla", "Pegar la vuelta",
    "Estar pelao", "Montar un coro", "Estar jarto", "En candela", "Hacer corillo", "La nota",
    "Arroz con habichuelas", "Me pica el bagre", "Chango", "La guagua", "Cotorra", "Chiviarse",
    "En bola", "Dar la talla", "Mabí", "Tiraera", "Tramar", "Guaguaeta", "Pichea eso", "Jeva",
    "Güevón", "Montar un palo", "Ronear", "Arroz con dulce", "To’ guilla", "Chacho", "Mangó", "A fuego",
    "Bregar con", "Mambo", "Pichear", "Chongo", "Tigre", "Mangú", "Güira", "Tumbao", "A la orden",
    "Chichaito", "Chivear", "Vacilar", "Pelea de gallos", "Changa", "La brega", "Tiradera", "Ponerse las pilas",
    "Guaraguao", "Majar", "Arrecho", "Pelar", "Chiripi", "Pelea de calle", "Tigueraje", "Chivo", "Pichar",
    "Rolo", "Bregar duro", "Chinchorrear", "Cangrim", "Brutalísimo", "Guay", "Mangú de plátano", "Chola",
    "Ñema", "Zafaconear", "Matar un tigre", "Bregar con la vida", "Jeva buena", "Chamaquita", "Pato nuevo",
    "Mangú de guineo", "Guapo", "Vacilar duro", "Tiraera caliente", "Chinchorreo nocturno", "Bregando",
    "Pichear eso ya", "Mandilón perdido", "Jangueo", "Fular", "Ñangote", "Pajilla", "Chilindrón",
    "Zafacón lleno", "Brutalito", "Jíbaro de ciudad", "Pichea pana", "Fren en candela", "Tumbao duro",
    "Changa loca", "Mangú sucio", "Choto", "Corillo loco", "Ponte alante", "Chicha", "Gufiado",
    "Mandilonazo", "Ñengo", "Chango pelúo", "Pelea callejera", "Chévere brutal", "Bregar a lo bestia",
    "Vacilón total", "Tiguerazo", "Guillao loco", "Jartera mala", "Chavo duro", "Pichar duro",
    "Mamey de calle", "Ronear fuerte", "Brega dura", "Tiraera fuerte", "Chinchorro duro",
    "Pelea de gallos fuerte", "Mangú con to'", "Corillo fuerte", "Jeva loca", "Mandilón fuerte",
    "Ñangotazo", "Vacilar bien", "Brutal total", "Pato fuerte", "Jíbaro duro", "Chévere total",
    "Guagua loca", "Chota fuerte", "Zafacón roto", "Bregar sin parar", "Tumbao fuerte", "Pichea duro",
    "Fren loco", "Chulo", "Mamey suave", "Bregando fuerte", "Mandilón loco", "Chinchorreo fuerte",
    "Jangueo fuerte", "Vacilón brutal", "Pelea de calle dura", "Corillo brutal", "Ñangote fuerte",
    "Ronear duro", "Guillao fuerte", "Tigueraje brutal", "Mangú duro", "Chacho loco", "Pichear fuerte",
    "Fula fuerte", "Jartera brut    al", "Chavo loco", "Brega brutal", "Mandilón total", "Zafacón fuerte",
    "Chinchorro brutal", "Pato brutal", "Tumbao total", "Brutal loco", "Pelea callejera brutal",
    "Corillo total", "Jeva brutal", "Jangueo total", "Ñangotazo fuerte", "Vacilar total", "Fren brutal",
    "Cholo", "Mangú brutal", "Pichear total", "Chavo total", "Bregar brutal", "Zafacón total",
    "Jíbaro total", "Tigueraje total", "Guillao total", "Ronear total", "Bregar total", "Chacho brutal",
    "Pelea brutal", "Vacilar brutal", "Jartera total", "Chinchorro total", "Pato total", "Tumbao brutal",
    "Brutal brutal", "Pelea de gallos brutal"
]
        
        #sort the list so regex doesn't falsely identify words
        puerto_rican_slang = sorted(puerto_rican_slang, key=lambda x: -len(x))
        
        #set up lock  so the txt file is not corrupted
        manager = Manager()
        lock = manager.Lock()

        batch_size = 10000  # Size of each batch
        process_count = os.cpu_count()  # Number of processes to use

        #set this to change the type of data to filter
        data_type = "slang"

        #chunk up batches and filter in multiprocessing
        for batch in make_batch(dataset_format(ds)["train"], batch_size):
                    
                    #set up filter arguments
                    args = []
                    for i in range(process_count):
                        start = i * (len(batch) // process_count)
                        end = start + (len(batch) // process_count)
                        args.append(batch.select(range(start, end)))

                    print(args)

                    #set up multiprocessing pool
                    with Pool(process_count) as pool:
                         pool.map(filter_words, args)