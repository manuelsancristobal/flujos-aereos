---
layout: project
title: "Flujos Aéreos de Chile"
category: Visualización de Datos
description: Análisis geoespacial interactivo del tráfico aéreo nacional e internacional, incluyendo pasajeros y carga.
github_url: "https://github.com/manuelsancristobal/flujos-aereos"
image: "/proyectos/flujos-aereos/preview.png"
tech_stack:
  - Python (Pandas)
  - Deck.gl
  - MapLibre
  - JavaScript
---

Bienvenido a la exploración interactiva de los cielos chilenos. Esta herramienta permite visualizar dinámicamente cómo se mueve el país a través de sus rutas aéreas, integrando datos de pasajeros y carga para revelar los patrones de conectividad que definen nuestro espacio aéreo. A continuación, puedes interactuar con el mapa o profundizar en el análisis detallado de los hallazgos.

## Visualización de Flujos Interactiva

Esta herramienta utiliza **Deck.gl** para representar la dinámica del transporte aéreo. Como se observa en la capa de `ArcLayer`, el sistema integra datos de la Junta de Aeronáutica Civil (JAC) para ofrecer una visión de pasajeros y carga.

<div class="project-viz-container" style="height: 600px; border-radius: 8px; overflow: hidden; margin: 20px 0; border: 1px solid #ddd;">
    <iframe src="/proyectos/flujos-aereos/viz.html" width="100%" height="100%" frameborder="0" allowfullscreen></iframe>
</div>

[Ver en pantalla completa](/proyectos/flujos-aereos/viz.html){: .btn .btn--primary }

### Características de la Herramienta
*   **Métricas Duales**: Alternancia entre **Pasajeros** y **Carga (Tonelaje)**.
*   **Perspectiva Doble**: Flujos **Emisivos** y **Receptivos**.
*   **Control Temporal**: Deslizador para observar la evolución de las rutas año tras año.
*   **Optimización**: Uso de arcos para trayectorias de gran volumen de datos.

---

## Hallazgos Clave en la Dinámica Aérea

A partir de la exploración de estos flujos, se han identificado patrones críticos que definen la estructura y comportamiento del sector en Chile:

### 1. El Nodo Santiago (SCL) como Centro de Gravedad
La visualización geoespacial confirma la posición de Santiago como el eje central del sistema aéreo chileno. Como se aprecia en la perspectiva **Emisiva**, existe una diversificación hacia destinos regionales en Sudamérica. La entrada de aerolíneas *low-cost* ha transformado rutas en el pasado marginales en conexiones de alto volumen.

### 2. Rutas Críticas y Puentes Globales
Como se vio en las trayectorias de círculos máximos del mapa, las rutas hacia Bogotá, Lima y São Paulo son puntos de conexión vitales hacia el resto del mundo. Los vuelos directos a Europa (Madrid, París) actúan de forma estratégica como puentes para el comercio y el turismo de alto valor.

### 3. Estacionalidad en Flujos Receptivos
El tráfico **Receptivo** revela una concentración de fuerza en el verano austral (enero-febrero). Las trayectorias desde Europa y Norteamérica muestran una densidad de arco superior en este periodo en la visualización. Este patrón valida la necesidad de infraestructura para gestionar peaks de demanda en nodos estratégicos.

### 4. Resiliencia de la Carga ante Crisis
Al contrastar las métricas se observa que los flujos de mercancías presentan una estabilidad mayor ante choques externos. Mientras el tráfico de pasajeros muestra fluctuaciones de temporada marcadas y una sensibilidad extrema a crisis, el transporte de carga mantiene una base constante. Esta solidez, analizada en profundidad en la serie histórica del [**Bar Chart Race: Movimiento Aéreo**](/proyectos/barchart-race/), se vincula en especial a las cadenas de suministro hacia Norteamérica y Asia.

<div class="methodology-box" style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-light); border-radius: 8px; border-left: 4px solid var(--secondary);">
    <p style="margin: 0; font-size: 0.95rem;">📌 <strong>Sobre este proyecto:</strong> Esta es la versión rediseñada como aplicación interactiva. Los notebooks desarrollados anteriormente están disponibles en Google Colab: <a href="https://colab.research.google.com/drive/1cOEHEMJTM6fkYkYqst9__5AVDlQaO9e2" target="_blank" style="color: var(--secondary); font-weight: 600;">Flujo Aéreo Nacional ArcLayer</a> y <a href="https://colab.research.google.com/drive/1woxG5EvWJUKDoNDW8hDxYpKaxP5So1RE" target="_blank" style="color: var(--secondary); font-weight: 600;">Flujo Aéreo Nacional GreatCircleLayer</a>.</p>
</div>
