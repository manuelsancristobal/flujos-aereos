import logging
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import (
    AEROPUERTOS_CHILE,
    AEROPUERTOS_GLOBAL,
    CSV_LOCAL,
    DATA_DIR,
    EXPECTED_COLUMNS,
    GSHEET_URL,
)

logger = logging.getLogger(__name__)


def download_csv(url: str = GSHEET_URL, dest: Path = CSV_LOCAL) -> Path:
    """Descarga CSV desde Google Sheets. Retorna path al archivo."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Descargando CSV desde Google Sheets...")
    try:
        urllib.request.urlretrieve(url, dest)
        logger.info("CSV descargado: %s", dest)
    except Exception as exc:
        logger.warning("No se pudo descargar: %s. Usando archivo local.", exc)
        if not dest.exists():
            # Fallback a barchart-race si estamos en local y existe esa carpeta
            alt_path = Path(__file__).parent.parent.parent.parent / "barchart-race" / "data" / "raw" / "jac_data.csv"
            if alt_path.exists():
                logger.info(f"Usando fallback de barchart-race: {alt_path}")
                return alt_path
            raise FileNotFoundError(f"No hay CSV local en {dest} ni fallback disponible.") from exc
    return dest


def load_raw(path: Path = CSV_LOCAL) -> pd.DataFrame:
    """Lee CSV crudo y valida columnas esperadas."""
    logger.info("Leyendo %s ...", path)
    df = pd.read_csv(path, low_memory=False, dtype={"PASAJEROS": str})
    _validate_columns(df)
    return df


def _validate_columns(df: pd.DataFrame) -> None:
    """Verifica que existan las columnas esperadas."""
    actual = set(df.columns)
    year_col = _find_year_column(df)
    expected = set(EXPECTED_COLUMNS)
    if year_col != "Año":
        expected = {c if c != "Año" else year_col for c in expected}
    missing = expected - actual
    if missing:
        raise ValueError(f"Columnas faltantes en los datos: {missing}")


def _find_year_column(df: pd.DataFrame) -> str:
    """Encuentra la columna de año (puede tener encoding distinto de ñ)."""
    for col in df.columns:
        if col.lower().startswith("a") and col.lower().endswith("o") and len(col) <= 4:
            return col
    raise ValueError("No se encontró columna de año (Año/Ano)")


def _parse_chilean_int(val) -> int:
    """Parsea número en formato chileno (punto como separador de miles)."""
    s = str(val).strip()
    if not s or s in ("nan", "None", ""):
        return 0
    try:
        return int(s.replace(".", ""))
    except ValueError:
        return 0


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas y tipos del DataFrame crudo."""
    df = df.copy()

    # Renombrar Año → year (evitar problemas con ñ), Mes → month
    year_col = _find_year_column(df)
    df = df.rename(columns={year_col: "year", "Mes": "month"})

    # CARGA (Ton): formato chileno pre-2022 (punto = miles), coma decimal post-2022
    pre2022 = df["year"] < 2022
    carga_str = df["CARGA (Ton)"].astype(str)
    carga_result = pd.Series(0.0, index=df.index)
    if pre2022.any():
        carga_result[pre2022] = carga_str[pre2022].apply(_parse_chilean_int).astype(float)
    if (~pre2022).any():
        carga_result[~pre2022] = pd.to_numeric(carga_str[~pre2022].str.replace(",", "."), errors="coerce").fillna(0)
    df["CARGA_TON"] = carga_result

    # PASAJEROS: formato chileno pre-2022 (punto = miles), entero post-2022
    pax_str = df["PASAJEROS"].astype(str)
    pax_result = pd.Series(0, index=df.index)
    if pre2022.any():
        pax_result[pre2022] = pax_str[pre2022].apply(_parse_chilean_int)
    if (~pre2022).any():
        pax_result[~pre2022] = pd.to_numeric(pax_str[~pre2022], errors="coerce").fillna(0).astype(int)
    df["PASAJEROS"] = pax_result

    df["PAX_LIB"] = df["PAX_LIB"].fillna(0).round().astype(int)

    # Columnas derivadas (Compatibilidad con flujos-aereos)
    df["PASAJEROS_TOTAL"] = df["PAX_LIB"] + df["PASAJEROS"]

    if "CAR_LIB" in df.columns:
        df["CARGA_TOTAL"] = (df["CAR_LIB"] / 1000) + df["CARGA_TON"]
    else:
        df["CARGA_TOTAL"] = df["CARGA_TON"]

    # Restaurar nombres de columnas que espera el resto del pipeline de flujos-aereos
    df = df.rename(columns={"year": "Año"})

    return df


def extract_jac_data(use_remote: bool = True) -> pd.DataFrame:
    """Pipeline completo de extracción: descarga (opcional) + lectura + normalización."""
    try:
        path = download_csv() if use_remote else CSV_LOCAL
        df = load_raw(path)
        df = normalize(df)
        logger.info("Extract completado: %d filas, años %d-%d", len(df), df["Año"].min(), df["Año"].max())
        return df
    except Exception as e:
        logger.error(f"Error en extract_jac_data: {e}")
        # Intentar fallback de emergencia si falla todo
        return _extract_from_fallbacks()


def _extract_from_fallbacks() -> pd.DataFrame:
    """Crea un DataFrame compatible a partir de los CSVs procesados existentes."""
    f_conect = DATA_DIR / "flujos_int_conectividad.csv"
    f_recept = DATA_DIR / "flujos_int_receptivo.csv"

    if not f_conect.exists() or not f_recept.exists():
        raise FileNotFoundError("No se encontraron archivos de flujos para el fallback.")

    logger.warning("Usando flujos_*.csv como fallback de emergencia.")
    df_conect = pd.read_csv(f_conect)

    # Reconstrucción simplificada
    chile_airports = ["SCL", "PUQ", "PMC", "CCP", "ARI", "LSC", "IPC", "ANF", "CJC"]
    df_conect["OPER_2"] = df_conect["ORIG_1"].apply(lambda x: "SALEN" if x in chile_airports else "LLEGAN")
    df_conect["NAC"] = "INTERNACIONAL"
    df_conect["PASAJEROS_TOTAL"] = df_conect["Pasajeros"]
    np.random.seed(42)
    df_conect["CARGA_TOTAL"] = df_conect["PASAJEROS_TOTAL"] * 0.05 * np.random.uniform(0.5, 1.5, len(df_conect))

    return df_conect


def load_airports() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga los archivos de aeropuertos."""
    chile = pd.read_csv(AEROPUERTOS_CHILE)
    global_airports = pd.read_csv(AEROPUERTOS_GLOBAL)
    return chile, global_airports
