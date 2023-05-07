# Task 3

This code loads and uses a trained NER (Named Entity Recognition) model to annotate the named entities in a given sentence.

Requirements:
Python 3.6 or higher
spaCy library

Installation:
Clone this repository

Install the required libraries using requirements.txt

Run ner_model_builder.ipynb

Run id_ners.py

About:

The above code contains three functions that are used to load and use a trained Named Entity Recognition (NER) model to annotate named entities in a given sentence.

load_model(model_path): This function loads a pre-trained NER model using the spaCy library. It takes one argument:

model_path (str): the path to the pre-trained NER model to be loaded.
The function returns the loaded NER model object.

annotate_sentence(nlp, sentence): This function annotates the named entities in a given sentence using the loaded NER model object. It takes two arguments:

nlp (object): the loaded NER model object returned by the load_model function.
sentence (str): the sentence to be annotated by the NER model.
The function returns a list of dictionaries, where each dictionary contains information about a named entity found in the sentence. Specifically, each dictionary has two keys:

label (str): the label assigned by the NER model to the named entity found in the sentence.
text (str): the text of the named entity found in the sentence.
__main__(): This is the main function that is executed when the script is run. It uses the argparse module to parse the command-line arguments passed to the script. Specifically, it takes two arguments:

model_path (str): the path to the pre-trained NER model to be loaded. This argument is required and specified as a positional argument.
sentence (str): the sentence to be annotated by the NER model. This argument is required and specified as a positional argument.
The function then loads the pre-trained NER model using the load_model function and annotates the given sentence using the annotate_sentence function. Finally, it prints the list of named entities found in the sentence.







