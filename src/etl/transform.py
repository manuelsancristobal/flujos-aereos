import logging

import pandas as pd

from src.config import (
    AMBITO_NAC_MAP,
    COL_AÑO,
    COL_CARGA,
    COL_DESTINO,
    COL_ORIGEN,
    COL_PASAJEROS,
    COL_SENTIDO,
    SENTIDO_MAP,
)

logger = logging.getLogger(__name__)


def build_pipeline(
    df: pd.DataFrame,
    airports_chile: pd.DataFrame,
    airports_global: pd.DataFrame,
    perspective: str,
    metric: str,
    ambito: str = "internacional",
) -> pd.DataFrame:
    """Procesa el dataframe para una métrica, perspectiva y ámbito específico."""

    sentido = SENTIDO_MAP[perspective]
    nac_filter = AMBITO_NAC_MAP[ambito]

    mask = (df[COL_SENTIDO] == sentido) & (df["NAC"] == nac_filter)
    filtered_df = df[mask].copy()

    col_metric = COL_PASAJEROS if metric == "pasajeros" else COL_CARGA

    grouped = filtered_df.groupby([COL_ORIGEN, COL_DESTINO, COL_AÑO]).agg({col_metric: "sum"}).reset_index()
    grouped = grouped[grouped[col_metric] > 0]

    # Para nacional, ambos extremos son domésticos → solo airports_chile
    if ambito == "nacional":
        all_airports = airports_chile.drop_duplicates(subset=["codigo_iata"])
    else:
        all_airports = pd.concat([airports_chile, airports_global]).drop_duplicates(subset=["codigo_iata"])

    coords_orig = all_airports[["codigo_iata", "lat", "lng"]].copy()
    coords_orig.columns = [COL_ORIGEN, "lat_orig", "lng_orig"]

    coords_dest = all_airports[["codigo_iata", "lat", "lng"]].copy()
    coords_dest.columns = [COL_DESTINO, "lat_dest", "lng_dest"]

    result = grouped.merge(coords_orig, on=COL_ORIGEN, how="left")
    result = result.merge(coords_dest, on=COL_DESTINO, how="left")

    count_before = len(result)
    result = result.dropna(subset=["lat_orig", "lng_orig", "lat_dest", "lng_dest"])
    count_after = len(result)

    if count_before > count_after:
        logger.warning(f"Se eliminaron {count_before - count_after} registros por falta de coordenadas.")

    return result
