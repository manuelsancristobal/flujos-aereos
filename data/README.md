# Datos: Flujos Aéreos

## Origen
- **Tráfico Aéreo**: JAC (Junta de Aeronáutica Civil, Chile).
- **Dataset**: `jac_data.csv` (Serie histórica consolidada).
- **Referencia**: Coordenadas de aeropuertos y clusters turísticos de SERNATUR.

## Estructura
- `raw/`: 
  - `jac_data.csv`: Datos originales de la JAC.
- `processed/`: Archivos JSON generados para la visualización Deck.gl (Arc Layer).
- `external/`:
  - `aeropuertos_chile.csv`: Catálogo de aeropuertos nacionales con coordenadas.
  - `aeropuertos_global.csv`: Catálogo de aeropuertos internacionales.
  - `clusters_turisticos.csv`: Centros de gravedad de clusters para visualización.
  - `flujos_*.csv`: Tablas auxiliares de flujos pre-calculados.

## Diccionario de Datos Clave
- `PASAJEROS`: Flujo de pasajeros entre pares de aeropuertos.
- `CARGA`: Tonelaje de carga transportada.
- `ORIG_1`, `DEST_1`: Códigos IATA de aeropuertos.
