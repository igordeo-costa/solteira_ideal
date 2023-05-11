import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------------
# Dados limpos importados a partir daqui
# O arquivo foi renomeado externamente como 'primeiros_dados.csv'
first = pd.read_csv('primeiros_dados.csv')

# Temos 11 colunas e 42 linhas (número de testes). Logo, podemos transformar
# em um data frame do pandas
final_data = pd.DataFrame(first.values.reshape(75, 11))
final_data.columns = final_data.iloc[0]
final_data = final_data.drop(0)

# Visualização por modelo da solteira
final_data[['Make', 'Model', 'Color']] = final_data[
    'Make - Model - Color'
].str.split('-', expand=True)
final_data['Maximum Arrest Force (N)'] = pd.to_numeric(
    final_data['Maximum Arrest Force (N)']
)

# Ordenar os boxplots pelo valor máximo (pior cenário possível)
grouped = (
    final_data.loc[:, ['Model', 'Maximum Arrest Force (N)']]
    .groupby(['Model'])
    .max()
    .sort_values(by='Maximum Arrest Force (N)')
)

# Plotar o gráfico
sns.boxplot(
    y='Model',
    x='Maximum Arrest Force (N)',
    data=final_data,
    order=grouped.index,
    showfliers=False,
).set(title='Máxima Força de Arrasto em função do Modelo da Solteira')
sns.stripplot(
    y='Model',
    x='Maximum Arrest Force (N)',
    color='black',
    alpha=0.3,
    data=final_data,
    order=grouped.index,
)
#plt.savefig('GY.png', bbox_inches='tight')
plt.show()

# Visualização por tipo de material
final_data[['Size (inches)', 'Material', 'Construction']] = final_data[
    'Size (inches) - Material - Construction'
].str.split('-', expand=True)

# Ordenar os boxplots pela mediana
grouped = (
    final_data.loc[:, ['Material', 'Maximum Arrest Force (N)']]
    .groupby(['Material'])
    .median()
    .sort_values(by='Maximum Arrest Force (N)')
)

sns.boxplot(
    y='Material',
    x='Maximum Arrest Force (N)',
    data=final_data,
    order=grouped.index,
    showfliers=False,
).set(title='Máxima Força de Arrasto em função do Material da Solteira')
sns.stripplot(
    y='Material',
    x='Maximum Arrest Force (N)',
    color='black',
    alpha=0.3,
    data=final_data,
    order=grouped.index,
)
#plt.savefig('GX.png', bbox_inches='tight')
plt.show()

# Investigando a alongação do material após o teste
not_failed = final_data[final_data['Final Unit Length (cm)'] != 'Failed']
not_failed = not_failed[
    not_failed['Final Unit Length (cm)'] != 'MNT'
]  # Measure Not Taken

not_failed['Final Unit Length (cm)'] = pd.to_numeric(
    not_failed['Final Unit Length (cm)']
)
not_failed['Initial Unit Length (cm)'] = pd.to_numeric(
    not_failed['Initial Unit Length (cm)']
)

# Valor percentual de elongação
not_failed['elongation'] = (
    not_failed['Final Unit Length (cm)']
    - not_failed['Initial Unit Length (cm)']
) / not_failed['Initial Unit Length (cm)']

grouped = (
    not_failed.loc[:, ['Model', 'elongation']]
    .groupby(['Model'])
    .median()
    .sort_values(by='elongation')
)

sns.boxplot(
    y='Model',
    x='elongation',
    data=not_failed,
    order=grouped.index,
    showfliers=False,
).set(title='Percentual de elongação após o teste')
sns.stripplot(
    y='Model',
    x='elongation',
    color='black',
    alpha=0.3,
    data=not_failed,
    order=grouped.index,
)
#plt.savefig('GW.png', bbox_inches='tight')
plt.show()

# Investigando também pelo tipo de material
grouped = (
    not_failed.loc[:, ['Material', 'elongation']]
    .groupby(['Material'])
    .median()
    .sort_values(by='elongation')
)

sns.boxplot(
    y='Material',
    x='elongation',
    data=not_failed,
    order=grouped.index,
    showfliers=False,
).set(title='Percentual de elongação após o teste')
sns.stripplot(
    y='Material',
    x='elongation',
    color='black',
    alpha=0.3,
    data=not_failed,
    order=grouped.index,
)
#plt.savefig('GZ.png', bbox_inches='tight')
plt.show()

# Quem falhou no teste?
# Total de instâncias de cada modelo testados e medidos (MNT excluídos)
medidos = final_data[final_data['Final Unit Length (cm)'] != 'MNT']
testados = medidos['Model'].value_counts()
testados = testados.to_frame()

# Total de falhas por modelo
failed = final_data[final_data['Final Unit Length (cm)'] == 'Failed']
failed = (
    failed.loc[:, ['Model', 'Final Unit Length (cm)']]
    .groupby(['Model'])
    .count()
)

wh_failed = testados.join(failed)
wh_failed.fillna(0, inplace=True)
wh_failed.columns = ['Medidos', 'Falharam']
wh_failed['perc_falha'] = (wh_failed['Falharam'] / wh_failed['Medidos']).round(
    decimals=2
)
wh_failed

# O mesmo, mas para o tipo de material
# Total de instâncias de cada modelo testados e medidos (MNT excluídos)
medidos_mat = final_data[final_data['Final Unit Length (cm)'] != 'MNT']
testados_mat = medidos_mat['Material'].value_counts()
testados_mat = testados_mat.to_frame()

# Total de falhas por material
failed_mat = final_data[final_data['Final Unit Length (cm)'] == 'Failed']
failed_mat = (
    failed_mat.loc[:, ['Material', 'Final Unit Length (cm)']]
    .groupby(['Material'])
    .count()
)

wh_failed_mat = testados_mat.join(failed_mat)
wh_failed_mat.fillna(0, inplace=True)
wh_failed_mat.columns = ['Medidos', 'Falharam']
wh_failed_mat['perc_falha'] = (
    wh_failed_mat['Falharam'] / wh_failed_mat['Medidos']
).round(decimals=2)
wh_failed_mat

# Quero investigar a relação entre MAF e Fall Factor e/ou Carga usada
final_data['Mass (kg)'] = pd.to_numeric(final_data['Mass (kg)'])
final_data['Fall Factor'] = pd.to_numeric(final_data['Fall Factor'])

sns.boxplot(
    y='Model',
    x='Maximum Arrest Force (N)',
    hue='Mass (kg)',
    data=final_data,
    showfliers=False,
).set(title = 'Relação entre Massa (kg) e MAF')
#plt.savefig('GQ.png', bbox_inches='tight')
plt.show()

sns.boxplot(
    x='Maximum Arrest Force (N)',
    y='Model',
    hue='Fall Factor',
    data=final_data,
    showfliers=False,
).set(title = 'Relação Fator de Queda e MAF em cada solteira')
plt.show()

sns.boxplot(
    y='Material',
    x='Maximum Arrest Force (N)',
    hue='Mass (kg)',
    data=final_data,
    showfliers=False,
).set(title = 'Relação entre Material e MAF')
#plt.savefig('GQ.png', bbox_inches='tight')
plt.show()

sns.boxplot(
    x='Maximum Arrest Force (N)',
    y='Material',
    hue='Fall Factor',
    data=final_data,
    showfliers=False,
).set(title = 'Fator de Queda e MAF em função do material da solteira')
#plt.savefig('GK.png', bbox_inches='tight')
plt.show()
