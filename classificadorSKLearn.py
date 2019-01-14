# -*- coding: utf-8 -*-
from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer #bag of words
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import KFold
import numpy as np
from sklearn import metrics
import json
from umtweetPorArquivo import preProcessingMessages
from Preprocessor import PreProcessor

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

from sklearn.grid_search import GridSearchCV


def datasetTrainTest(folder,categories=['positives','negatives','neutrals']):    
    train_set = load_files(folder,categories=categories,shuffle=True)
    return train_set

def testBetterParameters(train_set, classifiers=[],classifier_names=[],alphas=(1,1e-1,1e-2,1e-3)):

    for clf in classifiers:

        try:
            if len(classifier_names) > 0:
                print ("classifier_names[classifiers.index(clf)]")
        except ValueError:
            print ("No name for classifier. Some mistake happens.")
        
        '''
            quoted from scikit learn site
            run an exhaustive search of the best parameters on a grid of possible values. We try out all classifiers on either 
            words, bigrams, with or without tf-idf, and with a penalty parameter of either 1, 0.1, 0.01 or 0.001
            default values
        '''
        parameters = {'vect__ngram_range': [(1,4),(1,2),(1,3),(1,1)],'tfidf__use_idf': (True, False),'clf__alpha': (alphas)}
        
        '''
            quoted from scikit learn site
            The search can be expensive. Multiple CPU cores we could use the grid searcher to try these eight parameter 
            combinations in parallel with the n_jobs parameter. If we give this parameter a value of -1, grid search will detect 
            how many cores are installed.
        '''
        gs_clf = GridSearchCV(clf, parameters, n_jobs=-1)

        
        '''
            seting data_set to grid
        '''        
        gs_clf.fit(train_set.data, train_set.target)

        '''
            quoted from scikit learn site
            The result of calling fit on a GridSearchCV object is a classifier that we can use to predict:
        '''
        #twenty_train.target_names[gs_clf.predict(['God is love'])]
        
        '''
            quoted from scikit learn site
            but otherwise, it’s a pretty large and clumsy object. We can, however, get the optimal parameters out by inspecting 
            the object’s grid_scores_ attribute, which is a list of parameters/score pairs. To get the best scoring attributes, 
            we can do:
        '''
        best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
        for param_name in sorted(parameters.keys()):
            print("%s: %r" % (param_name, best_parameters[param_name]))
             
        print(score)                                              
        #print (best_score)

def multinomialNaivaBayesClassifier(ngram=(1,5)):
    return Pipeline([('vect', CountVectorizer(ngram_range=ngram)),('tfidf', TfidfTransformer()),('clf', MultinomialNB(alpha=1e-1))])

def BernoulliNaivaBayesClassifier(ngram=(1,4)):
    #ref http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html#sklearn.naive_bayes.BernoulliNB
    return Pipeline([('vect', CountVectorizer(ngram_range=ngram)),('tfidf', TfidfTransformer()),('clf', BernoulliNB(alpha=1e-1))])

def svmSGDClassifier(ngram=(1,4)):
    #return Pipeline([('vect', CountVectorizer(ngram_range=(1,2))),('tfidf', TfidfTransformer()),
    #                ('clf', SGDClassifier(alpha=1e-3, n_iter=5,shuffle=False))]) #1e-3 = 0.001, ANTIGO, melhor sem tfidf
    return Pipeline([('vect', CountVectorizer(ngram_range=ngram)),
                    ('clf', SGDClassifier(alpha=1e-3,penalty='l2'))])#n_iter=5 é o default, alpha=1e-3 ,random_state=42
    #shuffle = False, melhorou, penalty='elasticnet'

def svmSVCClassifier():#I could not do it work for text classifier
    return Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),
                    ('clf', SVC())]) #SVC(kernel='linear')

def iterations(n,train_set):    
    '''
        Using train_set.data to get the length of the dataSet
        Generate a k-fold subsets for being used in cross validation
        Size of k is defined by n parameter
    '''  
    #X = np.array([[tweet] for tweet in train_set.data])
    kf = KFold(len(train_set.data), n_folds=n)
    return kf

