# Tourism Investment Atlas — Plan Detallado de Implementación

---

## 1. Contexto y Motivación

### ¿Qué problema resuelve?
Un inversionista del sector turismo en Chile enfrenta una pregunta difícil: **¿En qué zona del país conviene invertir?** Para responderla necesita cruzar múltiples fuentes de datos: conectividad aérea, atractivos turísticos, tendencias de crecimiento y viabilidad financiera. Hoy esa información está dispersa en reportes estáticos, PDFs de la JAC, y análisis aislados.

### ¿Qué es el Tourism Investment Atlas?
Una **aplicación web interactiva** que muestra un mapa de Chile con múltiples capas de datos superpuestas, permitiendo al usuario:
- Ver flujos aéreos nacionales e internacionales sobre el mapa
- Identificar zonas turísticas (clusters) coloreadas por un "Score de Oportunidad"
- Ajustar los pesos del score según su criterio de inversión
- Hacer click en cualquier zona para ver un análisis detallado
- Consultar un ranking de las mejores zonas para invertir

### ¿Cómo integra los proyectos existentes del portafolio?

| Proyecto existente | Qué datos aporta | Dónde aparece en el Atlas |
|---|---|---|
| **ArcLayer (ipynb)** | Flujos aéreos nacionales: pasajeros por ruta, códigos IATA, coordenadas de aeropuertos chilenos | Capa de arcos rojos/verdes en el mapa + componente "Conectividad" del score |
| **GreatCircleLayer (ipynb)** | Flujos aéreos internacionales receptivos: pasajeros por ruta, coordenadas globales | Capa de arcos verdes/azules en el mapa + componente "Conectividad" del score |
| **Clustering turístico** | Agrupaciones de atractivos turísticos por zona geográfica | Capa de círculos/puntos en el mapa + componente "Atractivo" del score |
| **Proyección turismo emisivo** | Modelo de forecasting de demanda turística | Componente "Tendencia Histórica" del score + gráfico de tendencia histórica |
| **Inversión apalancada** | Metodología de análisis financiero comparativo | Componente "Oportunidad de mercado" del score |
| **BarchartRace** | Evolución histórica del tráfico aéreo | Contexto temporal y validación de tendencias |

---

## 2. Arquitectura Técnica

### 2.1 Visión General

```
┌─────────────────────────────────┐     ┌──────────────────────────────┐
│  Jekyll Site (GitHub Pages)     │     │  Streamlit App (Cloud)       │
│  manuelsancristobal.github.io   │     │  tourism-investment-atlas    │
│                                 │     │  .streamlit.app              │
│  _projects/                     │     │                              │
│    investment-atlas.md ─────────┼──→  │  app.py                      │
│      (iframe o link)            │     │  modules/                    │
│                                 │     │  data/                       │
│  _layouts/project.html          │     │                              │
│    (agregar soporte app_url)    │     │  Deploy: Streamlit Cloud     │
└─────────────────────────────────┘     └──────────────────────────────┘
```

**¿Por qué Streamlit y no solo Jekyll?**
Jekyll genera páginas estáticas (HTML fijo). El Atlas necesita interactividad real: filtros que recalculan el mapa, sliders que cambian el score, clicks que muestran detalle. Eso requiere un servidor Python. Streamlit Cloud es gratuito y se conecta directo a un repo de GitHub.

**¿Cómo se conectan?**
La página Jekyll del proyecto embebe la app Streamlit via `<iframe>`, exactamente como ya haces con el BarchartRace (`viz.html`). La diferencia es que en vez de un archivo local, el iframe apunta a una URL de Streamlit Cloud.

### 2.2 Estructura del Repositorio Nuevo

```
tourism-investment-atlas/          ← Nuevo repositorio en GitHub
│
├── app.py                         ← Punto de entrada de la app Streamlit
├── requirements.txt               ← Dependencias Python
├── .streamlit/
│   └── config.toml                ← Configuración visual de Streamlit
│
├── data/                              ← Datos pre-procesados (CSVs)
│   ├── flujos_nacionales.csv          ← Exportado desde ArcLayer ipynb
│   ├── flujos_int_conectividad.csv    ← Internacional bidireccional (LLEGAN+SALEN)
│   ├── flujos_int_receptivo.csv       ← Internacional solo LLEGAN (para proxy gasto)
│   ├── clusters_turisticos.csv        ← Exportado desde proyecto de clustering
│   ├── aeropuertos_chile.csv          ← Coordenadas aeropuertos nacionales
│   ├── aeropuertos_global.csv         ← Coordenadas aeropuertos internacionales
│   └── historico_pasajeros.csv        ← Serie histórica por aeropuerto y año
│
├── modules/                       ← Módulos Python
│   ├── __init__.py
│   ├── data_loader.py             ← Carga y validación de CSVs
│   ├── scoring.py                 ← Cálculo del Score de Oportunidad
│   ├── maps.py                    ← Funciones pydeck (3 capas)
│   └── charts.py                  ← Gráficos Plotly (barras, gauges, líneas)
│
├── notebooks/                     ← Notebooks de preparación (no se deployean)
│   └── 01_preparacion_datos.ipynb ← ETL desde fuentes originales a CSVs
│
└── README.md                      ← Documentación del proyecto
```

