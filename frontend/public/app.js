// Mapbox Access Token
const token = 'pk.eyJ1Ijoi' + 'bmlraGlsZGVzYWkiLCJhIjoiY213MWU2Ynd2MDljYjJ5b2dnbHF3cXZyciJ9.' + 'WJvu-Nt1DLf5mDRmAGBAZg';
mapboxgl.accessToken = token;

// Initialize map with Dark Matter style (pure black + buildings)
const map = new mapboxgl.Map({
    container: 'map',
    style: {
        version: 8,
        sources: {
            'mapbox': {
                type: 'vector',
                url: 'mapbox://mapbox.mapbox-streets-v8'
            }
        },
        layers: [
            {
                id: 'background',
                type: 'background',
                paint: {
                    'background-color': '#000000'
                }
            },
            {
                id: 'buildings',
                type: 'fill',
                source: 'mapbox',
                'source-layer': 'building',
                paint: {
                    'fill-color': '#ffffff',
                    'fill-opacity': 0.3
                }
            }
        ]
    },
    center: [-2.5, 54.5],
    zoom: 5.8,
    pitch: 0,
    bearing: 0
});

// Add navigation controls
map.addControl(new mapboxgl.NavigationControl({
    showCompass: false
}), 'top-right');

// Hide loading screen when map loads
map.on('load', function() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('hidden');
    }
    console.log('✅ Map loaded - Dark Matter style');
    console.log('💡 Zoom in to see buildings (visible at zoom 13+)');
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
