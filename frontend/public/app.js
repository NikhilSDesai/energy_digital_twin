// Mapbox Access Token
const token = 'pk.eyJ1Ijoi' + 'bmlraGlsZGVzYWkiLCJhIjoiY213MWU2Ynd2MDljYjJ5b2dnbHF3cXZyciJ9.' + 'WJvu-Nt1DLf5mDRmAGBAZg';
mapboxgl.accessToken = token;

// Initialize map with Mapbox dark style
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11',
    center: [-2.5, 54.5],
    zoom: 5.8,
    pitch: 0,
    bearing: 0
});

// Add navigation controls
map.addControl(new mapboxgl.NavigationControl({
    showCompass: false
}), 'top-right');

// Remove all labels when style loads
map.on('style.load', function() {
    const layers = map.getStyle().layers;
    // Remove all symbol layers (text labels)
    layers.forEach(layer => {
        if (layer.type === 'symbol') {
            map.removeLayer(layer.id);
        }
    });
});

// Hide loading screen and add transmission lines when map loads
map.on('load', async function() {
    try {
        // Load transmission lines
        const response = await fetch('/data/transmission_lines.geojson');
        const transmissionData = await response.json();

        // Add transmission lines source
        map.addSource('transmission', {
            type: 'geojson',
            data: transmissionData
        });

        // Add transmission lines layer - muted yellow
        map.addLayer({
            id: 'transmission-lines',
            type: 'line',
            source: 'transmission',
            paint: {
                'line-color': '#d4af37',  // Muted gold/yellow
                'line-width': 2,
                'line-opacity': 0.7
            }
        });

        console.log('✅ Transmission lines loaded:', transmissionData.features.length);

    } catch (error) {
        console.error('Error loading transmission lines:', error);
    }

    // Hide loading screen
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('hidden');
    }
    console.log('✅ Map loaded - UK Energy Grid');
});

// Error handling
map.on('error', function(e) {
    console.error('Map error:', e);
    const loading = document.getElementById('loading');
    if (loading) {
        loading.innerHTML = '<div style="color: #e15554;">Error loading map</div>';
    }
});

console.log('UK Energy Grid - Dark Matter Style');
console.log('Press R to reset view, use mouse/trackpad to navigate');

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'r' || e.key === 'R') {
        map.flyTo({
            center: [-2.5, 54.5],
            zoom: 5.8,
            pitch: 0,
            bearing: 0
        });
    }
});