### 2.3 Layout de la Aplicación (mockup detallado)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🗺️  TOURISM INVESTMENT ATLAS — Chile                    [ℹ️ Info] │
├───────────────┬─────────────────────────────────────────────────────┤
│               │                                                     │
│   SIDEBAR     │              MAPA PRINCIPAL                         │
│   ═══════     │              (pydeck con 3 capas)                   │
│               │                                                     │
│   📅 Año      │    ╲                                                │
│   [2024]      │     ╲    Arcos rojos/verdes = vuelos nacionales     │
│               │      ╲                                              │
│   Capas:      │   ╲                                                 │
│   ☑ Nacional  │    ╲     Arcos verdes/azules = vuelos internac.     │
│   ☑ Internac. │     ╲                                               │
│   ☑ Clusters  │                                                     │
│               │   ● ● ●  Círculos = clusters turísticos             │
│   ───────     │          Color = score (🔴alto → 🔵bajo)            │
│               │          Tamaño = # atractivos                      │
│   Pesos del   │                                                     │
│   Score:      │   Al hacer CLICK en un círculo (cluster):           │
│               │   → Se actualiza el Panel Inferior                  │
│   Conectiv.   │                                                     │
│   [▬▬▬▬░] 25% │                                                     │
│               │                                                     │
│   Atractivo   │                                                     │
│   [▬▬▬▬▬] 30% │                                                     │
│               │                                                     │
│   Tendencia   │                                                     │
│   [▬▬▬▬░] 25% │                                                     │
│               │                                                     │
│   Oportunidad │                                                     │
│   [▬▬▬░░] 20% │                                                     │
│               │                                                     │
├───────────────┼──────────────────────┬──────────────────────────────┤
│               │                      │                              │
│   ZONA        │   TOP 10 ZONAS       │   DETALLE DE ZONA           │
│   SELECCIONADA│   (bar chart horiz.) │   SELECCIONADA              │
│   ═══════════ │                      │   ══════════════             │
│               │   1. Atacama  ██ 85  │                              │
│   📍 Torres   │   2. Lagos    ██ 79  │   Componentes del Score:    │
│   del Paine   │   3. Elqui   ██ 76  │   Conectiv.  ████████░░ 78  │
│               │   4. T.Paine ██ 74  │   Atractivo  █████████░ 92  │
│   Score: 74   │   5. Chiloé  ██ 71  │   Tendencia  ██████░░░░ 61  │
│               │   6. ...            │   Oportunid. ████████░░ 77  │
│   Pasajeros   │                      │   ─────────────────── ──    │
│   /año: 245K  │                      │   SCORE FINAL:        74    │
│               │                      │                              │
│   CAGR 5 años │                      │   📈 CAGR 5 años: +8.4%     │
│   +8.4%       │                      │   ✈️ Rutas directas: 12     │
│               │                      │   🏨 Competencia: Media     │
│   Rutas: 12   │                      │                              │
│               │                      │   [💰 Ver análisis financ.] │
│               │                      │                              │
└───────────────┴──────────────────────┴──────────────────────────────┘
```

---

## 3. Fuentes de Datos

Todas las fuentes necesarias para el Atlas están identificadas y disponibles:

| # | Dato | Fuente | URL / Ubicación | Notas |
|---|------|--------|-----------------|-------|
| 1 | **Flujos aéreos JAC** (nacionales + internacionales + histórico multi-año) | Junta Aeronáutica Civil | [Google Sheet](https://docs.google.com/spreadsheets/d/1U3JiVuxjDcvaIoLw9XkW3JKfuh-8_3Pc/edit?usp=sharing&ouid=104678884088479152015&rtpof=true&sd=true) | Contiene datos desde 1984. Se filtra por `NAC` (NACIONAL/INTERNACIONAL) y `Año`. Columnas clave: `ORIG_1`, `DEST_1`, `PAX_LIB`, `PASAJEROS`, `OPER_2`. |
| 2 | **Aeropuertos Chile** (código IATA, lat, lng) | OurAirports vía data.humdata.org | [data.humdata.org/dataset/ourairports-chl](https://data.humdata.org/dataset/ourairports-chl?) | CSV público. Usado en `Publico_Flujo_aéreo_nacional_ARClayer.ipynb`. |
| 3 | **Aeropuertos globales** (código IATA, lat, lng) | OpenDataSoft | [data.opendatasoft.com/airports-code](https://data.opendatasoft.com/explore/dataset/airports-code%40public/export/) | CSV público. Usado en `Publico_Flujo_aéreo_receptivo_GreatCircleLayer.ipynb`. |
| 4 | **Atractivos turísticos 2020** (4.881 atractivos con jerarquía, coordenadas, comuna) | SERNATUR | [XLSX](https://www.sernatur.cl/wp-content/uploads/2022/11/NACIONAL-1.zip) | Usado en `Publico_Comparación_Atractivos_y_Destinos.ipynb`. Incluye jerarquía (Local, Regional, Nacional, Internacional) y categoría. |
| 5 | **Destinos turísticos 2025** (78 destinos oficiales con polígonos geográficos) | SERNATUR | [KMZ](https://www.sernatur.cl/wp-content/uploads/2025/09/Destinos_Nacional-Publico.kmz) | Usado en `Publico_Comparación_Atractivos_y_Destinos.ipynb`. Incluye tipología, región y delimitación espacial. El notebook ya ejecuta HDBSCAN para identificar clústeres rezagados fuera de destinos oficiales. **Nota:** KMZ fechado septiembre 2025; verificar si SERNATUR ha publicado actualización posterior antes de usar en producción. |
| 6 | **Gasto turístico receptivo 2023** (proxy para componente Oportunidad) | Subsecretaría de Turismo | [PDF](https://www.subturismo.gob.cl/wp-content/uploads/2024/12/20241209-perfil-receptivo-y-emisivo-2023.pdf) (pág. 5) | No existe dato de gasto por destino. Se construye un proxy con los datos disponibles (ver detalle abajo). |

### 3.0.1 Detalle fuente 6: Proxy de gasto turístico para componente Oportunidad

El PDF "Perfil del Turista Receptivo y Emisivo 2023" no desglosa gasto por destino, pero provee datos suficientes para construir un proxy:

**Datos agregados (turista receptivo vía aérea, 2023):**
- Gasto total promedio individual: **1.027,7 USD** por visita
- Gasto diario promedio individual: **61,7 USD**
- Permanencia promedio: **16,7 noches**

**Distribución de visitas por destino (respuesta múltiple, Top 15):**

| Destino | % visitas |
|---------|-----------|
| Santiago Urbano | 77,0% |
| San Pedro de Atacama | 9,5% |
| Litoral Viña del Mar - Concón | 7,4% |
| Resto región Metropolitana | 7,0% |
| Valparaíso | 6,7% |
| P.N. Torres del Paine | 6,6% |
| Estrecho de Magallanes | 4,2% |
| Lago Llanquihue y Todos Los Santos | 3,2% |
| Araucanía Lacustre | 3,1% |
| Patagonia Costa | 3,1% |
| La Serena - Coquimbo | 3,1% |
| Concepción y alrededores | 2,3% |
| Litoral de los Poetas | 1,8% |
| Archipiélago de Chiloé | 1,5% |
| Temuco y sus alrededores | 1,4% |

**Nota:** El producto 16,7 × 61,7 = 1.030,4 USD difiere del gasto total reportado (1.027,7 USD). La discrepancia (~3 USD) se debe a que la permanencia y gasto diario reportados son promedios redondeados independientemente. Usar el gasto total (1.027,7 USD) como valor de referencia, no el producto de los promedios.

**Estrategia de proxy:** Usar solo el volumen de pasajeros **internacionales** (`OPER_2 == 'LLEGAN'`) × gasto total promedio por visita (1.027,7 USD) × % de visitas por destino como factor de ajuste (0-1). No mezclar con pasajeros domésticos, ya que el % de visitas y el gasto provienen exclusivamente de la encuesta de turismo receptivo.

```python
def calcular_ingreso_receptivo_proxy(zona, df_int, tabla_visitas_pct, aeropuertos_zona):
    """
    Proxy de ingreso turístico receptivo por zona.
    Usa SOLO pasajeros internacionales × gasto promedio.
    NOTA: Versión simplificada. Ver modules/scoring.py para implementación final
    que usa aeropuertos_por_cluster (radio) en vez de aeropuerto_cercano.
    """
    pax_int = df_int[df_int['DEST_1'].isin(aeropuertos_zona)]['Pasajeros'].sum()

    gasto_total_usd = 1027.7

    pct_visita = tabla_visitas_pct.get(zona['nombre'], 0.01)  # default 1%

    return pax_int * gasto_total_usd * pct_visita
