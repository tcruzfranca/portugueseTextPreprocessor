# -*- coding: utf-8 -*-

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


import Preprocessor

def preProcessingMessages(PreProcessor, message, removeNonASCIIFromMessage=False,   
                         removeNonAlphaNumericValues=True, replaceNonASCIIFromStopWords=True, 
                         remove_stopWords=True, text_filter=True, replaceTwoOrMore=True, 
                         removeSmallWords=True, stemmingFrase = True):

    '''
        Preprocessor has a non functional method 'replaceTwoOrMoreObservingPortugueseGrammarRules'
    '''
   
    if removeNonASCIIFromMessage:
        message = PreProcessor.replaceNonASCIIcharacter(message)
   
    if removeNonAlphaNumericValues:
        message = PreProcessor.removeNonAlphaNumericValues(message)
    
    PreProcessor.stopWordsWithoutNonASCIICharacteres(replaceNonASCIIFromStopWords)
     
    if remove_stopWords:
        message = PreProcessor.remove_stopWords(message)     
    
    if text_filter:
       message = PreProcessor.textFilter(message) 
    
    if replaceTwoOrMore:
        message = PreProcessor.replaceTwoOrMore(message)
   
    if removeSmallWords:
        message = PreProcessor.removeSmallWords(message)
    
    if stemmingFrase:
        message = PreProcessor.stemmingFrase(message)
    
    return message


def oneFilePerMessage(PreProcessor,folder,arquivos):
    '''
        If message is a tweet, a file per tweet.
    '''
    contTweetsFileName = 0
    for arquivo in arquivos:
        with open(folder+arquivo) as arq:
        #CONSERTAR ESTE BLOCO INTEIRO.
            for message in arq:
                salvar = open(folder+arquivo+"_preprocessado", "w")
                #salvar = open(folder+arquivo, "r") # + "s/"+str(contTweetsFileName),"w")
                message = preProcessingMessages(PreProcessor, message)
                salvar.write(message)
                contTweetsFileName+=1
                salvar.close()

def oneFilePerMessageWithoutStemming(PreProcessor,folder,arquivos):
    '''
        If message is a tweet, a file per tweet.
    '''
    contTweetsFileName = 0
    for arquivo in arquivos:

        arq = open(folder+arquivo)
        
        for message in arq:
            salvar = open(folder+arquivo, "w") # + "s/"+str(contTweetsFileName),"w")
            message = preProcessingMessages(PreProcessor, message,stemmingFrase = False)
            salvar.write(message)
            contTweetsFileName+=1
            salvar.close()

def prepararBasesTreinoTeste(PreProcessor):
    '''
        Depois, se quiser centralizar configuracoes, passar folder e nomes das classes.
        Nome das classes igual ao nome dos arquivos onde se encontram os dados para treino e teste
        cada arquivo uma classe
    '''
    folder = "/home/edu/portugueseTextPreprocessor/Treinamento/BaseTreinoTeste/"
    # arquivos = ["VHVL","HVL","MVL","LVL","NVI"]
    arquivos = ["palestrinha.json"]    
    oneFilePerMessage(PreProcessor,folder,arquivos)
'''
def prepararBasesTreinoTesteWithoutStemming(PreProcessor):
    
        Depois, se quiser centralizar configuracoes, passar folder e nomes das classes.
        Nome das classes igual ao nome dos arquivos onde se encontram os dados para treino e teste
        cada arquivo uma classe
    
    folder = "/home/edu/portugueseTextPreprocessor/Treinamento/BaseTreinoTesteSemStemming/"
    arquivos = ["VHVL","HVL","MVL","LVL","NVI"]    
    oneFilePerMessageWithoutStemming(PreProcessor,folder,arquivos)
'''

def prepararBasesTreinoTestePorJanela(PreProcessor):
    '''
        Depois, se quiser centralizar configuracoes, passar folder e nomes das classes.
        Nome das classes igual ao nome dos arquivos onde se encontram os dados para treino e teste
        cada arquivo uma classe
    '''
    folder = "/home/edu/portugueseTextPreprocessor/Treinamento/BaseTreinoTeste/porJanela/"
    arquivos = ["VHVL","HVL","MVL","LVL","NVI"]    
    oneFilePerMessage(PreProcessor,folder,arquivos)

def prepararBase(PreProcessor):
    print ("nao ta fazendo nada, use apenas preProcessingMessages() a cada mensagem durante a classificacao!!! ao invés de preprocessar toda base")

def menu():
    PreProcessor = Preprocessor.PreProcessor()
    opcao = input("Preparar base de treino e teste yes/No?")
    if opcao.lower() in ["yes","y"]:
        prepararBasesTreinoTeste(PreProcessor)

    opcao = input("Preparar base de treino e teste sem stemming yes/No?")
    if opcao.lower() in ["yes","y"]:
        prepararBasesTreinoTesteWithoutStemming(PreProcessor)

    PreProcessor = Preprocessor.PreProcessor()
    opcao = input("Preparar base de treino e teste da pasta de janelas Yes/no?")
    if opcao.lower() in ["","yes","y"]:
        prepararBasesTreinoTestePorJanela(PreProcessor)

    opcao = input("Preparar base Yes/no (não uso, pre-processo a mensagem antes de classificar):")    
    if opcao.lower() in ["","yes","y"]:
        prepararBase(PreProcessor)

if __name__=="__main__":
    menu()
    print ("FIM um tweet por Arquivo")
