'''from spacy.lang.pt import Portuguese
from spacy.lang.pt.lemmatizer import LOOKUP

'''

import spacy

frase = "eu adoro caminhar caminhando na mata caminhada por o caminho caminhado por o caminhão de josé joão"
nlp = spacy.load('pt')


frase = nlp(frase)
lista = [(palavra.orth_, palavra.pos_) for palavra in frase]
#lista = [palavra.lemma_ for palavra in frase]

print(lista)