```

> **Nota metodológica:** Los % de visitas suman más de 100% (respuesta múltiple). Se usan como factor de ajuste relativo, no como distribución del gasto total.

---

## 4. Modelo de Datos

### 4.1 `flujos_nacionales.csv` (fuente 1 → ArcLayer ipynb)

Columnas del DataFrame final del ipynb actual (`df` en celda 53):

| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| ORIG_1 | str | "Santiago" | Ciudad de origen (ya mapeada desde código IATA) |
| DEST_1 | str | "Puerto montt" | Ciudad de destino |
| Año | int | 2024 | Año del registro |
| Pasajeros | int | 245000 | Total pasajeros en la ruta (PAX_LIB + PASAJEROS) |
| lat_h | float | -33.393 | Latitud aeropuerto origen |
| lng_h | float | -70.785 | Longitud aeropuerto origen |
| lat_w | float | -41.438 | Latitud aeropuerto destino |
| lng_w | float | -73.094 | Longitud aeropuerto destino |

**Origen del dato:** Junta Aeronáutica Civil (JAC) filtrado por `NAC == 'NACIONAL'`, agrupado por ORIG_1 + DEST_1, sumando PASAJEROS_TOTAL.

**Código actual que lo genera (ipynb ArcLayer, celdas 14-53):**
```python
raw['PASAJEROS_TOTAL'] = raw['PAX_LIB'] + raw['PASAJEROS']
nacionales_raw = raw[(raw['NAC'] == 'NACIONAL') & (raw['Año'] == año)][['PASAJEROS_TOTAL', 'ORIG_1', 'DEST_1', 'Año']]
nacionales = nacionales_raw.groupby(['ORIG_1', 'DEST_1', 'Año']).agg({'PASAJEROS_TOTAL': 'sum'}).reset_index()
nacionales = nacionales.loc[nacionales['PASAJEROS_TOTAL'] > 0]
# ... merges con coordenadas de aeropuertos ...
```

### 4.2 `flujos_internacionales.csv` (fuente 1 → GreatCircleLayer ipynb)

Misma estructura que nacionales, pero filtrado por:
```python
# Para CONECTIVIDAD: ambas direcciones (LLEGAN + SALEN) → consistente con nacional
raw[(raw['NAC'] == 'INTERNACIONAL') & (raw['Año'] == año)]
# Para OPORTUNIDAD (proxy gasto receptivo): solo LLEGAN (turistas que entran)
raw[(raw['NAC'] == 'INTERNACIONAL') & (raw['OPER_2'] == 'LLEGAN') & (raw['Año'] == año)]
```
→ Se generan DOS CSVs internacionales: `flujos_int_conectividad.csv` (bidireccional) y `flujos_int_receptivo.csv` (solo LLEGAN).
Las coordenadas vienen de OpenDataSoft (dataset global) en vez de OurAirports (solo Chile).

### 4.3 `clusters_turisticos.csv` (fuentes 4 y 5 → Comparación ipynb)

| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| cluster_id | int | 1 | Identificador del cluster |
| nombre | str | "Torres del Paine" | Nombre descriptivo de la zona |
| lat | float | -51.0 | Latitud del centroide del cluster |
| lng | float | -73.0 | Longitud del centroide del cluster |
| n_atractivos | int | 15 | Cantidad de atractivos en el cluster |
| score_atractivo | float | 92.0 | Score normalizado (0-100) del atractivo |
| aeropuerto_cercano | str | "PUQ" | Código IATA del aeropuerto más cercano (referencia; el scoring usa TODOS los aeropuertos dentro de 150km vía `obtener_aeropuertos_por_cluster`) |

**Nota:** Este CSV se construirá adaptando los resultados del proyecto de clustering existente. Si el clustering actual no tiene coordenadas, se agregarán manualmente para las zonas principales.

### 4.4 `aeropuertos_chile.csv` y `aeropuertos_global.csv` (fuentes 2 y 3)

Ya existen en los ipynb actuales. Se exportarán con columnas: `codigo_iata`, `lat`, `lng`, `nombre`.

---

## 5. Lógica del Score de Oportunidad

### 5.1 Fórmula

```
Score(zona) = w₁ × Conectividad(zona) + w₂ × Atractivo(zona) + w₃ × Tendencia(zona) + w₄ × Oportunidad(zona)

Donde:
  w₁ + w₂ + w₃ + w₄ = 1.0 (ajustables por el usuario via sliders)
  Valores default: w₁=0.25, w₂=0.30, w₃=0.25, w₄=0.20
  Cada componente está normalizado en escala 0-100 (via percentiles)
