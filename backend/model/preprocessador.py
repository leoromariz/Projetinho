from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                   percentual_teste,
                                                                   seed)
        # normalização/padronização
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        X = dados[:, 1:12]
        Y = dados[:, 12]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        
        X_input = np.array([
            form.age,
            form.gender,
            form.academic_level,
            form.country,
            form.avg_daily_usage_hours,
            form.most_used_platform,
            form.affects_academic_performance,
            form.sleep_hours_per_night,
            form.mental_health_score,
            form.relationship_status,
            form.conflicts_over_social_media
        ])
        
        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)
        return X_input
    
    def scaler(self, X_train):
        """ Normaliza os dados. """
        # normalização/padronização
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_addicted.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train