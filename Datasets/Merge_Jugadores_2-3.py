import pandas as pd
import os

# 1. Lista con los nombres de tus 5 CSVs ya juntados y listos
# (Cambia estos nombres por los nombres reales de tus archivos)
archivos_temporadas = [
    "tmp_segunda-21-22.csv",
    "tmp_segunda-22-23.csv",
    "tmp_segunda-23-24.csv",
    "tmp_segunda-24-25.csv",
    "tmp_segunda-25-26.csv"
]

columna_clave = 'Player'

lista_dataframes = []

# 2. Leer cada archivo de temporada
for archivo in archivos_temporadas:
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        
        # Filtro de seguridad: Eliminamos cualquier fila donde el nombre sea igual al título de la columna
        df = df[df[columna_clave] != columna_clave]
        
        # Eliminamos también filas que puedan estar completamente vacías
        df = df.dropna(subset=[columna_clave])
        
        lista_dataframes.append(df)
        print(f"Leído y verificado: {archivo} ({len(df)} filas)")
    else:
        print(f"Advertencia: No se encontró el archivo '{archivo}'")

# 3. Concatenar y guardar el archivo final
if lista_dataframes:
    # Apilamos verticalmente todos los archivos
    df_historico_total = pd.concat(lista_dataframes, ignore_index=True)
    
    # Doble check de seguridad en el archivo unificado
    df_historico_total = df_historico_total[df_historico_total[columna_clave] != columna_clave]
    
    # Guardar en el nuevo CSV maestro
    nombre_salida = "Jugadores_Segunda_Sucio.csv"
    df_historico_total.to_csv(nombre_salida, index=False)
    
    print("\n¡Proceso completado!")
    print(f"El archivo final '{nombre_salida}' está 100% limpio y tiene {len(df_historico_total)} filas en total.")
else:
    print("No se encontró ningún archivo para unir.")