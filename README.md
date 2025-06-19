
# refined-translate
Translate english to Puerto Rican Spansih

# Dataset
The dataset used can be found on Hugging Face. https://huggingface.co/datasets/Sephdude/esPR-en
It contains Puerto Rican spanish text from various sources and automatically generated english translations using the Heslinki-OPUS-MT-ES-EN model.

# How it was made
The translator is a fine-tuned version of the Helsinki-NLP OPUS-MT-EN-ES trained on formal Puerto Rican spanish text and english translations, then seperately trained on colloquial translations to make the translationator more casual. A style marker lets the user decide which data the model is trained on.
## References

- Hugging Face, *Transformers: State-of-the-art Natural Language Processing for Pytorch and TensorFlow 2.0*, 2023. [https://huggingface.co/transformers/](https://huggingface.co/transformers/)
- Helsinki-NLP, *OPUS-MT: English to Spanish translation model*, 2020. [https://huggingface.co/Helsinki-NLP/opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es)