def crossValidation(kf,train_set,clf,clf_name,pathDestination):
    text_clf = clf

    data = np.array(train_set.data)
    target = np.array(train_set.target)

    destination = open(pathDestination+clf_name+".csv",'w')
    destination2 = open(pathDestination+clf_name+'2'+".csv",'w')
    destination_conf_matrix = open(pathDestination+clf_name+'MatrizConfusao','w')
    destination_report = open(pathDestination+clf_name+'Report','w')

    accuracy = list()
    precision = list()
    recall = list()
    f_score = list()
    support = list()
    destination.write('acuracia,precisao,recall,f1-score\n')
    destination2.write('precisao,recall,f1-score,support\n')
    for train,test in kf:        
        text_clf = text_clf.fit(data[train], target[train])
        predicted = text_clf.predict(data[test])        
        acuracia = np.mean(predicted == target[test])
        accuracy.append(acuracia)

        destination.write(str(np.mean(predicted == target[test]))+',')
        destination.write(str(metrics.precision_score(target[test], predicted,average='weighted'))+',')
        destination.write(str(metrics.recall_score(target[test], predicted,average='weighted'))+',')
        destination.write(str(metrics.f1_score(target[test], predicted,average='weighted'))+'\n')

        destination2.write(str(metrics.precision_recall_fscore_support(target[test], predicted,average='weighted'))+"\n")

        precision.append(metrics.precision_score(target[test], predicted,average='weighted'))
        recall.append(metrics.recall_score(target[test], predicted,average='weighted'))
        f_score.append(metrics.f1_score(target[test], predicted,average='weighted'))
        #support.append(metrics.classification_report(target[test], predicted)) #PRECISION_RECALL... RETORNA a matriz de confusao

        destination_report.write(str(metrics.classification_report(target[test], predicted,target_names=train_set.target_names))+"\n")
        destination_conf_matrix.write(str(metrics.confusion_matrix(target[test], predicted))+"\n")

    
    accuracy = np.array(accuracy)
    precision = np.array(precision)
    recall = np.array(recall)
    f_score = np.array(f_score)
    #matrizConfusao = np.array(support)

    
    #print ("matrizConfusao:",matrizConfusao)
    print ("ACCURACY:",accuracy)
    print("Accuracy Mean: %0.2f (+/- %0.2f)" % (accuracy.mean(), accuracy.std() ))
    print ("PRECISION:",precision)
    print("Precision Mean: %0.2f (+/- %0.2f)" % (precision.mean(), precision.std() ))
    print ("RECALL:",recall)
    print("Recall Mean: %0.2f (+/- %0.2f)" % (recall.mean(), recall.std() ))
    print ("F_SCORE:",recall)
    print("f_score Mean: %0.2f (+/- %0.2f)" % (f_score.mean(), f_score.std() ))
    
    destination.close()
    destination2.close()
    destination_conf_matrix.close()
    destination_report.close()


def classifierTrain(train_set,clf):
    data = np.array(train_set.data)
    target = np.array(train_set.target)
    text_clf = clf.fit(data, target)
    return clf

def classifyOneMessage(train_set,cls, message):
    message = [message]
    message = np.array(message)    
    predicted = cls.predict(message)
    predicted = train_set.target_names[predicted]
    return predicted

def classMessages(train_set,clf,messages,date):#falta o retorno
    messages = np.array(messages)
    predicted = clf.predict(messages)
    
    '''
    Os diretorios sao temporarios para finalizar as analises
    Salvar as mensagens por dia tambem
    '''
    #positiveFile = open("timeWindowFunc/positive/"+date,"w")
    #negativeFile = open("timeWindowFunc/negative/"+date,"w")

    VHVL,HVL,MVL,LVL,NVI = 0,0,0,0,0
    for doc, category in zip(messages, predicted):
        if train_set.target_names[category] == 'VHVLs':            
            VHVL += 1
        elif train_set.target_names[category] == 'HVLs':
            HVL += 1
            #positiveFile.write(doc+'\n')
        elif train_set.target_names[category] == 'MVLs':
            MVL += 1
        elif train_set.target_names[category] == 'LVLs':
            LVL += 1
        else:
            NVI += 1
            #negativeFile.write(doc+'\n')

    #positiveFile.close()
    #negativeFile.close()
    return {'VHVL':VHVL,'HVL':HVL,'MVL':MVL, 'LVL':LVL, 'NVI':NVI}

