# -*-coding: utf-8 -*-
import re
from Preprocessor import PreProcessor 
prep = PreProcessor()

with open("uTest/assis_padrao.txt", "r") as arq_entrada:
	with open("uTest/machado_alterado.txt", "w") as arq_saida:
		'''
		# FUNCIONANDO sem alterações
		text = prep.removeNonAlphaNumericValues(str(arq_entrada.read()))
		'''


		'''
		# FUNCIONANDO
		# [Resolvido]'str' object has no attribute 'decode'
		# O processo correto em python 3 é: string -> bytes -> string

		text = prep.replaceNonASCIIcharacter(str(arq_entrada.read()))
		arq_saida.write(text)
		'''


		'''
		# FUNCIONANDO sem alterações
		text = prep.textFilter(str(arq_entrada.read()))
		arq_saida.write(text)
		'''


		'''
		# FUNCIONANDO sem alterações
		text = prep.replaceTwoOrMore(str(arq_entrada.read()))
		arq_saida.write(text)
		'''


		'''
		# FUNCIONANDO sem alterações
		text = prep.removeSmallWords(str(arq_entrada.read()), 3)
		arq_saida.write(text)
		'''

		'''
		# FUNCIONANDO sem alterações
		print(prep._getStopWords())
		'''

		''' 
		*** Ainda não tenho certeza do que essa função deve me retornar
		print(prep.stopWordsWithoutNonASCIICharacteres())
		'''
		'''
		# FUNCIONANDO sem alterações
		text = prep.remove_stopWords(str(arq_entrada.read()))
		arq_saida.write(text)
		'''


		
		# FUNCIONANDO sem alterações
		text = prep.stemming("lambança")
		print(text)

		'''

		
		# Não sei se a stemização está correta, preciso ler mais sobre
		stem = prep.stemmingFrase("O rato roeu a roupa do rei de Roma. Socorram-me subi no ônibus em Marrocos.")
		print(stem)
		
		'''





