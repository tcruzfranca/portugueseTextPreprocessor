# -*-coding:utf-8-*-
'''
testando removeStopWords.py

'''
from removeStopWords import _list_de_stopWords
from removeStopWords import listStopWords 

listStopWords()

with open("uTest/machado_alterado.txt", "w") as arq_saida:
	with open("uTest/assis_padrao.txt", "r") as arq_entrada:
		arq_saida.write(str(_list_de_stopWords(arq_entrada)))