```

### 5.2 Cálculo de cada componente

#### Conectividad(zona) — viene de los ipynb de flujos aéreos

> Ver implementación completa en sección 6.3 (`calcular_conectividad`).
>
> Resumen: para cada cluster, busca TODOS los aeropuertos dentro del radio y calcula `n_rutas` (rutas únicas) + `vol_pasajeros`. Normaliza sub-componentes con percentiles ANTES de ponderar (60% volumen, 40% rutas).

#### Atractivo(zona) — viene del proyecto de clustering

> Directamente `score_atractivo` del cluster (ya normalizado 0-100). No requiere función separada.

#### Crecimiento(zona) — viene del proyecto de proyección turística

> Ver implementación completa en sección 6.3 (`calcular_crecimiento`).
>
> Resumen: CAGR histórico de últimos 5 años, excluye 2020-2021 (COVID), denominador = span calendario real. Retorna `np.nan` si no hay datos → se asigna 50.0 post-normalización.

#### Oportunidad(zona) — Proxy de Ingreso Turístico Receptivo

> Ver implementación completa en sección 6.3 (`calcular_oportunidad`).
>
> Resumen: `pax_int × GASTO_TOTAL_USD × pct_visita`. Usa datos INDEPENDIENTES de Conectividad y Atractivo para eliminar doble conteo.

> **Cambio vs versión anterior:** Se reemplazó el ratio `n_atractivos / vol_pasajeros` (que medía saturación de demanda, no oportunidad) por el proxy de ingreso receptivo diseñado en sección 3.0.1. Esto: (a) usa la variable independiente `pct_visita` que no aparece en otros componentes, (b) elimina el doble conteo de `n_atractivos` y `vol_pasajeros`, (c) conecta la sección 3.0.1 con la implementación real.

### 5.3 Normalización final — Percentiles (no Min-Max)

> Ver implementación completa en sección 6.3 (`normalizar_percentil`).
>
> Más robusto ante outliers que Min-Max, pero sigue siendo relativo al tamaño de la muestra (agregar/quitar zonas SÍ puede cambiar percentiles existentes).

> **Cambio vs versión anterior:** Se reemplazó Min-Max por percentiles. Más robusto ante outliers que Min-Max, pero sigue siendo relativo al tamaño de la muestra.

---

## 6. Implementación Detallada por Archivo

### 6.1 `modules/data_loader.py`

```python
"""
Funciones para cargar y validar los CSVs del directorio data/.
Reutiliza la lógica de los ipynb originales pero refactorizada en funciones.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def _cargar_flujos(nombre_csv):
    """Carga genérica de CSV de flujos con validación de tipos."""
    df = pd.read_csv(DATA_DIR / nombre_csv)
    # Fix #12: Normalizar nombre columna → siempre 'Pasajeros'
    if 'PASAJEROS_TOTAL' in df.columns and 'Pasajeros' not in df.columns:
        df = df.rename(columns={'PASAJEROS_TOTAL': 'Pasajeros'})
    coord_cols = ['lat_h', 'lng_h', 'lat_w', 'lng_w']
    df[coord_cols] = df[coord_cols].apply(pd.to_numeric)
    return df

def cargar_flujos_nacionales():
    """Carga flujos_nacionales.csv."""
    return _cargar_flujos("flujos_nacionales.csv")

def cargar_flujos_int_conectividad():
    """Carga flujos internacionales BIDIRECCIONAL → para Conectividad."""
    return _cargar_flujos("flujos_int_conectividad.csv")

def cargar_flujos_int_receptivo():
    """Carga flujos internacionales solo LLEGAN → para Oportunidad (proxy gasto)."""
    return _cargar_flujos("flujos_int_receptivo.csv")

def cargar_clusters():
    """Carga clusters_turisticos.csv."""
    return pd.read_csv(DATA_DIR / "clusters_turisticos.csv")

def cargar_aeropuertos():
    """Carga aeropuertos_chile.csv."""
    return pd.read_csv(DATA_DIR / "aeropuertos_chile.csv")

def cargar_historico():
    """Carga serie histórica de pasajeros por aeropuerto y año."""
    path = DATA_DIR / "historico_pasajeros.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=['aeropuerto', 'Año', 'Pasajeros'])
```

### 6.2 `modules/maps.py`

```python
"""
Funciones pydeck para las 3 capas del mapa.
Refactorización directa del código de los ipynb existentes.
"""

import pydeck as pdk

def crear_arc_layer(df_nacionales):
    """
    Capa de flujos aéreos nacionales.

    REUTILIZA: Lógica exacta de celda 61 del ipynb ArcLayer.
    Colores: Rojo (origen) → Verde (destino)
    """
    return pdk.Layer(
        'ArcLayer',
        data=df_nacionales,
        get_width='Pasajeros / 50000',
        get_source_position=['lng_h', 'lat_h'],
        get_target_position=['lng_w', 'lat_w'],
        get_tilt=15,
        get_source_color=[240, 100, 0, 40],
        get_target_color=[0, 255, 0, 40],
        pickable=True,
        auto_highlight=True,
    )

def crear_great_circle_layer(df_internacionales):
    """
    Capa de flujos aéreos internacionales.

    REUTILIZA: Lógica exacta de celda 59 del ipynb GreatCircleLayer.
    Colores: Verde (origen) → Azul (destino)
    """
    return pdk.Layer(
        "GreatCircleLayer",
        data=df_internacionales,
        pickable=True,
        get_stroke_width=12,
        get_source_position=['lng_h', 'lat_h'],
        get_target_position=['lng_w', 'lat_w'],
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
    )

def crear_cluster_layer(df_clusters):
    """
    Capa de clusters turísticos como círculos coloreados por score.

    NUEVA: No existe en los ipynb actuales.
    Color: Score alto → Rojo intenso, Score bajo → Azul
    Tamaño: Proporcional a n_atractivos
    """
    return pdk.Layer(
        "ScatterplotLayer",
        data=df_clusters,
        get_position=['lng', 'lat'],
        get_radius='n_atractivos * 5000',
        get_fill_color=(
            '[255 * score_final / 100, 50, '
            '255 - (255 * score_final / 100), 160]'
        ),
        pickable=True,
        auto_highlight=True,
    )

def crear_mapa(capas_activas, df_nac, df_int, df_clusters):
    """
    Compone el mapa final con las capas seleccionadas.

    Vista: Centrada en Chile, misma vista del ipynb ArcLayer (celda 61).
    """
    layers = []
    if 'Nacional' in capas_activas:
        layers.append(crear_arc_layer(df_nac))
    if 'Internacional' in capas_activas:
        layers.append(crear_great_circle_layer(df_int))
    if 'Clusters' in capas_activas:
        layers.append(crear_cluster_layer(df_clusters))

    view_state = pdk.ViewState(
        latitude=-33.32,
        longitude=-70.89,
        bearing=45,
        pitch=50,
        zoom=4,
    )

    tooltip = {
        'html': '<b>{nombre}</b><br/>Score: {score_final}<br/>Pasajeros/año: {vol_pasajeros}',
        'style': {'backgroundColor': 'steelblue', 'color': 'white'}
    }

    return pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)
```

### 6.3 `modules/scoring.py`

```python
"""
Cálculo del Score de Oportunidad de Inversión Turística.
Combina 4 componentes de los proyectos existentes del portafolio.
"""

import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# ── Constantes para proxy de gasto receptivo ──
TABLA_VISITAS_PCT = {
    "Santiago Urbano": 0.770,
    "San Pedro de Atacama": 0.095,
    "Litoral Viña del Mar - Concón": 0.074,
    "Resto región Metropolitana": 0.070,
    "Valparaíso": 0.067,
    "P.N. Torres del Paine": 0.066,
    "Estrecho de Magallanes": 0.042,
    "Lago Llanquihue y Todos Los Santos": 0.032,
    "Araucanía Lacustre": 0.031,
    "Patagonia Costa": 0.031,
    "La Serena - Coquimbo": 0.031,
    "Concepción y alrededores": 0.023,
    "Litoral de los Poetas": 0.018,
    "Archipiélago de Chiloé": 0.015,
    "Temuco y sus alrededores": 0.014,
}
DEFAULT_PCT = 0.005
GASTO_TOTAL_USD = 1027.7

RADIO_AEROPUERTOS_KM = 150  # Radio para buscar aeropuertos cercanos
EARTH_RADIUS_KM = 6371


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia en km entre dos puntos geográficos."""
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat / 2) ** 2
         + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2)
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


