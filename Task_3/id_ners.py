import spacy
import argparse

def load_model(model_path):
    nlp = spacy.load(model_path)
    return nlp

def annotate_sentence(nlp, sentence):
    doc = nlp(sentence)
    entities = []
    for ent in doc.ents:
        entities.append({'label': ent.label_, 'text': ent.text})
    return entities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load and use a trained NER model')
    parser.add_argument('model_path', type=str, help='Path to the model to load')
    parser.add_argument('sentence', type=str, help='Sentence to annotate')
    args = parser.parse_args()
    
    nlp = load_model(args.model_path)
    entities = annotate_sentence(nlp, args.sentence)
    print(entities)
