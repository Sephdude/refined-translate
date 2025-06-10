#!/usr/bin/env python3

from transformers import AutoModelForSeq2SeqLM, trainer, PreTrainedTokenizer

#model to be trained
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")