def evaluateAllTweetMessages(train_set,clf, folderData, folderResultsAnalysis):

    '''
        Params:
        "clf" that is a method to tweets classification
        "folderData" where are files separated by data which have has also a file data.txt with name of all files one per line
        "folderResultsAnalysis" where will be saved the analyzes grouped by day
    '''
    arq_results = open(folderResultsAnalysis+"sentimentsEveryDay.csv","w")    
    arq_results.write("date,VHVL,HVL,MVL,LVL,NVI\n")

    arq_date = open(folderData+"datas.txt")
    cont = 0
    for date in arq_date:
        cont += 1
        print(cont)
        date = date.replace("\n","")
        arq_tweets = open(folderData+date+".json")
        
        tweets_list = []
        for linha in arq_tweets:
            tweet = json.loads(linha)
            '''
                Tweet preprocessing
            '''
            message = tweet['text']
            message = preProcessingMessages(PreProcessor(), message.encode("utf-8"))
            tweets_list.append(message)

        results = classMessages(train_set,clf,tweets_list,date)
        result = str(date)+","+str(results['VHVL'])+","+str(results['HVL'])+","+str(results['MVL'])+","+str(results['LVL'])+","+str(results['NVI'])+"\n"
        
        arq_results.write(result)

        arq_tweets.close()
        

    arq_date.close()
    arq_results.close()

def get_train_set(folderTrainTest = "BaseTreinoTeste",categories = ['positives','negatives','neutrals']):        
    train_set = datasetTrainTest(folderTrainTest,categories)
    return train_set

def get_train_set_without_stemming(folderTrainTest = "BaseTreinoTesteSemStemming", categories = ['positives','negatives','neutrals']):
    
    train_set = get_train_set(folderTrainTest,categories)
    return train_set