def obtener_aeropuertos_por_cluster(df_clusters, df_aeropuertos, radio_km=RADIO_AEROPUERTOS_KM):
    """
    Para cada cluster, encuentra TODOS los aeropuertos dentro del radio.
    Devuelve dict {cluster_id: [lista_codigos_iata]}.

    Fix #10: antes se usaba solo aeropuerto_cercano (1 aeropuerto).
    Ahora suma pasajeros de todos los aeropuertos accesibles.
    Ej: Torres del Paine → [PUQ, PMC] en vez de solo [PUQ].
    """
    resultado = {}
    for _, zona in df_clusters.iterrows():
        cercanos = []
        for _, aero in df_aeropuertos.iterrows():
            dist = haversine_km(zona['lat'], zona['lng'],
                                aero['lat'], aero['lng'])
            if dist <= radio_km:
                cercanos.append(aero['codigo_iata'])
        # Fallback: si ninguno en radio, usar el más cercano
        if not cercanos:
            dists = df_aeropuertos.apply(
                lambda a: haversine_km(zona['lat'], zona['lng'], a['lat'], a['lng']),
                axis=1
            )
            cercanos = [df_aeropuertos.loc[dists.idxmin(), 'codigo_iata']]
        resultado[zona['cluster_id']] = cercanos
    return resultado


def normalizar_percentil(serie):
    """
    Normalización por percentil a rango 0-100.
    Más robusto ante outliers que Min-Max, pero sigue siendo
    relativo al tamaño de la muestra.
    """
    if len(serie) < 2 or serie.nunique() == 1:
        return pd.Series([50] * len(serie), index=serie.index)
    return serie.rank(pct=True) * 100


def calcular_conectividad(df_clusters, df_nac, df_int, aeropuertos_por_cluster):
    """
    Calcula conectividad aérea por zona.
    - Usa TODOS los aeropuertos del cluster (no solo el más cercano).
    - Internacional: bidireccional (ORIG + DEST), consistente con nacional.
    - Normaliza sub-componentes con percentiles ANTES de ponderar.
    """
    resultados = []
    for _, zona in df_clusters.iterrows():
        aeropuertos = aeropuertos_por_cluster.get(zona['cluster_id'], [])

        # Nacional: bidireccional
        rutas_nac = df_nac[
            (df_nac['ORIG_1'].isin(aeropuertos)) |
            (df_nac['DEST_1'].isin(aeropuertos))
        ]
        # Internacional: bidireccional (fix #6)
        rutas_int = df_int[
            (df_int['ORIG_1'].isin(aeropuertos)) |
            (df_int['DEST_1'].isin(aeropuertos))
        ]

        resultados.append({
            'cluster_id': zona['cluster_id'],
            'vol_pasajeros': rutas_nac['Pasajeros'].sum() + rutas_int['Pasajeros'].sum(),
            'n_rutas': (
                len(rutas_nac[['ORIG_1', 'DEST_1']].drop_duplicates())
                + len(rutas_int[['ORIG_1', 'DEST_1']].drop_duplicates())
            ),
        })

    df_res = pd.DataFrame(resultados)
    df_res['vol_norm'] = normalizar_percentil(df_res['vol_pasajeros'])
    df_res['rutas_norm'] = normalizar_percentil(df_res['n_rutas'])
    df_res['conectividad_raw'] = df_res['vol_norm'] * 0.6 + df_res['rutas_norm'] * 0.4

    return df_res


def calcular_oportunidad(df_clusters, df_int_receptivo, aeropuertos_por_cluster):
    """
    Proxy de ingreso turístico receptivo por zona.
    Usa datos INDEPENDIENTES de Conectividad y Atractivo:
    - pax_int: pasajeros internacionales que LLEGAN (df_int_receptivo)
    - pct_visita: % de turistas receptivos que visitan el destino
    - GASTO_TOTAL_USD: gasto promedio por visita
    """
    resultados = []
    for _, zona in df_clusters.iterrows():
        aeropuertos = aeropuertos_por_cluster.get(zona['cluster_id'], [])
        pax_int = df_int_receptivo[
            df_int_receptivo['DEST_1'].isin(aeropuertos)
        ]['Pasajeros'].sum()

        pct_visita = TABLA_VISITAS_PCT.get(zona['nombre'], DEFAULT_PCT)
        ingreso_proxy = pax_int * GASTO_TOTAL_USD * pct_visita

        resultados.append({
            'cluster_id': zona['cluster_id'],
            'ingreso_receptivo_proxy': ingreso_proxy,
        })
    return pd.DataFrame(resultados)


