# -*- coding: utf-8

def _list_de_stopWords(arquivo):
    '''
        carrega lista de stopwords de arquivo.
        padrão utf-8
    '''
    lista = []

    for stop_word in arquivo:
        stop_word = stop_word.lower()
        stop_word = stop_word.replace('\n','')
        stop_word = stop_word.replace('\r','')
        lista.append(str(stop_word))

    return lista  

def listStopWords(language="pt-br", f="stopwords_pt.txt"):

    arquivo = ""
    if language == "pt-br":
        arquivo = open(f)
    else:
        print("Inclua a lista e altere o método listStopWords em removeStopWords")

    return _list_de_stopWords(arquivo)
