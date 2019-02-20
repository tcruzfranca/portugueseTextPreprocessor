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


import json
#import datetime
from dateutil import parser

#arq0 = open("tiagosilva.json", 'r')

dicionario = {}

with open("tiagosilva.json", 'r') as arq:
#for arq in [arq0]:
    for tweet in arq:
        try:
            tweet = json.loads(tweet)
            data = tweet["tweet_created_at"]
            data = data.replace("-","")
            data = parser.parse(data)
            chave = str(data.day)+"-"+str(data.month)
            if chave in dicionario:
                dicionario.update({chave:dicionario.get(chave)+1})
            else:
                dicionario.update({chave:1})
        except:
            #algumas datas estão vazias
            pass

#arq_novo = open("freq_tweets.csv","w")
with open("freq_tweets.csv","w") as arq_novo:
    for i,j in dicionario.items():
        arq_novo.write(i+","+str(j)+"\n")

#arq0.close()
#arq_novo.close()