def calcular_crecimiento(zona, df_historico, aeropuertos_por_cluster,
                         ventana_anios=5):
    """
    CAGR histórico de los últimos `ventana_anios` años.
    Excluye 2020-2021 (COVID). Denominador = span calendario real.
    Retorna np.nan si no hay datos → se asigna 50.0 post-normalización.
    """
    aeropuertos = aeropuertos_por_cluster.get(zona['cluster_id'], [])
    serie = df_historico[df_historico['aeropuerto'].isin(aeropuertos)].copy()
    serie = serie.groupby('Año')['Pasajeros'].sum().reset_index()
    serie = serie.sort_values('Año')
    serie = serie[~serie['Año'].isin([2020, 2021])]

    if len(serie) < 2:
        return np.nan

    serie_reciente = serie.tail(ventana_anios + 1)

    if len(serie_reciente) < 2:
        return np.nan

    primer_valor = serie_reciente['Pasajeros'].iloc[0]
    ultimo_valor = serie_reciente['Pasajeros'].iloc[-1]
    anio_inicio = serie_reciente['Año'].iloc[0]
    anio_fin = serie_reciente['Año'].iloc[-1]
    n_anios = anio_fin - anio_inicio

    if primer_valor <= 0 or n_anios <= 0:
        return np.nan

    cagr = (ultimo_valor / primer_valor) ** (1 / n_anios) - 1
    return cagr


def calcular_score_final(df_clusters, df_nac, df_int, df_int_receptivo,
                         df_historico, aero_map, pesos):
    """
    Calcula el score compuesto para cada zona.

    pesos: dict con keys 'conectividad', 'atractivo', 'tendencia', 'oportunidad'
           valores entre 0 y 1, deben sumar 1.
    aero_map: dict {cluster_id: [codigos_iata]} — precalculado en app.py.

    Inputs separados para eliminar doble conteo:
    - df_int: flujos internacionales BIDIRECCIONAL → Conectividad
    - df_int_receptivo: flujos internacionales solo LLEGAN → Oportunidad
    """

    # Paso 1: Conectividad (usa df_int bidireccional)
    df_conect = calcular_conectividad(df_clusters, df_nac, df_int, aero_map)
    df = df_clusters.merge(df_conect, on='cluster_id')
    df['conectividad'] = normalizar_percentil(df['conectividad_raw'])

    # Paso 2: Atractivo (ya normalizado 0-100 en el CSV)
    df['atractivo'] = df['score_atractivo']

    # Paso 3: Tendencia histórica (CAGR con años reales)
    if df_historico is not None and len(df_historico) > 0:
        cagrs = df_clusters.apply(
            lambda z: calcular_crecimiento(z, df_historico, aero_map), axis=1
        )
        df['crecimiento_raw'] = cagrs
        # Normalizar solo valores reales; NaN = zonas sin datos
        mask_valid = df['crecimiento_raw'].notna()
        df.loc[mask_valid, 'tendencia'] = normalizar_percentil(
            df.loc[mask_valid, 'crecimiento_raw']
        )
        df['tendencia'] = df['tendencia'].fillna(50.0)
    else:
        df['tendencia'] = 50.0

    # Paso 4: Oportunidad (proxy gasto receptivo — datos independientes)
    df_oport = calcular_oportunidad(df_clusters, df_int_receptivo, aero_map)
    df = df.merge(df_oport, on='cluster_id')
    df['oportunidad'] = normalizar_percentil(df['ingreso_receptivo_proxy'])

    # Score final ponderado
    df['score_final'] = (
        pesos['conectividad'] * df['conectividad'] +
        pesos['atractivo'] * df['atractivo'] +
        pesos['tendencia'] * df['tendencia'] +
        pesos['oportunidad'] * df['oportunidad']
    ).round(1)

    return df.sort_values('score_final', ascending=False)
```

### 6.4 `modules/charts.py`

```python
"""
Gráficos Plotly para el panel de análisis.
"""

import plotly.graph_objects as go
import plotly.express as px

def grafico_ranking_top10(df_zonas):
    """Bar chart horizontal con las top 10 zonas por score."""
    top10 = df_zonas.nlargest(10, 'score_final')
    fig = px.bar(
        top10, x='score_final', y='nombre',
        orientation='h',
        color='score_final',
        color_continuous_scale='RdYlGn',
        labels={'score_final': 'Score', 'nombre': ''},
    )
    fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
    return fig

def grafico_componentes_score(zona):
    """Barras horizontales mostrando cada componente del score de una zona."""
    componentes = ['Conectividad', 'Atractivo', 'Tendencia', 'Oportunidad']
    valores = [zona['conectividad'], zona['atractivo'], zona['tendencia'], zona['oportunidad']]
    colores = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

    fig = go.Figure(go.Bar(
        x=valores, y=componentes,
        orientation='h',
        marker_color=colores,
        text=[f'{v:.0f}/100' for v in valores],
        textposition='inside',
    ))
    fig.update_layout(
        height=250,
        xaxis_range=[0, 100],
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"Score: {zona['score_final']:.0f}/100"
    )
    return fig

def grafico_tendencia_historica(zona, df_historico, aeropuertos_por_cluster):
    """
    Línea de tendencia histórica de pasajeros (últimos 5-7 años).
    Muestra datos REALES, no proyecciones cosméticas.
    Marca años COVID (2020-2021) con color distinto.
    Incluye CAGR real como anotación.
    """
    aeropuertos = aeropuertos_por_cluster.get(zona['cluster_id'], [])
    serie = df_historico[df_historico['aeropuerto'].isin(aeropuertos)]
    serie = serie.groupby('Año')['Pasajeros'].sum().reset_index()
    serie = serie.sort_values('Año').tail(8)

    if len(serie) == 0:
        return go.Figure()  # vacío si no hay datos

    colores = ['rgba(231,76,60,0.6)' if a in [2020, 2021]
               else 'rgba(52,152,219,0.9)' for a in serie['Año']]

    fig = go.Figure(go.Bar(
        x=serie['Año'], y=serie['Pasajeros'],
        marker_color=colores,
        text=[f'{p:,.0f}' for p in serie['Pasajeros']],
        textposition='outside',
    ))

    cagr = zona.get('crecimiento_raw', None)
    titulo = f"CAGR real: {cagr:+.1%}" if cagr is not None else "Sin datos CAGR"
    fig.update_layout(
        height=200,
        xaxis_title='Año',
        yaxis_title='Pasajeros',
        margin=dict(l=0, r=0, t=30, b=40),
        title=titulo,
    )
    return fig
```

### 6.5 `app.py` (aplicación principal)

```python
"""
Tourism Investment Atlas — App principal Streamlit.
Integra flujos aéreos, clustering turístico, tendencia histórica y proxy de ingreso.
"""

