import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure


matplotlib.rcParams['figure.figsize'] = (12,8)

pd.options.mode.chained_assignment = None



# чтение данных
df = pd.read_csv('sberbank.csv')

# shape and data types of the data
print(df.shape)
print(df.dtypes)

# отбор числовых колонок
df_numeric = df.select_dtypes(include=[np.number])
numeric_cols = df_numeric.columns.values
print(numeric_cols)

# отбор нечисловых колонок
df_non_numeric = df.select_dtypes(exclude=[np.number])
non_numeric_cols = df_non_numeric.columns.values
print(non_numeric_cols)

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))
#@title Проверьте себя:
# Создание индикаторов пропущенных значений
for col in df.columns:
    missing = df[col].isnull()
    num_missing = np.sum(missing)

    if num_missing > 0:
        print('created missing indicator for: {}'.format(col))
        df['{}_ismissing'.format(col)] = missing

# Построение гистограммы количества пропущенных значений
ismissing_cols = [col for col in df.columns if 'ismissing' in col]
df['num_missing'] = df[ismissing_cols].sum(axis=1)

# Создание DataFrame для гистограммы
num_missing_counts = df['num_missing'].value_counts().reset_index()
num_missing_counts.columns = ['num_missing_values', 'count']
num_missing_counts = num_missing_counts.sort_values(by='num_missing_values')

# Вывод таблицы с пропущенными значениями
missing_table = df.isnull().sum().reset_index()
missing_table.columns = ['column', 'num_missing']
missing_table = missing_table[missing_table['num_missing'] > 0]
print("Таблица с количеством пропущенных значений в каждом столбце:")
print(missing_table)

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.bar(num_missing_counts['num_missing_values'], num_missing_counts['count'], color='skyblue')
plt.xlabel('Number of Missing Values per Row')
plt.ylabel('Number of Rows')
plt.title('Histogram of Missing Values per Row')
plt.xticks(num_missing_counts['num_missing_values'])  # Установить метки по оси X для всех значений
ind_missing = df[df['num_missing'] > 35].index
df_less_missing_rows = df.drop(ind_missing, axis=0)
df = df.drop(ind_missing, axis=0)
plt.show()
print(f"Before: {df.shape}, After: {df_less_missing_rows.shape}")