import pandas as pd

from src.etl.extract import extract_jac_data, load_airports


def test_extract_jac_data_structure():
    """Verifica que el dataframe de extracción tenga las columnas mínimas necesarias."""
    # Usamos use_remote=False para no depender de internet en el test
    # y que use el CSV descargado en el paso anterior.
    df = extract_jac_data(use_remote=False)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # Columnas críticas para el resto del pipeline
    expected_cols = ["Año", "ORIG_1", "DEST_1", "PASAJEROS_TOTAL", "CARGA_TOTAL", "OPER_2", "NAC"]
    for col in expected_cols:
        assert col in df.columns, f"Falta la columna crítica: {col}"

def test_load_airports():
    """Verifica la carga de catálogos de aeropuertos."""
    chile, global_airports = load_airports()

    assert isinstance(chile, pd.DataFrame)
    assert isinstance(global_airports, pd.DataFrame)
    assert "codigo_iata" in chile.columns
    assert "codigo_iata" in global_airports.columns
    assert not chile.empty
    assert not global_airports.empty
