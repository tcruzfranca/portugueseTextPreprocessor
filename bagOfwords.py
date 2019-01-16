import json
from Preprocessor import PreProcessor
import codecs

def contWordsInTweet(vetorPalavras):
    
    setPalavras = set(vetorPalavras)

    print (len(setPalavras))
    print (len(vetorPalavras))

    bagOfWords = {}
    for palavra in setPalavras:
        freqPalavra = vetorPalavras.count(palavra)
        bagOfWords.update({palavra:freqPalavra})

    return bagOfWords

def listOfAllWordsWithoutStopWords(arquivo,lang="pt-br"):

    listaOfWords = []
    preProcessor = PreProcessor()
    #cont = 0
    with open(arquivo) as arquivo:
        for linha in arquivo:
            #cont += 1
            #if cont > 200:
            #    break
            tweet = json.loads(linha)
            tweet = tweet['tweet_text']
            tweet = tweet.lower()
            tweet = preProcessor.remove_stopWords(tweet,lang)
            tweet = preProcessor.textFilter(tweet)
            tweet = preProcessor.removeNonAlphaNumericValues(tweet)
            listaOfWords.extend(tweet.split())
            #sugestão: substituir função lambda por list comprehension
            #listaOfWords = map(lambda x: x.replace(" ",""),listaOfWords)
            listaOfWords = [x.replace(" ","") for x in listaOfWords]
        '''
        for i in listaOfWords:
            if len(i)>20:
                print (i)
        '''
    return listaOfWords

def saveCSVFromBagOfWords(arq, bagOfWords,targetFile):

    for pal,freq in bagOfWords.items():
        arq.write(pal+", "+str(freq)+"\n")


if __name__ == "__main__":
    
    arq0 = open("collection_0.json")
    arq1 = open("collection_1.json")
    arq2 = open("collection_2.json")
    arq3 = open("collection_3.json")
    arq4 = open("collection_4.json")
    arq5 = open("collection_5.json")

    arquivos = [arq0,arq1,arq2,arq3,arq4,arq5]

    arqDestino = codecs.open("removeRetweets/targetFile.csv","w","utf-8")

    listaPalavras = []
    for arquivo in arquivos:
        listaPalavras.extend(listOfAllWordsWithoutStopWords(arquivo))

    bagOfWords = contWordsInTweet(listaPalavras)
    saveCSVFromBagOfWords(arqDestino, bagOfWords,"")

    arqDestino.close()

    print("FIM")





