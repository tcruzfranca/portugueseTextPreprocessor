'''from spacy.lang.pt import Portuguese
from spacy.lang.pt.lemmatizer import LOOKUP

'''
from Preprocessor import PreProcessor

prep = PreProcessor()

frase = "Eu como aquela batata como os ingleses comem aquela batata sintática."
k = prep.remove_stopWords(frase)
print(k)
w = prep.lemmatizePhraseWithoutStopwordsandPOS(frase)
print(w)
z = prep.lemmatizePhraseWithoutStopwords(frase)
print(z)
j = prep.lemmatizePhrase(frase)
print(j)
