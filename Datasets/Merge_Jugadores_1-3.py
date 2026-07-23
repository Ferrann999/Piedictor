import pandas as pd
import numpy as np
import os

# 1. Leer los 4 archivos CSV
archivo1 = 'jugadores_goles_laliga_25_26.csv'
archivo2 = 'jugadores_laliga_25_26.csv'
archivo3 = 'jugadores_misc_laliga_25_26.csv'
archivo_porteros = 'porteros_laliga_25_26.csv'

# Nombre de la columna de los jugadores (ej. 'Player' o 'Nombre')
columna_clave = 'Player' 

# Nombre del archivo unificado resultante
archivo_salida = 'tmp-25-26.csv'
# =====================================================================

def cargar_y_limpiar_csv(nombre_archivo):
    """Lee un CSV forzando que cualquier vacío se convierta en un NaN real"""
    if os.path.exists(nombre_archivo):
        # keep_default_na=True convierte automáticamente los campos vacíos (,,) en NaN
        df = pd.read_csv(nombre_archivo, keep_default_na=True)
        # Reemplaza celdas que solo tengan espacios en blanco (" ") o estén vacías ("") por NaN reales
        df = df.replace(r'^\s*$', np.nan, regex=True)
        return df
    else:
        raise FileNotFoundError(f"No se pudo encontrar el archivo: {nombre_archivo}")

# 1. Leer los 4 archivos CSV con la limpieza de vacíos a NaN integrada
df1 = cargar_y_limpiar_csv(archivo1)
df2 = cargar_y_limpiar_csv(archivo2)
df3 = cargar_y_limpiar_csv(archivo3)
df_porteros = cargar_y_limpiar_csv(archivo_porteros)

# =====================================================================
# PASO 1: Fusionar los 3 primeros CSV usando TODAS sus columnas comunes
# =====================================================================
comunes_1_2 = list(set(df1.columns) & set(df2.columns))
df_unido = pd.merge(df1, df2, on=comunes_1_2)

comunes_unido_3 = list(set(df_unido.columns) & set(df3.columns))
df_unido = pd.merge(df_unido, df3, on=comunes_unido_3)

# =====================================================================
# PASO 2: Limpiar el CSV de porteros antes de unirlo
# =====================================================================
# Eliminamos columnas repetidas para evitar conflictos de nombres
columnas_repetidas_porteros = [col for col in df_porteros.columns if col in df_unido.columns and col != columna_clave]
df_porteros_limpio = df_porteros.drop(columns=columnas_repetidas_porteros)

# =====================================================================
# PASO 3: Unión final (Left Join) conservando los NaN de forma natural
# =====================================================================
# Al hacer left join, los jugadores de campo que NO estén en el archivo de 
# porteros recibirán automáticamente un valor NaN en las columnas de portero.
# ¡Aquí ya NO aplicamos el .fillna(0) para mantener esos NaN intactos!
df_final = pd.merge(df_unido, df_porteros_limpio, on=columna_clave, how='left')

# =====================================================================
# PASO 4: Añadir metadatos y limpiar filas de cabecera repetidas
# =====================================================================
# Añadimos la temporada fija para todos
df_final['Temporada'] = '25/26'

# Filtro de seguridad: Eliminamos filas donde el nombre sea igual al de la columna
df_final = df_final[df_final[columna_clave] != columna_clave]

# 5. Guardar el archivo limpio resultante
df_final.to_csv(archivo_salida, index=False)
print(f"¡Fusión completada con éxito!")
print(f"Los jugadores de campo y datos vacíos ahora conservan sus valores NaN en '{archivo_salida}'.")