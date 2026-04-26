const {DeckGL, ArcLayer} = deck;

let currentData = [];
let deckgl;
let currentMetric = 'pasajeros';
let currentPerspective = 'emisivo';
let currentYear = 2024;

const tooltip = document.getElementById('tooltip');

async function loadData() {
    const filename = `${currentPerspective}_${currentMetric}.json`;
    const response = await fetch(`assets/data/${filename}`);
    currentData = await response.json();
    updateMap();
}

function updateMap() {
    const filteredData = currentData.filter(d => d.year === currentYear);
    
    // Calcular estadísticas
    document.getElementById('route-count').textContent = filteredData.length;
    const total = filteredData.reduce((acc, d) => acc + d.value, 0);
    const formatter = new Intl.NumberFormat('es-CL');
    document.getElementById('total-value').textContent = formatter.format(Math.round(total)) + (currentMetric === 'pasajeros' ? ' pax' : ' ton');

    const layer = new ArcLayer({
        id: 'arc-layer',
        data: filteredData,
        pickable: true,
        getWidth: d => Math.log10(d.value + 1) * 2,
        getSourcePosition: d => d.source,
        getTargetPosition: d => d.target,
        getSourceColor: d => currentPerspective === 'emisivo' ? [0, 128, 255] : [255, 128, 0],
        getTargetColor: d => currentPerspective === 'emisivo' ? [255, 128, 0] : [0, 128, 255],
        onHover: info => {
            if (info.object) {
                tooltip.style.display = 'block';
                tooltip.style.left = `${info.x + 10}px`;
                tooltip.style.top = `${info.y + 10}px`;
                tooltip.innerHTML = `
                    <strong>${info.object.orig} ➔ ${info.object.dest}</strong><br>
                    ${formatter.format(Math.round(info.object.value))} ${currentMetric === 'pasajeros' ? 'pasajeros' : 'toneladas'}
                `;
            } else {
                tooltip.style.display = 'none';
            }
        }
    });

    deckgl.setProps({
        layers: [layer]
    });
}

// Inicializar mapa
deckgl = new DeckGL({
    container: 'map',
    mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initialViewState: {
        longitude: -70.7,
        latitude: -33.4,
        zoom: 3,
        pitch: 45,
        bearing: 0
    },
    controller: true
});

// Event Listeners
document.getElementById('metric-toggle').addEventListener('click', e => {
    if (e.target.tagName === 'BUTTON') {
        document.querySelectorAll('#metric-toggle button').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentMetric = e.target.dataset.value;
        loadData();
    }
});

document.getElementById('perspective-toggle').addEventListener('click', e => {
    if (e.target.tagName === 'BUTTON') {
        document.querySelectorAll('#perspective-toggle button').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentPerspective = e.target.dataset.value;
        loadData();
    }
});

const yearSlider = document.getElementById('year-slider');
const yearLabel = document.getElementById('year-label');

yearSlider.addEventListener('input', e => {
    currentYear = parseInt(e.target.value);
    yearLabel.textContent = currentYear;
    updateMap();
});

// Carga inicial
loadData();
