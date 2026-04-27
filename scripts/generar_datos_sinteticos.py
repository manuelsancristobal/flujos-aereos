#!/usr/bin/env python3
"""
Genera datos sinteticos realistas para Tourism Investment Atlas.
Basados en estructura real de JAC, aeropuertos Chile, atractivos.
"""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

np.random.seed(42)

print("=" * 60)
print("GENERANDO DATOS SINTETICOS PARA TESTING")
print("=" * 60)

# ============================================================================
# 1. AEROPUERTOS CHILE
# ============================================================================
print("\n[1] Generando aeropuertos Chile...")
aeropuertos_chile = pd.DataFrame({
    'codigo_iata': ['SCL', 'PUQ', 'PMC', 'CCP', 'CTS', 'ARI', 'LSC', 'IPC', 'PUB', 'ZLC'],
    'nombre': [
        'Santiago', 'Punta Arenas', 'Puerto Montt', 'Calama',
        'Concepcion', 'Arica', 'La Serena', 'Isla Pascua', 'Puerto Bories', 'Zonal Chico'
    ],
    'lat': [-33.393, -53.003, -41.439, -22.452, -36.774, -18.348, -30.575, -27.165, -52.299, -45.374],
    'lng': [-70.786, -70.854, -73.094, -68.899, -73.047, -70.501, -71.543, -109.422, -73.146, -72.144]
})
aeropuertos_chile.to_csv(DATA_DIR / 'aeropuertos_chile.csv', index=False)
print(f"[OK] {len(aeropuertos_chile)} aeropuertos Chile")

# ============================================================================
# 2. AEROPUERTOS GLOBAL (subset)
# ============================================================================
print("\n[2] Generando aeropuertos globales...")
aeropuertos_global = pd.DataFrame({
    'codigo_iata': ['SCL', 'GRU', 'BOG', 'LIM', 'JFK', 'MAD', 'CDG', 'FCO', 'ORY', 'MIA'],
    'nombre': [
        'Santiago', 'Sao Paulo', 'Bogota', 'Lima',
        'New York', 'Madrid', 'Paris', 'Roma', 'Paris Orly', 'Miami'
    ],
    'lat': [-33.393, -23.435, 4.702, -12.022, 40.639, 40.472, 49.009, 41.800, 48.725, 25.795],
    'lng': [-70.786, -46.473, -74.148, -77.115, -73.778, -3.568, 2.550, 12.250, 2.386, -80.287]
})
aeropuertos_global.to_csv(DATA_DIR / 'aeropuertos_global.csv', index=False)
print(f"[OK] {len(aeropuertos_global)} aeropuertos globales")

# ============================================================================
# 3. FLUJOS NACIONALES
# ============================================================================
print("\n[3] Generando flujos nacionales...")
rutas_nac = [
    ('SCL', 'PUQ', 2024, 180000),
    ('SCL', 'PMC', 2024, 120000),
    ('SCL', 'CCP', 2024, 95000),
    ('SCL', 'CTS', 2024, 85000),
    ('SCL', 'ARI', 2024, 42000),
    ('SCL', 'LSC', 2024, 65000),
    ('PUQ', 'PMC', 2024, 35000),
    ('PMC', 'CTS', 2024, 28000),
    ('ARI', 'SCL', 2024, 42000),
    ('LSC', 'SCL', 2024, 65000),
]

flujos_nac = []
for orig, dest, año, pax in rutas_nac:
    orig_idx = aeropuertos_chile[aeropuertos_chile['codigo_iata'] == orig].index[0]
    dest_idx = aeropuertos_chile[aeropuertos_chile['codigo_iata'] == dest].index[0]

    orig_row = aeropuertos_chile.iloc[orig_idx]
    dest_row = aeropuertos_chile.iloc[dest_idx]

    flujos_nac.append({
        'ORIG_1': orig,
        'DEST_1': dest,
        'Año': año,
        'Pasajeros': int(pax * (0.9 + np.random.random() * 0.2)),
        'lat_h': orig_row['lat'],
        'lng_h': orig_row['lng'],
        'lat_w': dest_row['lat'],
        'lng_w': dest_row['lng']
    })

df_nac = pd.DataFrame(flujos_nac)
df_nac.to_csv(DATA_DIR / 'flujos_nacionales.csv', index=False)
print(f"[OK] {len(df_nac)} rutas nacionales")

# ============================================================================
# 4. FLUJOS INTERNACIONALES (conectividad)
# ============================================================================
print("\n[4] Generando flujos internacionales (conectividad)...")
rutas_int = [
    ('SCL', 'GRU', 2024, 220000),
    ('SCL', 'BOG', 2024, 85000),
    ('SCL', 'LIM', 2024, 95000),
    ('SCL', 'JFK', 2024, 120000),
    ('SCL', 'MAD', 2024, 110000),
    ('SCL', 'CDG', 2024, 105000),
    ('GRU', 'SCL', 2024, 220000),
    ('BOG', 'SCL', 2024, 85000),
    ('LIM', 'SCL', 2024, 95000),
    ('JFK', 'SCL', 2024, 120000),
]

