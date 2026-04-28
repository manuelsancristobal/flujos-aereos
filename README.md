# Flujos Aéreos - Deck.gl Arc Layer Visualization

## Impacto y Valor del Proyecto
Este proyecto visualiza la conectividad aérea de Chile mediante mapas de arcos (Deck.gl), permitiendo un análisis exploratorio de los flujos de pasajeros y carga. Al cruzar los datos de tráfico de la JAC con la ubicación de clusters turísticos, la herramienta identifica nodos críticos de infraestructura y oportunidades de inversión en zonas con alta demanda aérea pero sub-representación en servicios turísticos locales. Es una solución avanzada de Business Intelligence geoespacial para el sector aeronáutico y turístico.

## Stack Tecnológico
- **Lenguaje**: Python 3.10+
- **Librerías Clave**: `Pandas`, `Numpy`, `Deck.gl` (Frontend), `Pydeck`.
- **Calidad de Código**: `Ruff`, `Pytest`.
- **CI/CD**: GitHub Actions.

## Arquitectura de Datos y Metodología
1. **Pipeline ETL**: Procesamiento de microdatos de la JAC para agregar flujos por par origen-destino mensual.
2. **Geolocalización**: Enriquecimiento de flujos con coordenadas IATA para aeropuertos globales y nacionales.
3. **Métricas de Conectividad**: Cálculo de indicadores de intensidad de flujo y estacionalidad.
4. **Visualización**: Renderizado de capas Arc Layer dinámicas que representan volumen mediante grosor y color del arco.

## Quick Start (Reproducibilidad)
1. `git clone https://github.com/manuelsancristobal/flujos-aereos`
2. `pip install -e .`
3. `make test`
4. `python run.py etl` (Genera los JSONs de flujos)
5. `python run.py ver` (Inicia el servidor para la visualización Deck.gl)

## Estructura del Proyecto
- `src/`: Lógica de procesamiento de flujos y configuración.
- `data/`: Datos históricos de la JAC y catálogos de aeropuertos (`raw/`, `external/`).
- `viz/`: Template HTML/JS para la visualización Deck.gl.
- `scripts/`: Scripts de análisis de tráfico específicos.

---
**Autor**: Manuel San Cristóbal Opazo 
**Licencia**: MIT
