import pandas as pd
import os
import numpy as np

# =====================================================================
# CONFIGURACIÓN (Cambia estos nombres por los tuyos reales)
# =====================================================================
archivo_csv_grande = "Jugadores_Sucio.csv"
archivo_txt_jugadores = "Jugadores_26-27.txt"  # Tu archivo .txt
archivo_salida = "Jugadores_Limpio.csv"

# Nombre de la columna de jugadores en tu CSV (ej. 'Player' o 'Nombre')
columna_clave = 'Player' 

# 1. Elige los atributos originales que quieres conservar (en el orden que te guste)
atributos_que_quiero = [
    'Player', 
    'Temporada', 
    'Squad', 
    'Pos', 
    'Age',
    'MP',
    'Min',
    'Gls',
    'Ast',
    'G+A',
    'Pk',
    'CrdY',
    '2CrdY',
    'CrdR',
    'Sh',
    'SoT',
    'Fls',
    'Fld',
    'Int',
    'TklW',
    'GA',
    'SoTA',
    'W',
    'D',
    'L',
    'CS',
    'Save%',
    'SaveP%'
]

# 2. NUEVO: Pon aquí el nombre original y al lado el NUEVO nombre que quieres
# (Las columnas que no pongas aquí mantendrán su nombre original)
cambiar_nombres = {
    'Player': 'Jugador',
    'Squad': 'Equipo',
    'Age': 'Edad',
    'MP': 'Partidos',
    'Min': 'Minutos',
    'Gls': 'Goles',
    'Ast': 'Asistencias',
    'Pk': 'Penales',
    'CrdY': 'Amarillas',
    '2CrdY': '2a Amarillas',
    'CrdR': 'Rojas',
    'Sh': 'Tiros',
    'SoT': 'Tiros a puerta',
    'Fls': 'Faltas hechas',
    'Fld': 'Faltas recibidas',
    'Int': 'Intercepciones',
    'TklW': 'Entradas ganadas',
    'GA': 'Goles recibidos',
    'SoTA': 'Tiros a puerta recibidos',
    'W': 'Victorias',
    'D': 'Empates',
    'L': 'Derrotas',
    'CS': 'Partidos sin goles',
    'Save%': 'Tiros a puerta parados (%)',
    'SaveP%': 'Penaltis parados (%)'
}
# =====================================================================


# 1. Leer el archivo .txt
jugadores_txt = []
if os.path.exists(archivo_txt_jugadores):
    with open(archivo_txt_jugadores, 'r', encoding='utf-8') as f:
        jugadores_txt = [linea.strip() for linea in f if linea.strip()]
else:
    print(f"Error: No se encontró el archivo de texto '{archivo_txt_jugadores}'.")

# 2. Procesar y cruzar los datos
if jugadores_txt and os.path.exists(archivo_csv_grande):
    
    # Convertimos la lista del .txt directamente en un DataFrame
    df_txt = pd.DataFrame(jugadores_txt, columns=[columna_clave])
    
    # Cargamos el CSV gigante forzando que los vacíos sean NaN
    df_grande = pd.read_csv(archivo_csv_grande, keep_default_na=True)
    df_grande = df_grande.replace(r'^\s*$', np.nan, regex=True)
    
    # =================================================================
    # - Si el jugador no está en el CSV -> sus atributos se quedan en NaN
    # - Si un jugador del CSV no está en df_txt -> se elimina
    # =================================================================
    df_merged = pd.merge(df_txt, df_grande, on=columna_clave, how='left')
    
    # Filtramos para quedarnos solo con las columnas que quieres.
    # (Si por algún motivo una columna que pides no existe en el CSV, 
    # este bucle la crea y la llena de NaN para que no de error)
    for col in atributos_que_quiero:
        if col not in df_merged.columns:
            df_merged[col] = np.nan
            
    # Ordenamos según tu lista
    df_final = df_merged[atributos_que_quiero]
    
    # Traducir los nombres
    df_final = df_final.rename(columns=cambiar_nombres)
    
    # 3. Guardar el nuevo CSV
    df_final.to_csv(archivo_salida, index=False)
    
    print("\n¡Proceso completado con éxito!")
    print(f"El archivo final '{archivo_salida}' tiene {len(df_final)} filas.")
else:
    print("No se pudo realizar el filtrado. Verifica que ambos archivos existan.")