import streamlit as st
from modules.data_loader import (
    cargar_flujos_nacionales, cargar_flujos_int_conectividad,
    cargar_flujos_int_receptivo, cargar_clusters, cargar_aeropuertos,
    cargar_historico
)
from modules.scoring import (
    calcular_score_final, obtener_aeropuertos_por_cluster
)
from modules.maps import crear_mapa
from modules.charts import (
    grafico_ranking_top10, grafico_componentes_score,
    grafico_tendencia_historica
)

# ── Configuración de página ──
st.set_page_config(page_title="Tourism Investment Atlas", layout="wide")
st.title("Tourism Investment Atlas — Chile")

# ── Carga de datos ──
df_nac = cargar_flujos_nacionales()
df_int = cargar_flujos_int_conectividad()       # bidireccional → Conectividad
df_int_recep = cargar_flujos_int_receptivo()     # solo LLEGAN → Oportunidad
df_clusters = cargar_clusters()
df_aeropuertos = cargar_aeropuertos()
df_historico = cargar_historico()

# ── Sidebar: Filtros y Pesos ──
with st.sidebar:
    st.header("Configuración")

    st.subheader("Capas del mapa")
    capas = []
    if st.checkbox("Vuelos nacionales", value=True):
        capas.append('Nacional')
    if st.checkbox("Vuelos internacionales", value=True):
        capas.append('Internacional')
    if st.checkbox("Clusters turísticos", value=True):
        capas.append('Clusters')

    st.subheader("Pesos del Score")
    w_conect = st.slider("Conectividad aérea", 0, 100, 25)
    w_atract = st.slider("Atractivo turístico", 0, 100, 30)
    w_tend = st.slider("Tendencia histórica", 0, 100, 25)
    w_oportunidad = st.slider("Oportunidad de mercado", 0, 100, 20)

    total = w_conect + w_atract + w_tend + w_oportunidad
    if total == 0:
        total = 1
        st.warning("Todos los pesos están en 0. Ajusta al menos uno.")

    pesos = {
        'conectividad': w_conect / total,
        'atractivo': w_atract / total,
        'tendencia': w_tend / total,
        'oportunidad': w_oportunidad / total,
    }

    # Fix #9: Mostrar pesos EFECTIVOS → usuario entiende que son proporciones
    st.caption("**Pesos efectivos:**")
    st.caption(
        f"Conectiv. {pesos['conectividad']:.0%} · "
        f"Atract. {pesos['atractivo']:.0%} · "
        f"Tend. {pesos['tendencia']:.0%} · "
        f"Oport. {pesos['oportunidad']:.0%}"
    )
    if total != 100:
        st.info(f"Suma sliders = {total}. Se normalizan a 100%.")

# ── Calcular aero_map UNA vez (O(clusters × aeropuertos)) ──
aero_map = obtener_aeropuertos_por_cluster(df_clusters, df_aeropuertos)

# ── Cálculo del Score ──
df_scored = calcular_score_final(
    df_clusters, df_nac, df_int, df_int_recep,
    df_historico, aero_map, pesos
)

# ── Mapa Principal ──
mapa = crear_mapa(capas, df_nac, df_int, df_scored)
st.pydeck_chart(mapa)

# ── Panel Inferior (3 columnas — consistente con mockup, fix #7) ──
col1, col2, col3 = st.columns([1, 1, 1])

# Columna 1: Zona seleccionada (resumen rápido)
with col1:
    st.subheader("Zona Seleccionada")
    zona_seleccionada = st.selectbox(
        "Selecciona una zona:",
        df_scored['nombre'].tolist()
    )
    zona = df_scored[df_scored['nombre'] == zona_seleccionada].iloc[0]

    st.metric("Score", f"{zona['score_final']:.0f}/100")
    st.metric("Pasajeros/año", f"{zona.get('vol_pasajeros', 0):,.0f}")
    st.metric("Rutas directas", f"{zona.get('n_rutas', 0)}")

    cagr = zona.get('crecimiento_raw', None)
    if cagr is not None:
        st.metric("CAGR 5 años", f"{cagr:+.1%}")

# Columna 2: Top 10 ranking
with col2:
    st.subheader("Top 10 Zonas")
    st.plotly_chart(grafico_ranking_top10(df_scored), use_container_width=True)

# Columna 3: Detalle de zona
with col3:
    st.subheader("Detalle")
    st.plotly_chart(grafico_componentes_score(zona), use_container_width=True)

    st.plotly_chart(
        grafico_tendencia_historica(zona, df_historico, aero_map),
        use_container_width=True
    )
```

### 6.6 `requirements.txt`

```
streamlit>=1.30.0
pydeck>=0.9.0
plotly>=5.18.0
pandas>=2.0.0
numpy>=1.24.0
```

### 6.7 `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#2c3e50"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#2c3e50"
```

---

## 7. Integración con Jekyll Site

### 7.1 Nuevo archivo: `_projects/investment-atlas.md`

```markdown
---
layout: project
title: "Tourism Investment Atlas"
category: Visualización de Datos
description: "Atlas interactivo que cruza flujos aéreos, atractivos turísticos y proyecciones
de demanda para identificar zonas de oportunidad de inversión turística en Chile."
github_url: "https://github.com/manuelsancristobal/tourism-investment-atlas"
app_url: "https://tourism-investment-atlas.streamlit.app"
---

## Visualización Interactiva

Mapa multicapa que integra flujos aéreos nacionales e internacionales,
clusters de atractivos turísticos y un modelo de scoring de oportunidad de inversión.

{::nomarkdown}
<div style="position: relative; width: 100%; padding-bottom: 75%; overflow: hidden;">
  <iframe
    src="https://tourism-investment-atlas.streamlit.app/?embedded=true"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
    loading="lazy"
    title="Tourism Investment Atlas">
  </iframe>
</div>
{:/nomarkdown}

## Metodología

El **Score de Oportunidad** (0-100) combina cuatro dimensiones ponderables:
- **Conectividad aérea** (25%): volumen de pasajeros y rutas directas
- **Atractivo turístico** (30%): densidad y calidad del cluster
- **Tendencia histórica** (25%): CAGR de pasajeros a 5 años (excl. COVID)
- **Oportunidad de mercado** (20%): proxy de ingreso turístico receptivo (gasto × % visitas)

> **Disclaimer:** El Score de Oportunidad es un indicador relativo para priorizar zonas de exploración. No reemplaza un estudio de factibilidad financiera.

