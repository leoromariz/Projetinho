# Classificador de Adicção a Mídias Sociais
Este projeto tem como objetivo desenvolver um modelo de machine learning capaz de classificar estudantes como adictos ou não-adictos a mídias sociais, com base em dados demográficos e comportamentais. O modelo final, um Random Forest combinado com a normalização dos dados, pode ser utilizado para identificar indivíduos em risco, permitindo intervenções precoces e direcionadas.


# Como Executar o Projeto
Para replicar os resultados ou utilizar o modelo, siga os passos abaixo:

1. Clone o repositório:
```
 git clone https://github.com/leoromariz/Addicted.git
```
2. Navegue até a pasta backend:

```
cd Addicted/backend
```
3. Instale as dependências:

Certifique-se de ter o pip instalado. As bibliotecas necessárias estão listadas no cabeçalho do notebook.ipynb. Você pode instalá-las manualmente ou criar um arquivo requirements.txt com base nas importações do notebook.

```
pip install pandas numpy scikit-learn matplotlib
```
(É recomendado usar um ambiente virtual para gerenciar as dependências.)

4. Execute o Notebook Jupyter:
Abra o notebook.ipynb em um ambiente Jupyter (Jupyter Notebook ou JupyterLab) e execute todas as células para ver o processo completo de análise e treinamento do modelo.

```
jupyter notebook
```
#Resumo do Processo
O notebook notebook.ipynb documenta as seguintes etapas:

1. Carregamento e Exploração de Dados: Importação e visualização inicial do dataset students_social_media_addiction_processed.csv.

2. Separação de Dados: Divisão do dataset em conjuntos de treino e teste (X_train, X_test, y_train, y_test).

3. Avaliação de Modelos Base: Treinamento e comparação de diversos algoritmos de machine learning (Regressão Logística, KNN, Árvores de Decisão, Naive Bayes, SVM, e vários ensembles como Bagging, Random Forest, Extra Trees, AdaBoost, Gradient Boosting e Voting Classifier) utilizando validação cruzada.

4. Impacto do Pré-processamento: Análise do desempenho dos modelos com dados originais, padronizados (StandardScaler) e normalizados (MinMaxScaler). O Random Forest com normalização se destacou.

5. Tuning de Hiperparâmetros: Otimização de hiperparâmetros para o modelo KNN (embora o RF tenha sido o modelo final escolhido, esta etapa demonstra a metodologia).

6. Avaliação Final do Modelo: O modelo Random Forest (com hiperparâmetros otimizados: n_estimators=50, max_features='sqrt', min_samples_split=2, max_depth=10, min_samples_leaf=1) é treinado com normalização e avaliado no conjunto de testes, atingindo uma acurácia de aproximadamente 72.5%.

7. Persistência do Modelo: O modelo final, o scaler e o pipeline completo são salvos nos formatos .pkl para reutilização.

8. Predição de Novos Dados: Demonstração de como utilizar o modelo persistido para prever a classe (adicto/não-adicto) para novos dados de entrada.

# Conclusão
Este projeto oferece uma solução eficaz para a identificação de adicção a mídias sociais em estudantes, utilizando técnicas de machine learning. O modelo Random Forest normalizado demonstrou ser o mais robusto e performático para essa tarefa. A estrutura do projeto e os arquivos persistidos facilitam a replicação e a aplicação do modelo em contextos reais.