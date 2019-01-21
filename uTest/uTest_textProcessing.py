import json
from dateutil import parser
import codecs
import textProcessing as tpro
from Preprocessor import PreProcessor

'''
# O maior problema até agora aparentemente é com o uso da biblioteca dateutil

	# Quando se usa uma data do jeito que está no .json de um tweet, se tem a seguinte configuração:

		->  1:30 PM - 5 Oct 2018
		# o Python shell retorna o seguinte erro:
		> File "'DiretorioDoUsuário'/site-packages/dateutil/parser/_parser.py", line 648, in parse
    	> ValueError("Unknown string format:", timestr)
		> ValueError: ('Unknown string format:', '1:30 PM - 5 Oct 2018')

	# Fiz um teste sem o horário e o resultado foi o seguinte:

		>>> data = '5 Oct 2018'
		>>> print(parser.parse(data))
		2018-10-05 00:00:00
	
	# Como o horário é uma informação sensível, não acho que a melhor abordagem seja removê-lo

	*********** basta tirar o travessão que funciona
	>>> from dateutil import parser
	>>> data = '1:30 PM 5 Oct 2018'
	>>> print(parser.parse(data))
	2018-10-05 13:30:00

# Não funcionou a partir de um certo número de tweets
	>>> data = '1:30 PM - 5 Oct 2018'
	>>> data = data.replace("-","")
	>>> print(parser.parse(data))
	2018-10-05 13:30:00


'''


'''
# FUNCIONANDO
# Alterei o código para arquivo abrir no próprio método PARA FINS DE TESTE.
# Mudança acima já revertida.
datas = ['15-06-1998', '31-12-2012', '25-07-2001', '07-08-2016']
arquivo = "Datas_destino.txt"
tpro.saveDates(datas, arquivo)
'''


