#!/usr/bin/env python3

#load oscar dataset and remove unwanted data
#the formatting for this dataset is different than many others on hugging Face, so it might be different if using a seperate dataset

from modules import translate
import json
import os
import re
import multiprocessing
from datasets import Dataset, load_dataset
from urllib.parse import urlparse

#filter out the Puerto Rican spanish from the dataset
#type of data lets you choose whether you want slang found in puerto_rican_slang or domain specific data
#put type of data as "slang" or "domain"


def filter(ds, puerto_rican_slang, start, end, type_of_data):
    

    #remove non text columns
    cols_to_remove = [col for col in ["images", "metadata"] if col in ds.column_names]
    ds = ds.remove_columns(cols_to_remove)
    ds = ds.remove_columns(["images"])

    #create a puerto Rican Dataset and filter
    ds_current = ds["train"].select(range(start, end))

    pr_slang = multiprocessing.Manager().list()
    num_complete = multiprocessing.Manager().Value('i',0)
    process_list = []
    
    ds_length = len(ds_current)

    #split the dataset into chunks for multiprocessing
    ds_current = [ds_current[i::4] for i in range(4)]

    for block in ds_current:
        process_list.append(multiprocessing.Process(target=multi_filter, args=(block, puerto_rican_slang, type_of_data, pr_slang, num_complete, ds_length)))
    
    #run processes and end
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

    return pr_slang

#check if a domain is from Puerto Rico
def pr_domain(domain):
    parse = urlparse(domain)
    return parse.hostname.endswith(".pr")

