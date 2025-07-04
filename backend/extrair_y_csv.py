import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv(r'backend\MachineLearning\data\students_social_media_addiction_processed.csv')

# Extrair a coluna 'Addicted_Score'
addicted_score_column = df['Addicted_Score']

# Criar um novo DataFrame apenas com a coluna extraída
new_df = pd.DataFrame(addicted_score_column)

# Salvar o novo DataFrame em um arquivo CSV
new_df.to_csv(r'backend\MachineLearning\data\y_test_dataset_addicted.csv', index=False)

print("A coluna 'Addicted_Score' foi extraída com sucesso para o arquivo 'y_test_dataset_addicted.csv'.")

# Remover a coluna 'Addicted_Score'
df_sem_addicted_score = df.drop(columns=['Addicted_Score'])

# Salvar o novo DataFrame em um arquivo CSV
df_sem_addicted_score.to_csv(r'backend\MachineLearning\data\X_test_dataset_addicted_.csv', index=False)


print("A coluna 'Addicted_Score' foi removida com sucesso. O novo arquivo CSV é 'X_test_dataset_addicted_.csv'.")