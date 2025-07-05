#!/usr/bin/env python3

#load oscar dataset and remove unwanted data

from modules import translate
import json
import os
import re
import multiprocessing
from datasets import Dataset, load_dataset
from urllib.parse import urlparse

#filter out the Puerto Rican spanish from the dataset
def filter(ds, puerto_rican_slang, start, end):
    

    #remove non text columns
    cols_to_remove = [col for col in ["images", "metadata"] if col in ds.column_names]
    ds = ds.remove_columns(cols_to_remove)
    ds = ds.remove_columns(["images"])

    #create a puerto Rican Dataset and filter
    ds_current = ds["train"].select(range(start, end))



    pr_slang = []

    x = 0
    #extract the Puerto Rican sentences
    for example, metadata in zip(ds_current["text"], ds_current["metadata"]):
        for text_dict in example:
            for word in puerto_rican_slang:
                if word.lower() in text_dict["text"].lower():
                    pr_slang.append(text_dict["text"])
                    #continue so it doesn't make duplicates
                    continue
                
            if pr_domain(metadata["url"].lower()):
                pr_slang.append(text_dict["text"])
                print(f"Found Puerto Rican slang: {text_dict['text'], metadata['url']}")
        
        translate.load_bar(x, len(ds_current), example)
        x += 1
    
    return pr_slang

def pr_domain(domain):
    parse = urlparse(domain)
    return parse.hostname.endswith(".pr")


#execution
if __name__ == "__main__":
    try:
            
        #load Spanish oscar dataset
        ds = load_dataset("oscar-corpus/mOSCAR", "spa_Latn")

        #tokenizer = AutoTokenizer.from_pretrained(tokenizer)

        #slang words to filter in
        puerto_rican_slang = [ "perreo", "boricua",
            "wepa", "acho", "chacho", "diache", "boricua", "nene", "nena", "corillo", "cangri", "brutal", "mamey", "zafacón", "al garete", "jartera", "bregar", "breg", "janguear", "jangue", "gufear", "gufe", "pichear", "piche", "guagua", "bicho", "tiraera", "lengua suelta", "mano", "cantazo", "charro", "jíbaro", "feca", "taíno", "pichea", "jangueo", "bregando", "gufeo", "vacilón", "tostao", "tapón", "sanda", "rebuleo", "caco", "cafre", "lechón", "tirar", "mete mano", "bembé", "janguiar", "pelú", "tiradera", "pata abajo", "babilla", "gufiao", "zángano", "conuco", "maceta", "mamabicho", "bizcocho", "chillando goma", "encendío", "tripear", "mondongo", "algarete", "frontear", "motora", "nenes", "nenas", "cafrería", "melaza", "métele", "ñangotao", "ñemerson", "ñero", "pariseo", "paquetero", "pon", "ñoco", "ponte bruto", "rebulear", "rosca", "rocheliar", "sangana", "serrucho", "taparse", "tirar la mala", "tostón", "tumba eso", "vacilar", "vaso rojo", "yales", "zafao", "zángana", "zopenco", "abombao", "alcapurria", "aplatanao", "arroz con culo", "asicalao", "babear", "bacalao", "baratillo", "barriada", "bellaco", "bochinche", "brincacharcos", "bulto", "cabrón", "cantársela", "carecrimen", "chavos", "chichón", "chillin", "chiquistar", "chota", "cojines", "comelón", "concho", "craquear", "cuadrar", "darse el palo",
            "dar una pela", "de show", "empatar", "enganchaera", "esbaratáo", "fajao", "farfullero", 
            "fiestón", "gufiar", "gufiao", "huele bicho", "jacaroso", "jalcoroso", "la jodiste", 
            "lambeojo", "le mete", "loser", "mameyera", "matao", "meterle bellaco", "mona", "morón", 
            "no jodas", "pana", "papo", "pelabicho", "pelú", "por si las moscas", "quillao", 
            "ratón de ferretería", "rayao", "remeneo", "retumba", "salpafuera", "sandunguero", 
            "sin pena", "sopa'o", "tablazo", "te la echas", "te guillaste", "tirarte", "tirarse", 
            "tirau", "tripeo", "tú sabes", "una nota", "vacilársela", "vamos al mambo", 
            "vete al carajo", "vuélvete loco", "zafacón de gente", "¿Qué es la que hay?",
            "¿Cómo está la cosa?", "Vamos a darse un chance.", "No me compliques la vida.",
            "Eso está de show.", "Tira pa' acá.", "¿Dónde está el jangueo?", "Dale pa'lante.", "No te me achicopales.", "Estoy bien a gusto aquí.",
            "Esto está al pelo.", "Ponte pa' lo que viene.", "Tranquilo, que aquí nadie se raja.", "Eso no tiene pierde.", "No hay problema, mano.",
            "¿Quieres un chin?", "Voy a dar una vuelta.", "Me tiré una siesta.", "Esto es un vacilón.", "Estoy en la plena.", "¡Qué brutal!",
            "Eso es de pinga.",
            "Aquí se trabaja duro.",
            "No me hables na' más.",
            "Tú sabes cómo es la vuelta.",
            "Esto se puso bueno.",
            "Se me fue la mano.",
            "Esto está en candela.",
            "Voy a coger un chance.",
            "Tú eres una nota.",
            "No te me rajes ahora.",
            "Me fui pa'l trono.",
            "Echando pa'lante siempre.",
            "Se me olvidó el chin.",
            "Esto está bien encendío.",
            "Eso está brutal.",
            "¿Qué pasó, mi gente?",
            "Vamos a janguear un rato.",
            "Estoy cogiendo carrerilla.",
            "No hay mal que dure cien años.",
            "Esto está tirando pa'l piso.",
            "Dame un break.",
            "Estoy a punto de explotar.",
            "Eso está al garete.",
            "Aquí no se rinde nadie.",
            "Estoy alante con eso.",
            "Eso me tiene rayao.",
            "Eso fue un tremendo perreo.",
            "Me tienes de pana.",
            "Dame un toque.",
            "¿Qué es la que pasa?",
            "Estoy en candela con esto.",
            "Esto está a prueba de balas.",
            "Echando un pie.",
            "Eso está bien brutal.",
            "La vida es una nota.",
            "Estoy sin gota de energía.",
            "Echando un pie por ahí.",
            "Eso está para comérselo.",
            "Tú tienes un talento brutal.",
            "No te me pongas así.",
            "Estoy cagao de la risa.",
            "Eso está a otro nivel.",
            "Dale con calma.",
            "Aquí todo está chill.",
            "Tú eres un vacilón.",
            "Esto está para chuparse los dedos."

        ]


        #the list of slang
        pr_slang = []

        #run filter in steps so it doesn't crash
        for i in range(100):
            start = (len(ds["train"]) // 22) * i
            end = start + (len(ds["train"]) // 22)
            pr_slang.append(filter(ds, puerto_rican_slang, start, end))


    finally:

        with open("data/data-output/filtered_data.txt", "w", encoding="utf-8") as f:
            #make a text file with the filtered Puerto Rican slang examples
            for block in pr_slang:
                for example in block:
                    f.write(example + "\n")