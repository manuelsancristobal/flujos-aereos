"""Constantes, rutas y configuración del proyecto flujos-aereos."""

import os
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_EXTERNAL = DATA_DIR / "external"
DATA_PROCESSED = DATA_DIR / "processed"
CSV_LOCAL = DATA_RAW / "jac_data.csv"
VIZ_DIR = PROJECT_ROOT / "viz"
ASSETS_DIR = VIZ_DIR / "assets"
PROCESSED_DATA_DIR = ASSETS_DIR / "data"

# ── Google Sheets ──────────────────────────────────────
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1U3JiVuxjDcvaIoLw9XkW3JKfuh-8_3Pc/export?format=csv&gid=499690993"

# ── Columnas esperadas en la fuente ────────────────────
EXPECTED_COLUMNS = [
    "Año",
    "Mes",
    "Cod_Operador",
    "Operador",
    "Grupo",
    "ORIG_1",
    "DEST_1",
    "ORIG_1_N",
    "DEST_1_N",
    "ORIG_1_PAIS",
    "DEST_1_PAIS",
    "ORIG_2",
    "DEST_2",
    "ORIG_2_N",
    "DEST_2_N",
    "ORIG_2_PAIS",
    "DEST_2_PAIS",
    "OPER_2",
    "NAC",
    "PAX_LIB",
    "PASAJEROS",
    "CAR_LIB",
    "CARGA (Ton)",
    "CORREO",
    "Distancia",
]

# ── Jekyll ─────────────────────────────────────────────
_jekyll_env = os.getenv("JEKYLL_REPO")
JEKYLL_REPO: Path | None = Path(_jekyll_env) if _jekyll_env else None
JEKYLL_BASE = (JEKYLL_REPO / "proyectos" / "flujos-aereos") if JEKYLL_REPO else None
JEKYLL_DATA_DIR = (JEKYLL_BASE / "assets" / "data") if JEKYLL_BASE else None
JEKYLL_CSS_DIR = (JEKYLL_BASE / "assets" / "css") if JEKYLL_BASE else None
JEKYLL_JS_DIR = (JEKYLL_BASE / "assets" / "js") if JEKYLL_BASE else None
JEKYLL_PAGE = (JEKYLL_BASE / "viz.html") if JEKYLL_BASE else None
JEKYLL_PROJECTS_DIR = (JEKYLL_REPO / "_projects") if JEKYLL_REPO else None
JEKYLL_PROJECT_MD = PROJECT_ROOT / "jekyll" / "flujos-aereos.md" # Markdown del proyecto

# Archivos de datos procesados (salida del ETL)
AEROPUERTOS_CHILE = DATA_EXTERNAL / "aeropuertos_chile.csv"
AEROPUERTOS_GLOBAL = DATA_EXTERNAL / "aeropuertos_global.csv"
CLUSTERS_TURISTICOS = DATA_EXTERNAL / "clusters_turisticos.csv"
FLUJOS_INT_CONECTIVIDAD = DATA_EXTERNAL / "flujos_int_conectividad.csv"
FLUJOS_INT_RECEPTIVO = DATA_EXTERNAL / "flujos_int_receptivo.csv"
FLUJOS_NACIONALES = DATA_EXTERNAL / "flujos_nacionales.csv"
HISTORICO_PASAJEROS = DATA_EXTERNAL / "historico_pasajeros.csv"

# ── Configuraciones de la Visualización ────────────────
PERSPECTIVAS = ["emisivo", "receptivo"]
TIPOS_TRAFICO = ["pasajeros", "carga"]

# ── Mapeo de Columnas JAC ────────────────────────────
COL_AÑO = "Año"
COL_ORIGEN = "ORIG_1"
COL_DESTINO = "DEST_1"
COL_PASAJEROS = "PASAJEROS_TOTAL"
COL_CARGA = "CARGA_TOTAL"
COL_TIPO_VUELO = "NAC" # NACIONAL / INTERNACIONAL
COL_SENTIDO = "OPER_2" # LLEGAN / SALEN
