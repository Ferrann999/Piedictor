import pandas as pd
import numpy as np
import os

# =====================================================================
# CONFIGURACIÓN
# =====================================================================
archivo1 = 'jugadores_segunda_goles_laliga_25_26.csv'
archivo2 = 'jugadores_segunda_laliga_25_26.csv'
archivo3 = 'jugadores_segunda_misc_laliga_25_26.csv'
archivo_porteros = 'porteros_segunda_laliga_25_26.csv'

columna_clave = 'Player' 
archivo_salida = 'tmp_segunda-25-26.csv'

# =====================================================================
# FUNCIÓN INTELIGENTE DE LECTURA
# =====================================================================
def cargar_y_limpiar_csv(nombre_archivo, clave='Player'):
    """Lee un CSV y arregla automáticamente el problema de doble cabecera de FBref"""
    if os.path.exists(nombre_archivo):
        # 1. Leemos el archivo de forma normal
        df = pd.read_csv(nombre_archivo, keep_default_na=True)
        
        # 2. DETECTOR FBREF: Si la columna clave no existe, pero está en la fila 0...
        # Significa que Pandas se ha tragado la cabecera real como si fuera un dato.
        if clave not in df.columns and clave in df.values[0]:
            # Volvemos a leer el archivo pero saltándonos la primera fila basura (header=1)
            df = pd.read_csv(nombre_archivo, header=1, keep_default_na=True)
            
        # 3. Limpiamos espacios ocultos en los nombres de las columnas
        df.columns = df.columns.astype(str).str.strip()
        
        # 4. Forzamos que las celdas vacías sean NaN
        df = df.replace(r'^\s*$', np.nan, regex=True)
        return df
    else:
        raise FileNotFoundError(f"No se pudo encontrar el archivo: {nombre_archivo}")


# 1. Leer los 4 archivos CSV (el detector arreglará los títulos automáticamente)
df1 = cargar_y_limpiar_csv(archivo1, columna_clave)
df2 = cargar_y_limpiar_csv(archivo2, columna_clave)
df3 = cargar_y_limpiar_csv(archivo3, columna_clave)
df_porteros = cargar_y_limpiar_csv(archivo_porteros, columna_clave)

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
# Eliminamos columnas repetidas para evitar conflictos, protegiendo 'Player'
columnas_repetidas_porteros = [
    col for col in df_porteros.columns 
    if col in df_unido.columns and col != columna_clave
]
df_porteros_limpio = df_porteros.drop(columns=columnas_repetidas_porteros)

# =====================================================================
# PASO 3: Unión final (Left Join)
# =====================================================================
df_final = pd.merge(df_unido, df_porteros_limpio, on=columna_clave, how='left')

# =====================================================================
# PASO 4: Añadir metadatos y limpiar filas basura
# =====================================================================
df_final['Temporada'] = '25/26'

# Filtro extra: A veces FBref repite la cabecera en medio de la tabla cada 25 jugadores
df_final = df_final[df_final[columna_clave] != columna_clave]

# 5. Guardar el archivo limpio resultante
df_final.to_csv(archivo_salida, index=False)
print("¡Fusión completada con éxito!")
print(f"Los datos limpios se han guardado en '{archivo_salida}'.")