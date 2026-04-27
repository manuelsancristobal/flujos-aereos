"""Constantes, rutas y configuración del proyecto flujos-aereos."""

from pathlib import Path

# ── Rutas ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = PROJECT_ROOT / "data" / "raw"
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

# Ruta al repo Jekyll local (basada en la estructura detectada)
JEKYLL_REPO = PROJECT_ROOT.parent / "manuelsancristobal.github.io"
JEKYLL_BASE = JEKYLL_REPO / "proyectos" / "flujos-aereos"
JEKYLL_DATA_DIR = JEKYLL_BASE / "assets" / "data"
JEKYLL_CSS_DIR = JEKYLL_BASE / "assets" / "css"
JEKYLL_JS_DIR = JEKYLL_BASE / "assets" / "js"
JEKYLL_PAGE = JEKYLL_BASE / "viz.html"
JEKYLL_PROJECTS_DIR = JEKYLL_REPO / "_projects"
JEKYLL_PROJECT_MD = PROJECT_ROOT / "jekyll" / "flujos-aereos.md" # Markdown del proyecto

# Archivos de datos procesados (salida del ETL)
AEROPUERTOS_CHILE = DATA_DIR / "aeropuertos_chile.csv"
AEROPUERTOS_GLOBAL = DATA_DIR / "aeropuertos_global.csv"

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
