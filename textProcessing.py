# -*- coding: utf-8 -*-
import json
from dateutil import parser
import codecs
from Preprocessor import PreProcessor

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


def saveDates(datas, destino):

    datas = list(set(datas))
    datas.sort()
    for data in datas:
        destino.write(data+"\n")

    return datas


def tweetsAgrupadosPorData(arquivos, pathDestination):

    data = "vazio"
    dataNome = data
    destino = codecs.open(pathDestination+dataNome,"w","utf-8")
    datas = []
    for arq in arquivos:
        for linha in arq:
            tweet = json.loads(linha)
            try:
                created_at = tweet['tweet_created_at']
                created_at = created_at.replace("-","")
                created_at = parser.parse(created_at)
                created_at = str(created_at.day)+"-"+str(created_at.month)
            except:
                print(tweet)
                continue
            
            if data != created_at:
                destino.close()
                data = created_at
                dataNome = data+".json"
                destino = codecs.open(pathDestination+dataNome,"a","utf-8")
                if created_at not in datas:
                    datas.append(created_at)

            destino.write(linha)# .decode("utf-8"))
    destino.close()
    return datas

def wordNetWithTweets(datas, pathDestination, pathDestinationWordNet):
    
    preProcessor = PreProcessor()

    for data in datas:
        data = data.replace("\n","")
        dataNome = data+".csv"
        arq = open(pathDestination+dataNome)
        destino = codecs.open(pathDestinationWordNet+dataNome,"a","utf-8")
        for linha in arq:
            tweet = json.loads(linha)
            #created_at = tweet['created_at']
            #created_at = parser.parse(created_at)
            #created_at = str(created_at.day)+"-"+str(created_at.month)
            text = tweet["tweet_text"]
            text = text.lower()
            text = preProcessor.textFilter(text)
            text = preProcessor.removeNonAlphaNumericValues(text)
            text = preProcessor.remove_stopWords(text)
            text = text.strip()
            #text = text.replace(" ",",")
            destino.write(text+"\n")

        arq.close()
        destino.close()

    destino.close()

def wordNetWithTweetsStemming(datas, pathDestination, pathDestinationWordNet):
    
    preProcessor = PreProcessor()

    for data in datas:
        data = data.replace("\n","")
        dataNome = data+".json"
        arq = open(pathDestination+dataNome)
        destino = codecs.open(pathDestinationWordNet+dataNome,"a","utf-8")
        for linha in arq:
            tweet = json.loads(linha)
            #created_at = tweet['tweet_created_at']
            #created_at = created_at.replace("-","")
            #created_at = parser.parse(created_at)
            #created_at = str(created_at.day)+"-"+str(created_at.month)
            text = tweet["tweet_text"]
            text = text.lower()
            text = preProcessor.textFilter(text)
            text = preProcessor.removeNonAlphaNumericValues(text)
            text = preProcessor.remove_stopWords(text)
            text = preProcessor.replaceNonASCIIcharacter(text)
            text = preProcessor.stemmingFrase(text)
            text = text.strip()
            #text = text.replace(" ",",")
            destino.write(text+"\n")

        arq.close()
        destino.close()

    destino.close()


def bagfOfWords(datas, pathDestination, pathBagOfWords):
    
    for data in datas:
        data = data.replace("\n","")
        dataNome = data+".csv"
        arq = open(pathDestination+dataNome)
        destino = codecs.open(pathBagOfWords+dataNome,"a","utf-8")
        listaPalavras=[]
        for linha in arq:
            text = linha.split(",")
            listaPalavras.extend(text)

        setPalavras = set(listaPalavras)
        dicionario = {}
        for pal in setPalavras:
            qtde = listaPalavras.count(pal)
            dicionario.update({pal:qtde})

        for chave,qtde in dicionario.items():
            text = chave+","+str(qtde)
            destino.write(text+"\n")

        arq.close()
        destino.close()

def bagfOfWordsStemming(datas, pathDestination, pathBagOfWordsStemming):
    
    for data in datas:
        data = data.replace("\n","")
        dataNome = data+".csv"
        arq = open(pathDestination+dataNome)
        destino = codecs.open(pathBagOfWordsStemming+dataNome,"a","utf-8")
        listaPalavras=[]
        for linha in arq:
            text = linha.split(",")
            listaPalavras.extend(text)

        setPalavras = set(listaPalavras)
        dicionario = {}
        for pal in setPalavras:
            qtde = listaPalavras.count(pal)
            dicionario.update({pal:qtde})

        for chave,qtde in dicionario.items():
            text = chave+","+str(qtde)
            destino.write(text+"\n")

        arq.close()
        destino.close()


if __name__ == "__main__":

    
    arq0 = open("tiagosilva.json")        
    arquivos = [arq0]
    
    
    pathDestination = "/home/edu/portugueseTextPreprocessor/Save_by_Date/"
    datas = tweetsAgrupadosPorData(arquivos, pathDestination)
    
    datasDestino = open(pathDestination+"datas.txt","w+")
    saveDates(datas, datasDestino)
    datasDestino.close()
    
    '''
    #temp
    pathDestination = "./tweetsPorData/"
    datasDestino = open(pathDestination+"datas.txt")
    tweetsAgrupadosPorData(datasDestino,pathDestination)

    datasDestino.seek(0)    
    datasDestino = open(pathDestination+"datas.txt")
    pathDestinationWordNet = "./separacaoWordNetWithouStopWords/"
    wordNetWithTweets(datasDestino, pathDestination, pathDestinationWordNet)
    
    datasDestino.seek(0)
    pathDestinationWordNet = "./separacaoWordNetWithouStopWordsStemming/"
    wordNetWithTweetsStemming(datasDestino, pathDestination, pathDestinationWordNet)
    
    datasDestino.seek(0)
    pathDestination = "./separacaoWordNetWithouStopWords/"
    #pathDestination = "./separacaoData/"
    pathDestinationBagOfWords = "./bagOfWords/"
    bagfOfWords(datasDestino, pathDestination, pathDestinationBagOfWords)
    
    datasDestino.seek(0)
    pathDestination = "./separacaoWordNetWithouStopWordsStemming/"
    pathDestinationBagOfWordsStemming = "./bagOfWordsStemming/"
    bagfOfWordsStemming(datasDestino, pathDestination, pathDestinationBagOfWordsStemming)
    '''

    #datasDestino.close()
    arq0.close()

    print("FIM")



