import json
import logging
from pathlib import Path

import pandas as pd

from src.config import COL_CARGA, COL_PASAJEROS, PROCESSED_DATA_DIR

logger = logging.getLogger(__name__)


def load_to_json(df: pd.DataFrame, perspective: str, metric: str) -> Path:
    """Guarda el DataFrame procesado como JSON en el directorio de assets."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{perspective}_{metric}.json"
    filepath = PROCESSED_DATA_DIR / filename

    col_metric = COL_PASAJEROS if metric == "pasajeros" else COL_CARGA

    # Convertir a lista de diccionarios con formato amigable para Deck.gl
    records = []
    for _, row in df.iterrows():
        records.append(
            {
                "orig": row["ORIG_1"],
                "dest": row["DEST_1"],
                "year": int(row["Año"]),
                "value": float(row[col_metric]),
                "source": [float(row["lng_orig"]), float(row["lat_orig"])],
                "target": [float(row["lng_dest"]), float(row["lat_dest"])],
            }
        )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    logger.info(f"Archivo guardado: {filepath}")
    return filepath
