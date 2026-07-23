import pandas as pd
import os

# =====================================================================
# CONFIGURACIÓN
# =====================================================================
archivo_csv = 'Jugadores_Finales.csv'
columna_jugador = 'Jugador'
columna_temporada = 'Temporada'
# =====================================================================

def contar_lineas_vacias(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"Error: No se encuentra el archivo '{nombre_archivo}'.")
        return
    
    # Leer el archivo asegurando que los espacios vacíos sean NaN reales
    df = pd.read_csv(nombre_archivo, keep_default_na=True)
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    
    # Seleccionar columnas excluyendo las de identificación (nombre y temporada)
    columnas_estadisticas = [col for col in df.columns if col not in [columna_jugador, columna_temporada]]
    
    # Contar filas donde TODAS las columnas de estadísticas son NaN
    filas_todo_nan = df[columnas_estadisticas].isna().all(axis=1).sum()
    total_filas = len(df)
    
    print("=" * 45)
    print(f"Archivo analizado: {nombre_archivo}")
    print(f"Total de registros en la matriz: {total_filas}")
    print(f"Líneas con todo NaN: {filas_todo_nan}")
    print("=" * 45)

if __name__ == "__main__":
    contar_lineas_vacias(archivo_csv)