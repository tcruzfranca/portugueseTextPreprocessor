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
