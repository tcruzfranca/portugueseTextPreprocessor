import json
#import datetime
from dateutil import parser

arq0 = open("tiagosilva.json")

dicionario = {}

for arq in [arq0]:
    for tweet in arq:
        tweet = json.loads(tweet)
        data = tweet["tweet_created_at"]
        # não está sendo possível parsear a data
        data = parser.parse(data)
        chave = str(data.day)+"-"+str(data.month)
        if (dicionario.has_key(chave)):
            dicionario.update({chave:dicionario.get(chave)+1})
        else:
            dicionario.update({chave:1})

arq_novo = open("freq_tweets.csv","w")
for i,j in dicionario.items():
    arq_novo.write(i+","+str(j)+"\n")

arq0.close()

arq_novo.close()
