import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

%matplotlib inline

dataset = pd.read_csv('DT1.csv', usecols=[7,10], na_values='-')
dataset.rename(columns={'Comenzado el':'Fecha','Calificación/50':'Puntaje'}, inplace=True)
dataset = dataset.astype({'Fecha':'category'})
dataset['Fecha'] = dataset['Fecha'].apply(lambda x: '24/07' if '24 de julio' in x else '31/07')
dataset['N'] = range(len(dataset))

sns.boxplot(data=dataset, x='Fecha', y='Puntaje')
dataset.groupby('Fecha')['Puntaje'].describe()

import scipy.stats
scipy.stats.ttest_ind(*[df['Puntaje'].values for name, df in dataset.groupby('Fecha')], nan_policy='omit')

dataset['Calificación'] = dataset['Puntaje'].apply(lambda x: 'Aprobado' if x >= 30 else 'Reprobado')
dataset.head()

sns.countplot(data=dataset, x='Fecha', hue='Calificación')

tbl = dataset.groupby(['Fecha','Calificación'])['N'].count().to_frame()
tbl_pivot = pd.pivot_table(tbl, index='Calificación', columns='Fecha', values='N')
tbl_pivot
scipy.stats.chi2_contingency(tbl_pivot)