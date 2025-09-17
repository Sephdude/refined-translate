#!/usr/bin/env python3


from datasets import load_dataset

#load the mOSCAR dataset from Huggingface
ds = load_dataset("oscar-corpus/mOSCAR", "spa_Latn", split="train")

ds.save_to_disk("data_files/mOSCAR_spa_Latn")