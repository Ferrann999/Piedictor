import pandas as pd

# Carga tu archivo final
df_comprobacion = pd.read_csv('tmp-21-22.csv')

# Cuenta cuántos NaN reales hay en cada columna
print(df_comprobacion.isna().sum())