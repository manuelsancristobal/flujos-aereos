#!/usr/bin/env python3
"""
Script de preparacion de datos para Tourism Investment Atlas.
Lee JAC raw local + descarga aeropuertos y genera CSVs multi-año.
"""

import shutil
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

JAC_RAW = Path(__file__).parent.parent / 'Barchart race' / 'data' / 'raw' / 'jac_data.csv'
ATLAS_DATA = Path(__file__).parent.parent / 'tourism-investment-atlas' / 'data'

AÑOS_MIN = 2022
AÑOS_MAX = 2026

print("=" * 60)
print("DESCARGANDO Y PROCESANDO DATOS")
print("=" * 60)

# ============================================================================
# 1. AEROPUERTOS CHILE (data.humdata.org)
# ============================================================================
print("\n[1] Descargando aeropuertos Chile...")
try:
    url_aero_chile = "https://data.humdata.org/dataset/9f43c1a7-1f68-42f8-9b82-0051f9cfe0f5/resource/12e0b5fe-3cca-4c19-8bc1-b2c08a23a0c0/download/ourairports_chl.csv"
    aero_chile = pd.read_csv(url_aero_chile)
    aero_chile = aero_chile[['iata_code', 'latitude_deg', 'longitude_deg']].dropna()
    aero_chile.columns = ['codigo_iata', 'lat', 'lng']
    aero_chile.to_csv(DATA_DIR / 'aeropuertos_chile.csv', index=False)
    print(f"[OK] Guardado: {len(aero_chile)} aeropuertos Chile")
except Exception as e:
    print(f"[ERR] Error descargando aeropuertos Chile: {e}")
    print("[FALLBACK] Usando aeropuertos_chile.csv existente")
    aero_chile = pd.read_csv(DATA_DIR / 'aeropuertos_chile.csv')

# ============================================================================
# 2. AEROPUERTOS GLOBAL (OpenDataSoft)
# ============================================================================
print("\n[2] Descargando aeropuertos globales...")
try:
    url_aero_global = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/airports-code-icao/exports/csv?limit=-1"
    aero_global = pd.read_csv(url_aero_global)
    cols = aero_global.columns
    iata_col = [c for c in cols if 'iata' in c.lower()]
    lat_col = [c for c in cols if 'lat' in c.lower()][0] if any('lat' in c.lower() for c in cols) else None
    lng_col = [c for c in cols if 'long' in c.lower() or 'lon' in c.lower()]

    if iata_col and lat_col and lng_col:
        aero_global_clean = aero_global[[iata_col[0], lat_col, lng_col[0]]].dropna()
        aero_global_clean.columns = ['codigo_iata', 'lat', 'lng']
        aero_global_clean.to_csv(DATA_DIR / 'aeropuertos_global.csv', index=False)
        print(f"[OK] Guardado: {len(aero_global_clean)} aeropuertos globales")
    else:
        raise ValueError("Columnas no encontradas")
except Exception as e:
    print(f"[ERR] Error descargando aeropuertos globales: {e}")
    print("[FALLBACK] Usando aeropuertos_global.csv existente")
    aero_global_clean = pd.read_csv(DATA_DIR / 'aeropuertos_global.csv')

# ============================================================================
# 3. DATOS JAC (lectura local de jac_data.csv)
# ============================================================================
print(f"\n[3] Leyendo JAC raw de {JAC_RAW}...")
if not JAC_RAW.exists():
    print(f"[ERR] No encontrado: {JAC_RAW}")
    print("    Coloca jac_data.csv en 'Barchart race/data/raw/'")
    raise SystemExit(1)

jac_raw = pd.read_csv(JAC_RAW, low_memory=False)
print(f"[OK] Leído: {len(jac_raw)} registros JAC")

