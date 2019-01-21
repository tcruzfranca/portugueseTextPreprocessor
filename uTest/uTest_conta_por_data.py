# -*-encoding: utf-8 -*-
import json
#import datetime
from dateutil import parser
import re

'''
# Não funcionou a partir de 60 tweets
    >>> data = '1:30 PM - 5 Oct 2018'
    >>> data = data.replace("-","")
    >>> print(parser.parse(data))
    2018-10-05 13:30:00

Traceback (most recent call last):
  File "conta_por_data.py", line 15, in <module>
    data = parser.parse(data)
  File "/home/edu/.local/lib/python3.5/site-packages/dateutil/parser/_parser.py", line 1356, in parse
    return DEFAULTPARSER.parse(timestr, **kwargs)
  File "/home/edu/.local/lib/python3.5/site-packages/dateutil/parser/_parser.py", line 651, in parse
    raise ValueError("String does not contain a date:", timestr)
ValueError: ('String does not contain a date:', '')

# Pode ser um tweet editado por engano.

 ## Testei duas abordagens: split/join e replace. AS DUAS formas pararam no tweet 60 com o erro de formato
    de tempo inválido.

'''
k = 0
with open("tiagosilva.json", 'r') as arq:
    for tweet in arq:
        
        try:
            tweet = json.loads(tweet)
            print(json.dumps(tweet))

            data = tweet["tweet_created_at"]
            data_split = []
            data_split = data.split('-')
            data = " ".join(data_split)
            #data = data_split[0] + data_split[1]
            print(data)
            '''data = data.replace("-","")
            print(data)
            '''
            data = parser.parse(data)
            print(data)
            k = k + 1
            print(k)
        except:
            pass