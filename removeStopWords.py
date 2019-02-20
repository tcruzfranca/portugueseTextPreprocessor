# -*- coding: utf-8

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
