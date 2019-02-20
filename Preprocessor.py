# -*- coding: utf-8 -*-
import re
import removeStopWords
import spacy
#import csv
from unicodedata import normalize
from ptstemmer.implementations.OrengoStemmer import OrengoStemmer
from ptstemmer.implementations.SavoyStemmer import SavoyStemmer
from ptstemmer.implementations.PorterStemmer import PorterStemmer

'''
    @authors
        Tiago Cruz de França
        Eduardo Freire Mangabeira
    @since
        03-23-2015
    @version 
        1.0.0
    @see
        https://github.com/tcruzfranca/annotatedDatasetBrazilianProtests
        This is a specific version made for turn easy the retrival of tweets from the Brazilian protests Golden Dataset.
        For a more generic version for retrival of tweets by id, access https://github.com/tcruzfranca/scripts.
    License (BSD 2): Available in https://github.com/tcruzfranca/annotatedDatasetBrazilianProtests/blob/master/LICENSE.txt.
    
    description 
                This code is useful for retrieval tweets usin list of tweet's IDs. Such list must be a file in which each ID is in a different line.
                In the end of this file you can see the main function and the instructions for set correctly the configurations needed.
    
    Please access the git address and cite at least one: our paper or the git account if we want use this script.
'''

class PreProcessor(object):

    def __init__(self):
        self.stopWords = []
        self.stopWordsOnlyASCIICharacteres = False
        self.stemmer = OrengoStemmer()
        self.stemmerType = "orengo"

    def removeNonAlphaNumericValues(self, text):

        text = re.sub('[^a-zA-Z0-9@]',' ',text)
        text = re.sub('\s{2,}',' ',text)
        return text


    def replaceNonASCIIcharacter(self, text, codif='utf-8'):
        '''
        Todos carateres não ASCII e não alfa-numéricos,
        (ex: bullets, travessões, etc.) 
        são removidos!
        '''
        return normalize('NFKD', text).encode('ASCII','ignore').decode(codif)


    def textFilter(self, text):
        '''
            Remove retweets, menções, url, espaços multiplo, tabulações, etc.
        '''
        text = text.lower()
        text = re.sub('([RT]|[rt]*\s*@[a-z]+)|(http([!a-z]|[^ \t\n\r\f\v]*))|([^a-zA-ZÀ-ú0-9\s])',' ',text)
        '''
        o intervalo À-ú para englobar todos os acentuados, ou ainda À-Ú e à-ú caso se queria só maiúsculas ou minúsculas.
            [[:lower:]]	[a-zà-ú]
            [[:upper:]]	[A-ZÀ-Ú]
            [[:alpha:]]	[A-Za-zÀ-ú]
        '''   
        return text.strip()


    def replaceTwoOrMore(self, text):
        '''
            Remove caracteres repetidos.
            Falta incluir exceções: ss, rr, ee e oo
        '''
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        findings = pattern.findall(text)
        #print (findings)
        return pattern.sub(r"\1", text)


    def replaceTwoOrMoreObservingPortugueseGrammarRules(self,text):
        pass


    def removeSmallWords(self, tweet, minSize = 2):
        '''
            Remove qualquer string menhor ou igual ao tamanho mínimo informado
        '''
        palavras = tweet.split()
        palavra = ""
        for pal in palavras:
            if len(pal) > minSize:
                palavra += pal+" "
        return palavra.strip()


    def _getStopWords(self,language="pt-br"):
        if len(self.stopWords) == 0:
            self.stopWords = removeStopWords.listStopWords(language)
        return self.stopWords


    def stopWordsWithoutNonASCIICharacteres(self,onlyASCII = True,language="pt-br"):
        if (self.stopWordsOnlyASCIICharacteres and onlyASCII):            
            pass
        elif (not(self.stopWordsOnlyASCIICharacteres) and onlyASCII):
            stop_words = self._getStopWords(language)
            self.stopWords = [self.replaceNonASCIIcharacter(str(i.encode("utf-8"))) for i in stop_words]
            self.stopWordsOnlyASCIICharacteres = True            
        elif (self.stopWordsOnlyASCIICharacteres and not onlyASCII):            
            self.stopWords = []
            self.stopWords = self._getStopWords(language)
            self.stopWordsOnlyASCIICharacteres = False
        else:
            self.stopWords = self._getStopWords(language)
        
        return onlyASCII

        

    def remove_stopWords(self, tweet, language="pt-br", list_stopWords=[]):
        '''
            Usado depois de remover pontuacoes do tweet.
            Remove stopwords do tweet com base na lista_stopWords criada em lista_de_stopWords(arquivo).
        '''
        listStopWords = []
        if len(list_stopWords) == 0:     
            listStopWords = self._getStopWords(language)
        else:
            listStopWords = list_stopWords

        listTokensTweet = tweet.split()
        text = ''
        for i in listTokensTweet:
            #print(i) 
            i.strip()    
            if i not in listStopWords:
                text += i+' '

        return text.strip()
    

    def _getStemmerObject(self, language="pt-br", approach="orengo"):

        if (approach != self.stemmerType):
        
            self.stemmerType = approach
            if approach == "orengo":
                self.stemmer = OrengoStemmer()
                
            if approach == "porter":
                self.stemmer = PorterStemmer()        

            if approach == "savoy":
                self.stemmer = SavoyStemmer()        

        return self.stemmer
            

    def stemming(self,palavras,language="pt-br", approach="orengo"):

        stemmer = self._getStemmerObject(language, approach)
        if type(palavras) is str:
            return stemmer.getWordStem(palavras)

        lista = []        
        for palavra in palavras:
            lista.append(stemmer.getWordStem(palavra))

        return lista


    def stemmingFrase(self,frase,language="pt-br", approach="orengo"):
        palavras = frase.split()
        palavras = self.stemming(palavras)
        text=""
        listStopWords = self._getStopWords(language)
        for i in palavras:
            # print (i)
            i.strip()    
            if i not in listStopWords:
                text += i+' '

        return text.strip()

    def lemmatizePhraseWithoutStopwords(self, frase, language="pt-br"):
        # é preciso baixar o modelo --> python3 -m spacy download pt

        languageAdapter = "pt"
        if language != "pt-br":
            languageAdapter = language

        nlp = spacy.load(languageAdapter)
        frase = nlp(frase)
        listStopWords = self._getStopWords(language)

        lista = [palavra.lemma_ for palavra in frase if palavra not in listStopWords]

        return lista

    def lemmatizePhraseWithoutStopwordsandPOS(self, frase, language="pt-br"):
        # é preciso baixar o modelo --> python3 -m spacy download pt

        languageAdapter = "pt"
        if language != "pt-br":
            languageAdapter = language

        nlp = spacy.load(languageAdapter)
        frase = nlp(frase)
        listStopWords = self._getStopWords(language, disable=['tagger'])

        lista = [palavra.lemma_ for palavra in frase if palavra not in listStopWords]

        return lista
        
    def lemmatizePhrase(self, frase, language="pt"):
        # é preciso baixar o modelo --> python3 -m spacy download pt
        nlp = spacy.load('pt')
        frase = nlp(frase)

        lista = [palavra.lemma_ for palavra in frase]

        return lista
        
    def lemmatize(self, word, language="pt"):
        
        nlp = spacy.load(language)
        word = nlp(word)

        lista = word[0].lemma_

        # return lista
        
        pass