
import pandas as pd
import requests
from io import StringIO
import os

def update_airports():
    print("Descargando datos de OurAirports...")
    url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = StringIO(response.text)
        df = pd.read_csv(data)
        
        # Filtrar solo aeropuertos con código IATA
        df_clean = df[df['iata_code'].notna()][['iata_code', 'latitude_deg', 'longitude_deg', 'iso_country']]
        df_clean.columns = ['codigo_iata', 'lat', 'lng', 'pais']
        
        # Separar Chile de Global (aunque Global los incluya)
        chile = df_clean[df_clean['pais'] == 'CL'].drop(columns=['pais'])
        global_airports = df_clean.drop(columns=['pais'])
        
        # Guardar en las rutas esperadas
        os.makedirs('data/external', exist_ok=True)
        chile.to_csv('data/external/aeropuertos_chile.csv', index=False)
        global_airports.to_csv('data/external/aeropuertos_global.csv', index=False)
        
        print(f"Actualización completada:")
        print(f" - Aeropuertos Chile: {len(chile)}")
        print(f" - Aeropuertos Globales: {len(global_airports)}")
        
    except Exception as e:
        print(f"Error actualizando aeropuertos: {e}")

if __name__ == '__main__':
    update_airports()