# Limpiar whitespace en PAX_LIB y PASAJEROS
jac_raw['PAX_LIB'] = pd.to_numeric(jac_raw['PAX_LIB'].astype(str).str.strip(), errors='coerce').fillna(0)
jac_raw['PASAJEROS'] = pd.to_numeric(jac_raw['PASAJEROS'].astype(str).str.strip(), errors='coerce').fillna(0)
jac_raw['NAC'] = jac_raw['NAC'].astype(str).str.strip()
jac_raw['OPER_2'] = jac_raw['OPER_2'].astype(str).str.strip() if 'OPER_2' in jac_raw.columns else 'DESCONOCIDO'

jac_raw['PASAJEROS_TOTAL'] = jac_raw['PAX_LIB'] + jac_raw['PASAJEROS']

# Filtrar rango de años
jac_raw = jac_raw[(jac_raw['Año'] >= AÑOS_MIN) & (jac_raw['Año'] <= AÑOS_MAX)]
print(f"[OK] Filtrado {AÑOS_MIN}-{AÑOS_MAX}: {len(jac_raw)} registros")
print(f"    Años: {sorted(jac_raw['Año'].unique())}")

# --- FLUJOS NACIONALES ---
print("\n[3a] Procesando flujos nacionales...")
nac_df = jac_raw[jac_raw['NAC'] == 'NACIONAL'].copy()
nac_df = nac_df.groupby(['ORIG_1', 'DEST_1', 'Año']).agg({'PASAJEROS_TOTAL': 'sum'}).reset_index()
nac_df = nac_df[nac_df['PASAJEROS_TOTAL'] > 0]
nac_df.columns = ['ORIG_1', 'DEST_1', 'Año', 'Pasajeros']

# Merge coordenadas Chile
aero_orig = aero_chile[['codigo_iata', 'lat', 'lng']].copy()
aero_orig.columns = ['ORIG_1', 'lat_h', 'lng_h']
nac_df = nac_df.merge(aero_orig, on='ORIG_1', how='left')

aero_dest = aero_chile[['codigo_iata', 'lat', 'lng']].copy()
aero_dest.columns = ['DEST_1', 'lat_w', 'lng_w']
nac_df = nac_df.merge(aero_dest, on='DEST_1', how='left')

nac_df = nac_df.dropna(subset=['lat_h', 'lng_h', 'lat_w', 'lng_w'])
nac_df.to_csv(DATA_DIR / 'flujos_nacionales.csv', index=False)
print(f"[OK] flujos_nacionales.csv: {len(nac_df)} rutas ({nac_df['Año'].nunique()} años)")

# --- FLUJOS INTERNACIONALES CONECTIVIDAD ---
print("\n[3b] Procesando flujos internacionales (conectividad)...")
int_df = jac_raw[jac_raw['NAC'] == 'INTERNACIONAL'].copy()
int_df = int_df.groupby(['ORIG_1', 'DEST_1', 'Año']).agg({'PASAJEROS_TOTAL': 'sum'}).reset_index()
int_df = int_df[int_df['PASAJEROS_TOTAL'] > 0]
int_df.columns = ['ORIG_1', 'DEST_1', 'Año', 'Pasajeros']

aero_g_orig = aero_global_clean[['codigo_iata', 'lat', 'lng']].copy()
aero_g_orig.columns = ['ORIG_1', 'lat_h', 'lng_h']
int_df_merged = int_df.merge(aero_g_orig, on='ORIG_1', how='left')

aero_g_dest = aero_global_clean[['codigo_iata', 'lat', 'lng']].copy()
aero_g_dest.columns = ['DEST_1', 'lat_w', 'lng_w']
int_df_merged = int_df_merged.merge(aero_g_dest, on='DEST_1', how='left')

int_df_merged = int_df_merged.dropna(subset=['lat_h', 'lng_h', 'lat_w', 'lng_w'])
int_df_merged.to_csv(DATA_DIR / 'flujos_int_conectividad.csv', index=False)
print(f"[OK] flujos_int_conectividad.csv: {len(int_df_merged)} rutas ({int_df_merged['Año'].nunique()} años)")

