import json
from Preprocessor import PreProcessor
import codecs


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





