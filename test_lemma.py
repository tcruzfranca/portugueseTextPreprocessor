'''from spacy.lang.pt import Portuguese
from spacy.lang.pt.lemmatizer import LOOKUP

'''

import spacy
from spacy import displacy

frase = "Eu como aquela batata como os ingleses comem aquela batata."
nlp = spacy.load('pt')
frase = nlp(frase)
print([(token,token.pos_) for token in frase])
