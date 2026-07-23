import pandas as pd
import numpy as np
import os

# =====================================================================
# CONFIGURACIÓN
# =====================================================================
archivo_primera = 'Jugadores_Limpio.csv'  # Pon tus nombres reales
archivo_segunda = 'Jugadores_Segunda_Limpio.csv'

archivo_final = 'Jugadores_Finales.csv'

# Columnas que identifican de forma única a cada fila de datos
columna_jugador = 'Jugador'
columna_temporada = 'Temporada'

# Define aquí TODAS las temporadas que quieres que aparezcan obligatoriamente 
# para cada jugador, tengan datos o no. 
# (Asegúrate de que el formato coincida con el de tus CSVs, ej: '21/22')
lista_temporadas_obligatorias = ['21/22', '22/23', '23/24', '24/25', '25/26']
# =====================================================================

def cargar_csv(nombre_archivo):
    """Lee el CSV asegurando que los espacios vacíos sean NaN reales"""
    if os.path.exists(nombre_archivo):
        df = pd.read_csv(nombre_archivo, keep_default_na=True)
        df = df.replace(r'^\s*$', np.nan, regex=True)
        return df
    else:
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")

print("1. Cargando CSVs de Primera y Segunda...")
df_primera = cargar_csv(archivo_primera)
df_segunda = cargar_csv(archivo_segunda)

# 2. Combinar Primera y Segunda respetando los números existentes
print("2. Combinando datos existentes...")
df_p = df_primera.set_index([columna_jugador, columna_temporada])
df_s = df_segunda.set_index([columna_jugador, columna_temporada])
df_combinado = df_p.combine_first(df_s)
df_combinado = df_combinado.combine_first(df_s)
df_combinado = df_combinado.reset_index()

# =====================================================================
# CREACIÓN DE LA MATRIZ COMPLETA (Rellenar huecos de temporadas vacías)
# =====================================================================
print("3. Generando la matriz completa de Jugador x Temporada...")

# A. Extraer la lista de todos los jugadores únicos que existen en tus datos
todos_los_jugadores = df_combinado[columna_jugador].dropna().unique()

# B. Crear todas las combinaciones posibles (Cada jugador x Cada temporada de la lista)
matriz_completa = pd.MultiIndex.from_product(
    [todos_los_jugadores, lista_temporadas_obligatorias], 
    names=[columna_jugador, columna_temporada]
).to_frame(index=False)

# C. Hacer un Left Join: La matriz completa manda. 
# Si el jugador tiene datos en una temporada, los pega. Si no los tiene, crea la fila con NaN.
df_final = pd.merge(matriz_completa, df_combinado, on=[columna_jugador, columna_temporada], how='left')

# 4. Guardar el archivo definitivo listo para rellenar a mano
df_final.to_csv(archivo_final, index=False)

print("\n¡Proceso completado con éxito!")
print(f"-> Archivo guardado como: '{archivo_final}'")
print(f"-> Total de filas generadas: {len(df_final)}")