flujos_int = []
for orig, dest, año, pax in rutas_int:
    orig_idx = aeropuertos_global[aeropuertos_global['codigo_iata'] == orig].index[0]
    dest_idx = aeropuertos_global[aeropuertos_global['codigo_iata'] == dest].index[0]

    orig_row = aeropuertos_global.iloc[orig_idx]
    dest_row = aeropuertos_global.iloc[dest_idx]

    flujos_int.append({
        'ORIG_1': orig,
        'DEST_1': dest,
        'Año': año,
        'Pasajeros': int(pax * (0.9 + np.random.random() * 0.2)),
        'lat_h': orig_row['lat'],
        'lng_h': orig_row['lng'],
        'lat_w': dest_row['lat'],
        'lng_w': dest_row['lng']
    })

df_int = pd.DataFrame(flujos_int)
df_int.to_csv(DATA_DIR / 'flujos_int_conectividad.csv', index=False)
print(f"[OK] {len(df_int)} rutas internacionales (bidireccional)")

# ============================================================================
# 5. FLUJOS INTERNACIONALES (receptivo - solo LLEGAN a Chile)
# ============================================================================
print("\n[5] Generando flujos internacionales (receptivo)...")
rutas_receptivo = [
    ('GRU', 'SCL', 2024, 220000),
    ('BOG', 'SCL', 2024, 85000),
    ('LIM', 'SCL', 2024, 95000),
    ('JFK', 'SCL', 2024, 120000),
    ('MAD', 'SCL', 2024, 110000),
    ('CDG', 'SCL', 2024, 105000),
    ('FCO', 'SCL', 2024, 45000),
    ('ORY', 'SCL', 2024, 38000),
    ('MIA', 'SCL', 2024, 65000),
]

flujos_rec = []
for orig, dest, año, pax in rutas_receptivo:
    orig_idx = aeropuertos_global[aeropuertos_global['codigo_iata'] == orig].index[0]
    dest_idx = aeropuertos_global[aeropuertos_global['codigo_iata'] == dest].index[0]

    orig_row = aeropuertos_global.iloc[orig_idx]
    dest_row = aeropuertos_global.iloc[dest_idx]

    flujos_rec.append({
        'ORIG_1': orig,
        'DEST_1': dest,
        'Año': año,
        'Pasajeros': int(pax * (0.9 + np.random.random() * 0.2)),
        'lat_h': orig_row['lat'],
        'lng_h': orig_row['lng'],
        'lat_w': dest_row['lat'],
        'lng_w': dest_row['lng']
    })

df_rec = pd.DataFrame(flujos_rec)
df_rec.to_csv(DATA_DIR / 'flujos_int_receptivo.csv', index=False)
print(f"[OK] {len(df_rec)} rutas internacionales (receptivas)")

# ============================================================================
# 6. CLUSTERS TURISTICOS (actualizado con coordenadas reales)
# ============================================================================
print("\n[6] Generando clusters turisticos...")
clusters = pd.DataFrame({
    'cluster_id': [1, 2, 3, 4, 5, 6],
    'nombre': [
        'Torres del Paine',
        'San Pedro de Atacama',
        'Lagos Patagonia',
        'Chiloe',
        'Elqui - Coquimbo',
        'Litoral Central'
    ],
    'lat': [-51.0, -22.5, -40.7, -42.5, -30.2, -33.0],
    'lng': [-73.0, -68.5, -72.2, -73.8, -71.3, -71.5],
    'n_atractivos': [18, 14, 22, 16, 12, 20],
    'score_atractivo': [92.0, 88.0, 85.0, 78.0, 72.0, 82.0],
    'aeropuerto_cercano': ['PUQ', 'CCP', 'PMC', 'PMC', 'LSC', 'SCL']
})
clusters.to_csv(DATA_DIR / 'clusters_turisticos.csv', index=False)
print(f"[OK] {len(clusters)} clusters turisticos")

# ============================================================================
# 7. HISTORICO PASAJEROS (2019-2024, excluyendo COVID)
# ============================================================================
print("\n[7] Generando historico pasajeros...")
años = [2019, 2020, 2021, 2022, 2023, 2024]
pasajeros_base = [850000, 450000, 320000, 680000, 780000, 900000]

historico = pd.DataFrame({
    'Año': años,
    'Pasajeros_Total': pasajeros_base,
    'Pasajeros_Nacionales': [650000, 250000, 150000, 450000, 520000, 600000],
    'Pasajeros_Internacionales': [200000, 200000, 170000, 230000, 260000, 300000]
})
historico.to_csv(DATA_DIR / 'historico_pasajeros.csv', index=False)
print(f"[OK] {len(historico)} años de historico")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("[OK] DATOS SINTETICOS GENERADOS")
print("=" * 60)
csv_files = sorted(list(DATA_DIR.glob('*.csv')))
print(f"\n[INFO] Archivos en {DATA_DIR}:")
for f in csv_files:
    size = f.stat().st_size / 1024
    print(f"  [OK] {f.name:35} ({size:7.1f} KB)")

print("\n[TODO] Proximos pasos:")
print("  1. Adaptar clusters_turisticos.csv con datos reales")
print("  2. Reemplazar flujos_*.csv con datos JAC cuando esten disponibles")
print("  3. Crear repo tourism-investment-atlas")
