const {DeckGL, ArcLayer} = deck;

let currentData = [];
let deckgl;
let currentMetric = 'pasajeros';
let currentPerspective = 'emisivo';
let currentScope = 'internacional';
let currentYear = null;

const tooltip = document.getElementById('tooltip');

const PERSPECTIVE_LABELS = {
    internacional: {first: 'Emisivo', firstValue: 'emisivo', second: 'Receptivo', secondValue: 'receptivo'},
    nacional: {first: 'Salidas', firstValue: 'salidas', second: 'Llegadas', secondValue: 'llegadas'},
};

const VIEW_STATES = {
    internacional: {longitude: -70.7, latitude: -33.4, zoom: 3, pitch: 45, bearing: 0},
    nacional: {longitude: -70.7, latitude: -36.0, zoom: 5, pitch: 45, bearing: 0},
};

function updatePerspectiveButtons() {
    const labels = PERSPECTIVE_LABELS[currentScope];
    const container = document.getElementById('perspective-toggle');
    container.innerHTML = `
        <button class="active" data-value="${labels.firstValue}">${labels.first}</button>
        <button data-value="${labels.secondValue}">${labels.second}</button>
    `;
    currentPerspective = labels.firstValue;
}

function updateSliderRange() {
    const years = [...new Set(currentData.map(d => d.year))].sort((a, b) => a - b);
    if (years.length === 0) return;

    const slider = document.getElementById('year-slider');
    slider.min = years[0];
    slider.max = years[years.length - 1];

    if (currentYear === null || currentYear > years[years.length - 1] || currentYear < years[0]) {
        currentYear = years[years.length - 1];
    }
    slider.value = currentYear;
    document.getElementById('year-label').textContent = currentYear;
}

async function loadData() {
    const prefix = currentScope === 'nacional' ? 'nacional_' : '';
    const filename = `${prefix}${currentPerspective}_${currentMetric}.json`;
    try {
        const response = await fetch(`assets/data/${filename}`);
        currentData = await response.json();
    } catch {
        currentData = [];
    }
    updateSliderRange();
    updateMap();
}

function getArcColors() {
    if (currentScope === 'nacional') {
        const isSalidas = currentPerspective === 'salidas';
        return {
            source: isSalidas ? [0, 200, 150] : [100, 50, 200],
            target: isSalidas ? [100, 50, 200] : [0, 200, 150],
        };
    }
    const isEmisivo = currentPerspective === 'emisivo';
    return {
        source: isEmisivo ? [0, 128, 255] : [255, 128, 0],
        target: isEmisivo ? [255, 128, 0] : [0, 128, 255],
    };
}

function updateMap() {
    const filteredData = currentData.filter(d => d.year === currentYear);

    document.getElementById('route-count').textContent = filteredData.length;
    const total = filteredData.reduce((acc, d) => acc + d.value, 0);
    const formatter = new Intl.NumberFormat('es-CL');
    document.getElementById('total-value').textContent = formatter.format(Math.round(total)) + (currentMetric === 'pasajeros' ? ' pax' : ' ton');

    const colors = getArcColors();

    const layer = new ArcLayer({
        id: 'arc-layer',
        data: filteredData,
        pickable: true,
        getWidth: d => Math.log10(d.value + 1) * 2,
        getSourcePosition: d => d.source,
        getTargetPosition: d => d.target,
        getSourceColor: colors.source,
        getTargetColor: colors.target,
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

    deckgl.setProps({layers: [layer]});
}

// Inicializar mapa
deckgl = new DeckGL({
    container: 'map',
    mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initialViewState: VIEW_STATES.internacional,
    controller: true
});

// Event Listeners
document.getElementById('scope-toggle').addEventListener('click', e => {
    if (e.target.tagName === 'BUTTON') {
        document.querySelectorAll('#scope-toggle button').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentScope = e.target.dataset.value;
        updatePerspectiveButtons();
        deckgl.setProps({initialViewState: {...VIEW_STATES[currentScope], transitionDuration: 1000}});
        loadData();
    }
});

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
