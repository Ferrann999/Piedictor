import pandas as pd
import os

# 1. Lista de los 6 archivos CSV originales
archivos_csv = [
    "1aDiv_23-24.csv",
    "1aDiv_24-25.csv",
    "1aDiv_25-26.csv",
    "2aDiv_23-24.csv",
    "2aDiv_24-25.csv",
    "2aDiv_25-26.csv"
]

# 2. Mapeo lógico de los equipos
mapeo_equipos = {
    'Ath Bilbao': 'Ath Bilbao',
    'Ath Madrid': 'Ath Madrid',
    'Osasuna': 'Osasuna',
    'Alaves': 'Alaves',
    'Elche': 'Elche',
    'Barcelona': 'Barcelona',
    'Getafe': 'Getafe',
    'Levante': 'Levante',
    'Malaga': 'Malaga',
    'Santander': 'Racing Santander',
    'Vallecano': 'Rayo',
    'Celta': 'Celta',
    'La Coruna': 'La Coruna',
    'Espanol': 'Espanyol',
    'Betis': 'Betis',
    'Real Madrid': 'Real Madrid',
    'Sociedad': 'Real Sociedad',
    'Sevilla': 'Sevilla',
    'Valencia': 'Valencia',
    'Villarreal': 'Villarreal'
}

# 3. Diccionario para renombrar las columnas
mapeo_columnas = {
    'Date': 'Fecha',
    'Time': 'hora',
    'HomeTeam': 'L',
    'AwayTeam': 'V',
    'FTHG': 'GL',  
    'FTAG': 'GV',  
    'HST': 'TL',   
    'AST': 'TV',   
    'HC': 'CL',    
    'AC': 'CV',    
    'HY': 'AL',    
    'AY': 'AV',    
    'HR': 'RL',    
    'AR': 'RV'     
}

# 4. Orden final de las columnas
orden_columnas = [
    'Fecha', 'hora', 'L', 'V', 'GL', 'GV', 'TL', 'TV', 'CL', 'CV', 'AL', 'AV', 'RL', 'RV'
]

# Lista para guardar cada DataFrame procesado
lista_dataframes = []

# 5. Procesamiento de cada archivo
for archivo in archivos_csv:
    if os.path.exists(archivo):
        # Leer el CSV
        df = pd.read_csv(archivo)
        
        # FILTRO: Partidos donde el equipo local O el visitante están en la lista
        condicion = df['HomeTeam'].isin(mapeo_equipos.keys()) | df['AwayTeam'].isin(mapeo_equipos.keys())
        df_filtrado = df[condicion].copy()
        
        # REEMPLAZO: Cambiar los nombres de nuestra lista y dejar intactos los demás
        df_filtrado['HomeTeam'] = df_filtrado['HomeTeam'].replace(mapeo_equipos)
        df_filtrado['AwayTeam'] = df_filtrado['AwayTeam'].replace(mapeo_equipos)
        
        # Recortar solo las columnas que nos interesan y renombrarlas
        df_final = df_filtrado[list(mapeo_columnas.keys())].rename(columns=mapeo_columnas)
        
        # Reordenar las columnas al orden solicitado
        df_final = df_final[orden_columnas]
        
        # Añadir el dataframe procesado a la lista
        lista_dataframes.append(df_final)
        
        print(f"Leído y procesado: {archivo}")
    else:
        print(f"Advertencia: No se encontró el archivo '{archivo}'.")

# 6. Unir todos los dataframes y guardar en un solo CSV
if lista_dataframes:
    # Concatenar todos los dataframes en uno solo
    df_unido = pd.concat(lista_dataframes, ignore_index=True)
    
    # Guardar en un nuevo archivo CSV
    Resultados_Equipos = "partidos_equipos_.csv"
    df_unido.to_csv(Resultados_Equipos, index=False)
    
    print(f"\n¡Éxito! Se han unido los archivos. Total de partidos: {len(df_unido)}")
    print(f"Archivo guardado como: '{Resultados_Equipos}'")
else:
    print("No se encontró ningún dato para unir.")