from io import StringIO
import pandas as pd

# 1. En lugar de internet, abrimos el archivo que guardaste en tu computadora
print("Leyendo el archivo local laliga.html...")

try:
    with open("urls_jugadores_misc/25_26.html", "r", encoding="utf-8") as f:
        html_local = f.read()

    # 2. Envolvemos el texto en StringIO para evitar el FutureWarning de Pandas
    html_string = StringIO(html_local)

    # 3. Pandas lee las tablas del archivo guardado
    tablas = pd.read_html(html_string)

    # La tabla de estadísticas de los jugadores suele ser la número 2 o 3
    df_jugadores = tablas[11]

    # Mostramos las primeras filas en la consola para verificar
    print("\n--- ¡ÉXITO! Datos encontrados ---")
    print(df_jugadores.head())

    # 4. Lo guardamos como un CSV limpio para nuestro modelo de IA
    df_jugadores.to_csv("jugadores_misc_laliga_25_26.csv", index=False)
    print("\n¡Archivo guardado con éxito como 'jugadores_misc_laliga_25_26  .csv'!")

except FileNotFoundError:
    print(
        "\n[ERROR] No se encontró el archivo 'laliga.html'."
        "\nAsegúrate de guardar la página web en la misma carpeta que este script."
    )
except Exception as e:
    print(f"\n[ERROR] Ocurrió un problema al procesar el archivo: {e}")