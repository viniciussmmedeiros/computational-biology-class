import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.cluster import KMeans

file_name = 'Liver_GSE76427.csv' # https://sbcb.inf.ufrgs.br/cumida

if __name__ == '__main__': 
    # usando a biblioteca pandas para abrir o arquivo .csv com os dados de expressão gênica
    data = pd.read_csv(file_name, delimiter=',', header=0, index_col=0) 
    # exibe um resumo do conjunto de dados
    print(data) 
    
    # A)
    # normalizando dataframe usando z-score
    normalized_data = data.copy();

    for column in normalized_data.columns:
        if column != 'type':
            normalized_data[column] = (normalized_data[column] - normalized_data[column].mean()) / normalized_data[column].std()

    print("\nDados normalizados:\n")
    print(normalized_data)

    # B)
    # Dividindo conjunto de dados em teste (30%) e treinamento (70%) usando amostragem estratificada
    train, test = train_test_split(normalized_data, test_size=0.3, stratify=normalized_data['type'])    

    # C)
    # Usando scikit para criar SVM, treinar usando letra B
    classifier = svm.SVC()
    classifier.fit(train.drop('type', axis=1), train['type'])

    # D)
    # Usando modelo treinado na C e conjunto de testes, avaliar:
    # Matriz de confusão; Acurácia; Sensitivity; Specificity; F1-score
    y_true = test['type']
    y_pred = classifier.predict(test.drop('type', axis=1))
    confusion_matrix_result = confusion_matrix(y_true, y_pred, labels=data['type'].unique())
    print("\nMatriz de confusão:\n")
    print(confusion_matrix_result)

    # Acurácia
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\nAcurácia: {accuracy:.2f}")

    # Sensitivity, e F1-score
    report = classification_report(y_true, y_pred, target_names=data['type'].unique())
    print("\nReport (contendo sensitivity e f1-score):")
    print(report)

    # Specificity
    true_negative, false_positive, fn, tp = confusion_matrix_result.ravel()
    specificity = true_negative / (true_negative + false_positive)

    print(f"\nSpecificity: {specificity:.2f}\n")

    """
    Matriz de confusão:
    [[33  2]
    [ 1 14]]

    Apenas 2 falsos positivos e 1 falso negativo, o que parece ser um resultado muito bom
    comparando com os verdadeiros positivos e negativos.

    Accuracy: 0.94

    Precisão de 94%.
    
    Classification Report:
                    precision   recall(ensitivity)  f1-score   support

        HCC             0.97      0.94              0.96        35
        normal          0.88      0.93              0.90        15

        accuracy                                    0.94        50
        macro avg       0.92      0.94              0.93        50
        weighted avg    0.94      0.94              0.94        50

    O treinamento e predição funcionaram muito bem, resultando em alta precisão e predição
    correta em boa parte. No entanto, é importante considerar a qualidade dos dados usados, o
    resultado da amostragem estratificada e a possibilidade de que os dados de treinamento e teste
    são muito poucos para que seja possível chegar em uma conclusão confiável.
    """

    # E)
    # k-means: Para cada cluster, reportar o número de amostras
    num_clusters = [2, 3, 4]

    for n_clusters in num_clusters:
        kmeans = KMeans(n_clusters = n_clusters, random_state=0).fit(normalized_data.drop('type', axis=1))
        clusters = kmeans.predict(normalized_data.drop('type', axis=1))

        print("\nNúmero de amostras em cada cluster:\n", pd.Series(clusters).value_counts())
    """
    Número de amostras em cada cluster (2):
    0    111
    1     54

    Número de amostras em cada cluster (3):
    0    72
    1    51
    2    42

    Número de amostras em cada cluster (4):
    0    83
    3    40
    2    24
    1    18

    O número de amostras variou consideravelmente de acordo com o número de clusters, o que pode significar que
    os dados usados não são muito homogêneos e há um bom potencial de haverem subgrupos.
    """