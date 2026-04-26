import pandas as pd
import logging
from src.config import COL_AÑO, COL_ORIGEN, COL_DESTINO, COL_PASAJEROS, COL_CARGA, COL_SENTIDO

logger = logging.getLogger(__name__)

def build_pipeline(df: pd.DataFrame, airports_chile: pd.DataFrame, airports_global: pd.DataFrame, perspective: str, metric: str) -> pd.DataFrame:
    """Procesa el dataframe para una métrica y perspectiva específica."""
    
    # 1. Filtrar por perspectiva
    # Emisivo = SALEN (Desde Chile al exterior)
    # Receptivo = LLEGAN (Desde el exterior a Chile)
    sentido = "SALEN" if perspective == "emisivo" else "LLEGAN"
    
    # Nota: También podríamos incluir Nacional aquí si quisiéramos, 
    # pero por ahora seguimos la lógica de internacional para emisivo/receptivo
    mask = (df[COL_SENTIDO] == sentido) & (df['NAC'] == 'INTERNACIONAL')
    filtered_df = df[mask].copy()
    
    # 2. Seleccionar métrica
    col_metric = COL_PASAJEROS if metric == "pasajeros" else COL_CARGA
    
    # 3. Agrupar por origen, destino y año
    grouped = filtered_df.groupby([COL_ORIGEN, COL_DESTINO, COL_AÑO]).agg({col_metric: 'sum'}).reset_index()
    grouped = grouped[grouped[col_metric] > 0]
    
    # 4. Unir con coordenadas
    # Necesitamos lat/lng para ORIGEN y DESTINO
    # Usamos aeropuertos_global para ambos ya que incluye a los de Chile también (usualmente)
    # Si no, combinamos ambos.
    
    all_airports = pd.concat([airports_chile, airports_global]).drop_duplicates(subset=['codigo_iata'])
    
    coords_orig = all_airports[['codigo_iata', 'lat', 'lng']].copy()
    coords_orig.columns = [COL_ORIGEN, 'lat_orig', 'lng_orig']
    
    coords_dest = all_airports[['codigo_iata', 'lat', 'lng']].copy()
    coords_dest.columns = [COL_DESTINO, 'lat_dest', 'lng_dest']
    
    result = grouped.merge(coords_orig, on=COL_ORIGEN, how='left')
    result = result.merge(coords_dest, on=COL_DESTINO, how='left')
    
    # Eliminar filas sin coordenadas
    count_before = len(result)
    result = result.dropna(subset=['lat_orig', 'lng_orig', 'lat_dest', 'lng_dest'])
    count_after = len(result)
    
    if count_before > count_after:
        logger.warning(f"Se eliminaron {count_before - count_after} registros por falta de coordenadas.")
        
    return result
