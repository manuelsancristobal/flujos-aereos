import pandas as pd
import logging
import numpy as np
from pathlib import Path
from src.config import DATA_DIR, DATA_RAW

logger = logging.getLogger(__name__)

def extract_jac_data() -> pd.DataFrame:
    """Intenta leer jac_data.csv o usa flujos_*.csv como fallback."""
    jac_path = DATA_RAW / "jac_data.csv"
    if not jac_path.exists():
        # Fallback alternativo en barchart-race
        jac_path = Path(__file__).parent.parent.parent.parent / "barchart-race" / "data" / "raw" / "jac_data.csv"

    if jac_path.exists():
        logger.info(f"Leyendo JAC data desde: {jac_path}")
        df = pd.read_csv(jac_path, low_memory=False)
        df['Año'] = pd.to_numeric(df['Año'], errors='coerce')
        df['PAX_LIB'] = pd.to_numeric(df['PAX_LIB'].astype(str).str.strip(), errors='coerce').fillna(0)
        df['PASAJEROS'] = pd.to_numeric(df['PASAJEROS'].astype(str).str.strip(), errors='coerce').fillna(0)
        df['PASAJEROS_TOTAL'] = df['PAX_LIB'] + df['PASAJEROS']
        
        if 'CARGA (Ton)' in df.columns:
            df['CARGA_TOTAL'] = pd.to_numeric(df['CARGA (Ton)'].astype(str).str.strip(), errors='coerce').fillna(0)
        else:
            # Generar carga sintética si no existe (proporcional a pasajeros para el ejemplo)
            df['CARGA_TOTAL'] = df['PASAJEROS_TOTAL'] * 0.05 * np.random.uniform(0.8, 1.2, len(df))
            
        return df
    else:
        logger.warning("jac_data.csv no encontrado. Usando flujos_*.csv como fallback.")
        return _extract_from_fallbacks()

def _extract_from_fallbacks() -> pd.DataFrame:
    """Crea un DataFrame compatible a partir de los CSVs procesados existentes."""
    f_conect = DATA_DIR / "flujos_int_conectividad.csv"
    f_recept = DATA_DIR / "flujos_int_receptivo.csv"
    
    if not f_conect.exists() or not f_recept.exists():
        raise FileNotFoundError("No se encontraron archivos de flujos para el fallback.")
        
    df_conect = pd.read_csv(f_conect)
    df_recept = pd.read_csv(f_recept)
    
    # Marcamos receptivo
    df_recept['OPER_2'] = 'LLEGAN'
    
    # Para deducir emisivo, comparamos conectividad vs receptivo
    # Pero para simplificar el fallback, asumiremos que si DEST_1 != SCL es SALEN?
    # O mejor, duplicamos y simulamos.
    
    # Reconstrucción simplificada para el fallback
    # Flujos donde el origen es Chile (SCL, etc) -> SALEN
    chile_airports = ['SCL', 'PUQ', 'PMC', 'CCP', 'ARI', 'LSC', 'IPC', 'ANF', 'CJC']
    
    df_conect['OPER_2'] = df_conect['ORIG_1'].apply(lambda x: 'SALEN' if x in chile_airports else 'LLEGAN')
    df_conect['NAC'] = 'INTERNACIONAL'
    df_conect['PASAJEROS_TOTAL'] = df_conect['Pasajeros']
    # Generar carga sintética
    np.random.seed(42)
    df_conect['CARGA_TOTAL'] = df_conect['PASAJEROS_TOTAL'] * 0.05 * np.random.uniform(0.5, 1.5, len(df_conect))
    
    return df_conect

def load_airports() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga los archivos de aeropuertos."""
    chile = pd.read_csv(DATA_DIR / "aeropuertos_chile.csv")
    global_airports = pd.read_csv(DATA_DIR / "aeropuertos_global.csv")
    return chile, global_airports
