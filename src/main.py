"""Orquestador ETL para ArcLayer."""

import logging
import sys
from src.config import PERSPECTIVAS, TIPOS_TRAFICO
from src.etl.extract import extract_jac_data, load_airports
from src.etl.transform import build_pipeline
from src.etl.load import load_to_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def run():
    """Ejecuta el pipeline completo para todas las combinaciones."""
    logger.info("Iniciando ETL de ArcLayer...")
    
    try:
        df_jac = extract_jac_data()
        airports_chile, airports_global = load_airports()
    except Exception as e:
        logger.error(f"Error extrayendo datos: {e}")
        return
        
    generated = []
    for perspective in PERSPECTIVAS:
        for metric in TIPOS_TRAFICO:
            combo = f"{perspective}_{metric}"
            try:
                logger.info(f"Procesando {combo}...")
                transformed = build_pipeline(df_jac, airports_chile, airports_global, perspective, metric)
                path = load_to_json(transformed, perspective, metric)
                generated.append(path)
            except Exception as e:
                logger.error(f"Error procesando {combo}: {e}")
                
    logger.info(f"ETL finalizado. {len(generated)} archivos generados.")

if __name__ == "__main__":
    run()