def multi_filter(ds_current, puerto_rican_slang, type_of_data, pr_slang, num_complete, ds_length):
    

    #extract the Puerto Rican sentences
    for example, metadata in zip(ds_current["text"], ds_current["metadata"]):
        for text_dict in example:
            if type_of_data == "slang":
                #only append if there are two Puerto Rican slang words in the sample
                match_found = 0
                for word in puerto_rican_slang:
                    pattern = r'\b' + re.escape(word.lower()) + r'\b'
                    if re.search(pattern, text_dict["text"].lower()):
                        match_found += 1
                        if match_found >= 2:
                            pr_slang.append(text_dict["text"])
                            break
                            

            if type_of_data == "domain":    
                if pr_domain(metadata["url"].lower()):
                    pr_slang.append(text_dict["text"])
        
        translate.load_bar(num_complete.value, ds_length, example)
        print("ctrl+c to stop")
        num_complete.value += 1
    

    #run filter in steps so it doesn't crash
    for i in range(22):
        start = (len(ds["train"]) // 22) * i
        end = start + (len(ds["train"]) // 22)
        pr_slang.append(filter(ds, puerto_rican_slang, start, end, type_of_data))

        print(f"Completed {i+1} of 22 steps")

    return pr_slang

#execution
if __name__ == "__main__":
    try:
            
        #load Spanish oscar dataset
        ds = load_dataset("oscar-corpus/mOSCAR", "spa_Latn")

        #slang words to filter in
        puerto_rican_slang = [
        "Acho", "Wepa", "Chévere", "Nene", "Nena", "Boricua", "Janguear", "Guagua", "Corillo", "Chavo", "perreo", "perrea", "cabrón", "boricua", "Puerto Rico",
        "Mofongo", "Brutal", "Pichea", "Fren", "Chinchorro", "Tato", "Nítido", "Bregar", "Al garete", "Jartera",
        "Ñangotarse", "Zafacón", "Gufear", "Mandilón", "Jibaro", "Cangri", "Bregar", "Jíbaro", "Guillao", "Tiguere",
        "Guilla", "Pichea", "Fula", "Cangri", "Chombo", "Coro", "Chavos", "Pato", "Vacilón", "Jíbaro",
        "Gato", "Chota", "Chinchorreo", "To’", "Bregar", "Mamey", "Bayunco", "Naco", "Changuería", "La Jeva",
        "Bregar", "Chulear", "Ponte las pilas", "Estoy ready", "Tirar la toalla", "Pegar la vuelta", "Estar pelao", "Montar un coro", "Estar jarto", "Janguear",
        "En candela", "Hacer corillo", "Chévere", "La nota", "Arroz con habichuelas", "Me pica el bagre", "Chango", "La guagua", "Cotorra", "Chiviarse",
        "En bola", "Dar la talla", "Pato", "Mabí", "Tiraera", "Tramar", "Guaguaeta", "Pichea eso", "Jeva", "Gufear",
        "Estar pelao", "Güevón", "Montar un palo", "Ronear", "Arroz con dulce", "To’ guilla", "Chacho", "Mangó", "Mamey", "A fuego",
        "Bregar con", "Pato", "Jartera", "Mambo", "Pichear", "Chongo", "Tigre", "Mangú", "Brutal", "Güira",
        "Chavos", "Tumbao", "Nítido", "A la orden", "Chichaito", "Fula", "Jeva", "Bregar", "Chivear", "Vacilar",
        "Al garete", "Pichear", "Pelea de gallos", "Coro", "Mamey", "Chavo", "Guillao", "Changa", "La brega", "Tiradera",
        "Chota", "Ponerse las pilas", "Guaraguao", "Majar", "Arrecho", "Bregar", "La jeva", "Pelar", "Chiripi", "Gato",
        "Acho", "Tiraera", "Pichea", "Zafacón", "Ñangotarse", "Pelea de calle", "Corillo", "To’ guilla", "Tigueraje", "Cangri",
        "Brutal", "Chivo", "Jartera", "Mamey", "Nítido", "Fula", "Chévere", "Güevón", "Tumbao", "Pichar",
        "Vacilar", "Rolo", "Bregar duro", "Chinchorrear", "Cangrim", "Brutalísimo", "Guay", "Mangú de plátano", "Chola", "Ñema",
        "Zafaconear", "Matar un tigre", "Bregar con la vida", "Jeva buena", "Chamaquita", "Pato nuevo", "Mangú de guineo", "Guapo", "Vacilar duro", "Tiraera caliente",
        "Chinchorreo nocturno", "Bregando", "Pichear eso ya", "Mandilón perdido", "Jangueo", "Fular", "Ñangote", "Pajilla", "Chilindrón", "Zafacón lleno",
        "Brutalito", "Jíbaro de ciudad", "Pichea pana", "Fren en candela", "Tumbao duro", "Changa loca", "Mangú sucio", "Choto", "Corillo loco", "Ponte alante",
        "Chicha", "Gufiado", "Mandilonazo", "Ñengo", "Chango pelúo", "Pelea callejera", "Chévere brutal", "Bregar a lo bestia", "Vacilón total", "Tiguerazo",
        "Guillao loco", "Jartera mala", "Chavo duro", "Pichar duro", "Mamey de calle", "Ronear fuerte", "Brega dura", "Tiraera fuerte", "Chinchorro duro", "Pelea de gallos fuerte",
        "Mangú con to'","Corillo fuerte", "Jeva loca", "Mandilón fuerte", "Ñangotazo", "Vacilar bien", "Brutal total", "Pato fuerte", "Jíbaro duro", "Chévere total",
        "Guagua loca", "Chota fuerte", "Zafacón roto", "Bregar sin parar", "Tumbao fuerte", "Pichea duro", "Fren loco", "Chulo", "Mamey suave", "Bregando fuerte",
        "Mandilón loco", "Chinchorreo fuerte", "Jangueo fuerte", "Vacilón brutal", "Pelea de calle dura", "Corillo brutal", "Ñangote fuerte", "Ronear duro", "Guillao fuerte", "Tigueraje brutal",
        "Mangú duro", "Chacho loco", "Pichear fuerte", "Fula fuerte", "Jartera brutal", "Chavo loco", "Brega brutal", "Mandilón total", "Vacilar duro", "Zafacón fuerte",
        "Chinchorro brutal", "Pato brutal", "Tumbao total", "Brutal loco", "Pelea callejera brutal", "Corillo total", "Jeva brutal", "Jangueo total", "Mandilón brutal", "Ñangotazo fuerte",
        "Vacilar total", "Fren brutal", "Cholo", "Mangú brutal", "Pichear total", "Chavo total", "Bregar brutal", "Zafacón total", "Jíbaro total", "Tigueraje total",
        "Guillao total", "Ronear total", "Bregar total", "Chacho brutal", "Pelea brutal", "Mandilón loco", "Vacilar brutal", "Jartera total", "Chinchorro total", "Pato total",
        "Tumbao brutal", "Brutal total", "Pelea de gallos total", "Corillo loco", "Jeva total", "Jangueo brutal", "Mandilón total", "Ñangotazo brutal", "Vacilar total", "Fren total",
        "Mangú total", "Pichear brutal", "Chavo brutal", "Bregar total", "Zafacón brutal", "Jíbaro brutal", "Tigueraje brutal", "Guillao brutal", "Ronear brutal", "Bregar brutal",
        "Chacho total", "Pelea total", "Mandilón brutal", "Vacilar total", "Jartera brutal", "Chinchorro brutal", "Pato brutal", "Tumbao brutal", "Brutal brutal", "Pelea de gallos brutal",
        "Corillo brutal", "Jeva brutal", "Jangueo brutal", "Mandilón brutal", "Ñangotazo brutal", "Vacilar brutal", "Fren brutal", "Mangú brutal", "Pichear brutal", "Chavo brutal",
        "Bregar brutal", "Zafacón brutal", "Jíbaro brutal", "Tigueraje brutal", "Guillao brutal", "Ronear brutal", "Bregar brutal", "Chacho brutal", "Pelea brutal", "Mandilón brutal",
        "Vacilar brutal", "Jartera brutal", "Chinchorro brutal", "Pato brutal", "Tumbao brutal", "Brutal brutal", "Pelea de gallos brutal", "Corillo brutal", "Jeva brutal", "Jangueo brutal"
        ]



        #the list of slang
        pr_slang = []

        #run filter in steps so it doesn't crash
        for i in range(22):
            start = (len(ds["train"]) // 22) * i
            end = start + (len(ds["train"]) // 22)
            pr_slang.append(filter(ds, puerto_rican_slang, start, end, "slang"))

            print(f"Completed {i+1} of 22 steps")


    finally:

        print("quitting")
        with open(f"data/data-output/filtered_data.txt", "w", encoding="utf-8") as f:
            #make a text file with the filtered Puerto Rican slang examples
            for block in pr_slang:
                for example in block:
                    f.write(example + "\n")