if __name__=="__main__":
    '''
        Pegando mensagens para treino e teste dentro do diretorio folderTrainTest
        Cada mensagem percisa esta dentro de um arquivo separado, cada arquivo 
        dentro de um folder com o nome da classe a qual pertence o arquivo.
        Ver arquivo "umtweetPorArquivo" utilizado para gerar esses diretorios
            em "umtweetPorArquivo" os dados recebem o preprocessamento
        datasetTrainTest retorna "train_set" com todos os dados rotulados manualmente
        train_set uma matriz com os dados e outra correspondente contendo as classes de cada dado
    '''
    train_set = get_train_set(categories = ['VHVLs','HVLs','MVLs','LVLs','NVIs'])#se dados estiverem em outra base, mudar funcao para pegar nova base de treino/teste
    #train_set = get_train_set_without_stemming(categories = ['VHVLs','HVLs','MVLs','LVLs','NVIs'])#base sem stemming

    opcao = input("Test parameters for classifiers?(yes/No):")
    if opcao.lower() in ["yes","y"]:
        '''
            Instantiating classifiers
        '''
        pipeline_params = [('vect', CountVectorizer()),('tfidf', TfidfTransformer())]
        
        pipeline_paramsMultNomBayes = pipeline_params[:]
        pipeline_paramsMultNomBayes.append(('clf',MultinomialNB()))
        multinomialNaiveBayes = Pipeline(pipeline_paramsMultNomBayes)

        pipeline_paramsBernBayes = pipeline_params[:]
        pipeline_paramsBernBayes.append(('clf',BernoulliNB()))
        bernoulliNaiveBayes = Pipeline(pipeline_paramsBernBayes)

        pipeline_paramsSGDClassifier = pipeline_params[:]
        pipeline_paramsSGDClassifier.append(('clf',SGDClassifier()))
        svmSGD = Pipeline(pipeline_paramsSGDClassifier)

        #svmSVC is worse than other tree "SVM SVC linear kernel"
        #svmSVC = svmSVCClassifier()#"better to unbalanced classes samples" (i have few negatives samples) according scikit learn

        print ("Testing better parrameters for classifiers")
        classifiers_names = ["multinomial Naive Bayes","Bernoulli Naive Bayes","SVM LinearSGD"]
        testBetterParameters(train_set,[multinomialNaiveBayes,bernoulliNaiveBayes,svmSGD],classifiers_names)
        print ("Fim dos testes de parâmetros")
        print ("You could take the best parameter obtained and change pipeline for each classifier.")
    else:
        print ("You must previously know the better parameter for each classifier.")

    opcao = input("Cross Validation Evaluation using kfolds?(yes/No):")
    if opcao.lower() in ["yes","y"]:

        print ("Cross Validation")
        '''
            Train & Test using k-folds
            k = num de k folds for iteraction train/test
            train_set vai ser utilizado apenas para se identificar o tamanho da amostra
            k fatias da amostra serao retornadas e podem ser utilizadas de forma intercalada.
            A cada rodada um fatia e separada para test e as outras serao usadas para treino
            O classificador prepara(treina com k-1 folds) e testa com o folder restante
            Uma media da acuracia, precisao, recall e f_scores sao calculados bem 
            como o desvio padrao da media
        '''
        k = 30 #n_folds  
        kf = iterations(k,train_set)#return a object k-
        
        pathDestination = "resultadosAnalises/"
        
        print ("SVM")
        

        print ("multinomialNaiveBayes")
        multinomialNaiveBayes = multinomialNaivaBayesClassifier()
        crossValidation(kf,train_set,multinomialNaiveBayes,"multinomialNaiveBayes",pathDestination)
        
        print ("\n\nBernoulliNaiveBayes")
        bernoulliNaiveBayes = BernoulliNaivaBayesClassifier()
        crossValidation(kf,train_set,bernoulliNaiveBayes,"bernoulliNaiveBayes",pathDestination)
        
        print ("\n\nsvmSGDClassifier")
        svmSGD = svmSGDClassifier()
        crossValidation(kf,train_set,svmSGD,"svmSGD",pathDestination)

        #print ("\n\nsvmSVCClassifier")
        #crossValidation(kf,train_set,svmSVC)

        print ("FIM DAS AVALIAÇÕES")

    opcao = input("Train classifier using all samples and classifer all data_set?(yes/No):")
    if opcao.lower() in ["yes","y"]:
        print ("Treinando e classificando toda base")

        folderData = "tweetsPorData/"
        
        print ("SVM SGDLinear")
        classifier = svmSGDClassifier()        
        cls = classifierTrain(train_set,classifier)
        folderResultsAnalysis = "resultadosAnalises/SVMSGDClassifier/"
        evaluateAllTweetMessages(train_set,cls,folderData,folderResultsAnalysis)

        '''temp
        import sys
        aux = input("Digite sua msg:").decode(sys.stdin.encoding)
        #print (aux)
        #aux = aux.decode('utf-8')
        aux = preProcessingMessages(PreProcessor(), aux.encode('utf-8'))
        print ("resultado:",classifyOneMessage(train_set,cls, aux))

        #fim temp para teste
        
        print ('\n\nParei depois que rodei a primeira vez para evitar sobrescrita. Se precisar, remover \'exit()\'')
        exit()    
        '''    
        #folderResultsAnalysis = "resultadosAnalises/SVMSGDClassifier/"
        #evaluateAllTweetMessages(train_set,cls,folderData,folderResultsAnalysis)

        '''

        #linear multinomialNaiveBayes
        print ("multinomial Naive Bayes 1,2 grams")
        classifier = multinomialNaivaBayesClassifier()#melhor valor de gram
        cls = classifierTrain(train_set,classifier)        
        folderResultsAnalysis = "resultadosAnalises/MultinomialNaiveBayesClassifier/"
        evaluateAllTweetMessages(train_set,cls,folderData,folderResultsAnalysis)
        '''

        '''
        #linear multinomialNaiveBayes 1-gram
        print ("multinomial Naive Bayes 1,1 grams")
        classifier = multinomialNaivaBayesClassifier(ngram=(1,1))
        cls = classifierTrain(train_set,classifier)        
        folderResultsAnalysis = "resultadosAnalises/multinomialNaiveBayesClassifier1gram/"
        evaluateAllTweetMessages(train_set,cls,folderData,folderResultsAnalysis)
        '''

        '''
        #linear bernoulliNaiveBayes 1-gram
        print ("Bernoulli Naive Bayes 1,1 grams")
        classifier = bernoulliNaivaBayesClassifier(ngram=(1,1))
        cls = classifierTrain(train_set,classifier)        
        folderResultsAnalysis = "resultadosAnalises/Bernoulli/"
        evaluateAllTweetMessages(train_set,cls,folderData,folderResultsAnalysis)
        '''