## Fuentes de Datos

- [Junta Aeronáutica Civil](https://www.jac.gob.cl/estadisticas/estadisticas-historicas/) — Estadísticas de vuelos
- [OurAirports](https://data.humdata.org/dataset/ourairports-chl) — Georreferenciación aeropuertos Chile
- [OpenDataSoft](https://data.opendatasoft.com/) — Aeropuertos globales
```

### 7.2 Modificación: `_layouts/project.html`

Agregar soporte para el campo `app_url` en el frontmatter, para mostrar un botón "Ver App en Vivo" junto al botón de GitHub:

**Cambio en `_layouts/project.html`** — después del bloque `{% if page.github_url %}`:

```html
{% if page.app_url %}
<a href="{{ page.app_url }}" class="btn-project" target="_blank" style="margin-left: 1rem;">
    <i class="fas fa-external-link-alt"></i> Ver App en Vivo
</a>
{% endif %}
```

**Archivo a modificar:** `_layouts/project.html` en el repo `manuelsancristobal.github.io`
**Línea aproximada:** Dentro del bloque `<div class="project-links">`, después del link de GitHub.

---

## 8. Fases de Implementación (paso a paso)

### Fase 1: Preparación de datos (carpeta actual ArcLayer)
1. Abrir `Publico_Flujo_aéreo_nacional_ARClayer.ipynb`
2. Corregir el `SettingWithCopyWarning` en celda 23-24:
   ```python
   raw_ciudades = raw[['ORIG_1', 'ORIG_1_N']].copy()  # Agregar .copy()
   ```
3. Agregar celda al final que exporte el DataFrame `df` a CSV:
   ```python
   df.to_csv('data/flujos_nacionales.csv', index=False)
   ```
4. Repetir para `Publico_Flujo_aéreo_receptivo_GreatCircleLayer.ipynb`
5. Exportar los DataFrames de aeropuertos a CSVs separados
6. Crear `clusters_turisticos.csv` adaptando los resultados del proyecto de clustering (agregar coordenadas y aeropuerto_cercano)

### Fase 2: Crear repositorio `tourism-investment-atlas`
1. `git init tourism-investment-atlas`
2. Crear la estructura de directorios (`data/`, `modules/`, `.streamlit/`, `notebooks/`)
3. Copiar los CSVs generados en Fase 1 al directorio `data/`
4. Crear `requirements.txt`
5. Crear `.streamlit/config.toml`

### Fase 3: Implementar módulos Python
1. Crear `modules/__init__.py` (vacío)
2. Crear `modules/data_loader.py` (código en sección 6.1)
3. Crear `modules/scoring.py` (código en sección 6.3)
4. Crear `modules/maps.py` (código en sección 6.2)
5. Crear `modules/charts.py` (código en sección 6.4)

### Fase 4: Implementar app.py
1. Crear `app.py` (código en sección 6.5)
2. Testear localmente: `streamlit run app.py`
3. Verificar que las 3 capas del mapa se renderizan
4. Verificar que los sliders recalculan el score
5. Verificar que el ranking y detalle de zona funcionan

### Fase 5: Deploy en Streamlit Cloud
1. Push del repo a GitHub: `git push -u origin main`
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repo `manuelsancristobal/tourism-investment-atlas`
4. Seleccionar `app.py` como archivo principal
5. Deploy automático → URL tipo `tourism-investment-atlas.streamlit.app`

### Fase 6: Integrar en Jekyll site
1. En el repo `manuelsancristobal.github.io`:
2. Crear `_projects/investment-atlas.md` (contenido en sección 7.1)
3. Editar `_layouts/project.html` para agregar botón `app_url` (sección 7.2)
4. Push → GitHub Pages se actualiza automáticamente

---

## 9. Verificación End-to-End

| # | Test | Resultado esperado |
|---|------|--------------------|
| 1 | `streamlit run app.py` ejecuta sin errores | App se abre en localhost:8501 |
| 2 | Mapa muestra arcos nacionales (rojos/verdes) | Arcos sobre Chile como en ipynb actual |
| 3 | Mapa muestra arcos internacionales (verdes/azules) | Great circles como en ipynb actual |
| 4 | Mapa muestra círculos de clusters | Puntos coloreados por score |
| 5 | Checkboxes prenden/apagan capas | Capas aparecen/desaparecen |
| 6 | Sliders de pesos cambian el score | Ranking se reordena, colores cambian |
| 7 | Seleccionar zona muestra detalle | Gráfico de componentes + métricas |
| 8 | App deployada en Streamlit Cloud | URL pública accesible |
| 9 | iframe en Jekyll carga la app | Visualización embebida funciona |
| 10 | Página aparece en listado de proyectos | Card visible en homepage del portafolio |

---

## 10. Resumen de Archivos a Crear/Modificar

### Repo nuevo: `tourism-investment-atlas`
| Archivo | Acción |
|---------|--------|
| `app.py` | Crear |
| `requirements.txt` | Crear |
| `.streamlit/config.toml` | Crear |
| `data/flujos_nacionales.csv` | Crear (exportar de ipynb) |
| `data/flujos_int_conectividad.csv` | Crear (internacional bidireccional) |
| `data/flujos_int_receptivo.csv` | Crear (internacional solo LLEGAN) |
| `data/clusters_turisticos.csv` | Crear (adaptar de proyecto clustering) |
| `data/aeropuertos_chile.csv` | Crear (exportar de ipynb) |
| `data/aeropuertos_global.csv` | Crear (exportar de ipynb) |
| `data/historico_pasajeros.csv` | Crear (serie histórica por aeropuerto) |
| `modules/__init__.py` | Crear |
| `modules/data_loader.py` | Crear |
| `modules/scoring.py` | Crear |
| `modules/maps.py` | Crear |
| `modules/charts.py` | Crear |
| `README.md` | Crear |

### Repo existente: `manuelsancristobal.github.io`
| Archivo | Acción |
|---------|--------|
| `_projects/investment-atlas.md` | Crear |
| `_layouts/project.html` | Editar (agregar soporte app_url) |

### Carpeta actual: `ArcLayer`
| Archivo | Acción |
|---------|--------|
| `Publico_Flujo_aéreo_nacional_ARClayer.ipynb` | Editar (fix warnings + exportar CSV) |
| `Publico_Flujo_aéreo_receptivo_GreatCircleLayer.ipynb` | Editar (fix warnings + exportar CSV) |
