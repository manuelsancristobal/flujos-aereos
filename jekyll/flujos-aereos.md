---
layout: project
title: "ArcLayer: Flujos Aéreos de Chile"
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

## Visualización de Flujos Aéreos

Esta herramienta permite explorar la dinámica del transporte aéreo en Chile mediante una interfaz geoespacial interactiva basada en **Deck.gl**. El proyecto integra datos de la Junta de Aeronáutica Civil (JAC) para ofrecer una visión completa tanto de pasajeros como de carga.

### Características Principales

*   **Multidimensional**: Permite alternar entre métricas de **Pasajeros** y **Carga (Tonelaje)**.
*   **Doble Perspectiva**: Visualización de flujos **Emisivos** (desde Chile al mundo) y **Receptivos** (llegadas al país).
*   **Análisis Histórico**: Control deslizante para observar la evolución de las rutas año tras año.
*   **Tecnología Geoespacial**: Uso de `ArcLayer` para representar trayectorias de círculos máximos, optimizado para grandes volúmenes de datos.

### Visualización Interactiva

<div class="project-viz-container" style="height: 600px; border-radius: 8px; overflow: hidden; margin: 20px 0; border: 1px solid #ddd;">
    <iframe src="/proyectos/flujos-aereos/viz.html" width="100%" height="100%" frameborder="0"></iframe>
</div>

[Ver en pantalla completa](/proyectos/flujos-aereos/viz.html){: .btn .btn--primary }

### Impacto y Aplicaciones

Este análisis es fundamental para identificar:
1.  **Hubs Logísticos**: Destinos con alta carga relativa que funcionan como centros de distribución.
2.  **Polos Turísticos**: Rutas con alto volumen de pasajeros que conectan con los principales atractivos del país.
3.  **Conectividad Regional**: La importancia del Aeropuerto de Santiago (SCL) como nodo central y el crecimiento de rutas interregionales.

## Análisis de Dinámicas Aéreas

### 1. Resiliencia de la Carga vs. Volatilidad de Pasajeros
Al contrastar las métricas de **Pasajeros** y **Carga**, se observa que los flujos de mercancías presentan una mayor estabilidad ante choques externos. Mientras que el tráfico de pasajeros muestra fluctuaciones estacionales marcadas y una sensibilidad extrema a crisis sanitarias o económicas, el transporte de carga mantiene una base constante vinculada a las cadenas de suministro internacionales, especialmente en rutas hacia Norteamérica y Asia.

### 2. Estacionalidad y Flujos Receptivos
El análisis del tráfico **Receptivo** revela una fuerte concentración en los meses de verano austral (enero-febrero), impulsado por el turismo de larga distancia. Las trayectorias provenientes de Europa y Norteamérica muestran una densidad de arco superior en este período, lo que valida la necesidad de una infraestructura aeroportuaria capaz de gestionar peaks de demanda estacionales en nodos estratégicos como SCL.

### 3. El Nodo Santiago (SCL) como Hub Regional
La visualización geoespacial confirma la posición de Santiago como el centro de gravedad del sistema aéreo chileno. Sin embargo, la perspectiva **Emisiva** muestra una diversificación creciente hacia destinos regionales en Sudamérica, evidenciando un mercado cada vez más integrado donde las aerolíneas *low-cost* han transformado rutas anteriormente marginales en conexiones de alto volumen.

### 4. Rutas Críticas y Conectividad Global
Las trayectorias de círculos máximos permiten identificar las "rutas críticas" de conectividad para Chile. La densidad de los flujos hacia Bogotá, Lima y São Paulo subraya su rol como puntos de conexión hacia el resto del mundo, mientras que los vuelos directos a Europa (Madrid, París) actúan como puentes estratégicos para el comercio y el turismo de alto valor.

<div class="methodology-box" style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-light); border-radius: 8px; border-left: 4px solid var(--secondary);">
    <p style="margin: 0; font-size: 0.95rem;">📌 <strong>Sobre este proyecto:</strong> Esta es la versión rediseñada como aplicación interactiva. Los notebooks originales desarrollados durante la fase exploratoria están disponibles en Google Colab:
    <a href="https://colab.research.google.com/drive/1cOEHEMJTM6fkYkYqst9__5AVDlQaO9e2" target="_blank" style="color: var(--secondary); font-weight: 600;">Análisis de Atractivos y Destinos</a> y
    <a href="https://colab.research.google.com/drive/1woxG5EvWJUKDoNDW8hDxYpKaxP5So1RE" target="_blank" style="color: var(--secondary); font-weight: 600;">Flujo Aéreo Nacional</a>.</p>
</div>