# --- FLUJOS INTERNACIONALES RECEPTIVO ---
print("\n[3c] Procesando flujos internacionales (receptivo)...")
int_receptivo = jac_raw[(jac_raw['NAC'] == 'INTERNACIONAL') & (jac_raw['OPER_2'] == 'LLEGAN')].copy()
int_receptivo = int_receptivo.groupby(['ORIG_1', 'DEST_1', 'Año']).agg({'PASAJEROS_TOTAL': 'sum'}).reset_index()
int_receptivo = int_receptivo[int_receptivo['PASAJEROS_TOTAL'] > 0]
int_receptivo.columns = ['ORIG_1', 'DEST_1', 'Año', 'Pasajeros']
int_receptivo = int_receptivo.merge(aero_g_orig, on='ORIG_1', how='left')
int_receptivo = int_receptivo.merge(aero_g_dest, on='DEST_1', how='left')
int_receptivo = int_receptivo.dropna(subset=['lat_h', 'lng_h', 'lat_w', 'lng_w'])
int_receptivo.to_csv(DATA_DIR / 'flujos_int_receptivo.csv', index=False)
print(f"[OK] flujos_int_receptivo.csv: {len(int_receptivo)} rutas")

# ============================================================================
# 4. CLUSTERS TURISTICOS
# ============================================================================
print("\n[4] Clusters turisticos (template)...")
clusters_template = pd.DataFrame({
    'cluster_id': [1, 2, 3, 4, 5],
    'nombre': ['Torres del Paine', 'Atacama', 'Lagos del Sur', 'Chiloe', 'Elqui'],
    'lat': [-51.0, -22.5, -40.7, -42.0, -30.2],
    'lng': [-73.0, -68.5, -72.2, -73.8, -71.3],
    'n_atractivos': [15, 12, 18, 10, 8],
    'score_atractivo': [92.0, 88.0, 85.0, 78.0, 72.0],
    'aeropuerto_cercano': ['PUQ', 'CCP', 'PMC', 'PMC', 'LSC']
})
clusters_template.to_csv(DATA_DIR / 'clusters_turisticos.csv', index=False)
print(f"[OK] clusters_turisticos.csv: {len(clusters_template)} clusters")

# ============================================================================
# 5. HISTORICO PASAJEROS (con Nacional + Internacional + Total)
# ============================================================================
print("\n[5] Creando historico de pasajeros...")
hist_nac = nac_df.groupby('Año')['Pasajeros'].sum().reset_index()
hist_nac.columns = ['Año', 'Pasajeros_Nacionales']

hist_int = int_df_merged.groupby('Año')['Pasajeros'].sum().reset_index()
hist_int.columns = ['Año', 'Pasajeros_Internacionales']

historico = hist_nac.merge(hist_int, on='Año', how='outer').fillna(0)
historico['Pasajeros_Total'] = historico['Pasajeros_Nacionales'] + historico['Pasajeros_Internacionales']
historico = historico.sort_values('Año').astype({'Pasajeros_Nacionales': int, 'Pasajeros_Internacionales': int, 'Pasajeros_Total': int})
historico.to_csv(DATA_DIR / 'historico_pasajeros.csv', index=False)
print(f"[OK] historico_pasajeros.csv: {len(historico)} años")
print(historico.to_string(index=False))

# ============================================================================
# 6. COPIAR CSVs → tourism-investment-atlas/data/
# ============================================================================
print(f"\n[6] Copiando CSVs a {ATLAS_DATA}...")
if ATLAS_DATA.exists():
    for csv_file in DATA_DIR.glob('*.csv'):
        shutil.copy2(csv_file, ATLAS_DATA / csv_file.name)
        print(f"  [OK] {csv_file.name} -> atlas/data/")
else:
    print(f"[WARN] {ATLAS_DATA} no existe, saltando copia")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("[OK] PREPARACION DE DATOS COMPLETADA")
print("=" * 60)
csv_files = list(DATA_DIR.glob('*.csv'))
print(f"\n[INFO] Archivos generados en {DATA_DIR}:")
for f in csv_files:
    size = f.stat().st_size / 1024
    print(f"  [OK] {f.name} ({size:.1f} KB)")
