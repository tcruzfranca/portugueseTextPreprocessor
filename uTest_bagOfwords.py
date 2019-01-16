import bagOfwords as bw
import codecs

'''
# FUNCIONANDO sem alterações
vetor = ["Banana", "Beterraba", "Cenoura", "Alface", "Inhame", "Rúcula"]
print(bw.contWordsInTweet(vetor))
'''


'''
# (Resolvido)JSONDecodeError
	# Abri o arquivo com 'with open'
# (Resolvido)'map' object has no attribute 'list'
	# Troquei lambda por list comprehension 
arquivo = "tiagosilva.json"
print(bw.listOfAllWordsWithoutStopWords(arquivo))
'''

'''
# FUNCIONANDO sem alterações
arqDestino = codecs.open("targetFile.csv","w","utf-8")
listaPalavras = ["Banana", "Beterraba", "Cenoura", "Alface", "Inhame", "Rúcula"]
bagOfWords = bw.contWordsInTweet(listaPalavras)
bw.saveCSVFromBagOfWords(arqDestino, bagOfWords,"")
'''