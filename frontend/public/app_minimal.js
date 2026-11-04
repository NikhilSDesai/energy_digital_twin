// Mapbox Access Token
if (typeof CONFIG !== 'undefined' && CONFIG.mapboxToken) {
    mapboxgl.accessToken = CONFIG.mapboxToken;
} else {
    console.error('Mapbox token not found');
}

// Initialize map - very minimal style
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11',
    center: [-2.5, 54.5],
    zoom: 5.8,
    pitch: 0,
    bearing: 0
});

// Add minimal controls
map.addControl(new mapboxgl.NavigationControl({
    showCompass: false
}), 'top-right');

// Layer visibility state
const layerState = {
    'gsp-boundaries': true,
    'projects': false,
    'transmission': false
};

// Load data
map.on('load', async function() {
    try {
        // Load GSP Boundaries
        const gspResponse = await fetch('../../data/raw/infrastructure/gsp_boundaries_20261103.geojson');
        const gspData = await gspResponse.json();

        // Add GSP boundaries - very subtle
        map.addSource('gsp-boundaries', {
            type: 'geojson',
            data: gspData
        });

        map.addLayer({
            id: 'gsp-fill',
            type: 'fill',
            source: 'gsp-boundaries',
            paint: {
                'fill-color': '#667eea',
                'fill-opacity': 0.03
            }
        });

        map.addLayer({
            id: 'gsp-outline',
            type: 'line',
            source: 'gsp-boundaries',
            paint: {
                'line-color': '#667eea',
                'line-width': 0.5,
                'line-opacity': 0.2
            }
        });

        // Hover effects
        let hoveredGSP = null;

        map.on('mousemove', 'gsp-fill', (e) => {
            if (e.features.length > 0) {
                if (hoveredGSP !== null) {
                    map.setFeatureState(
                        { source: 'gsp-boundaries', id: hoveredGSP },
                        { hover: false }
                    );
                }
                hoveredGSP = e.features[0].id;
                map.setFeatureState(
                    { source: 'gsp-boundaries', id: hoveredGSP },
                    { hover: true }
                );
                map.getCanvas().style.cursor = 'pointer';
            }
        });

        map.on('mouseleave', 'gsp-fill', () => {
            if (hoveredGSP !== null) {
                map.setFeatureState(
                    { source: 'gsp-boundaries', id: hoveredGSP },
                    { hover: false }
                );
            }
            hoveredGSP = null;
            map.getCanvas().style.cursor = '';
        });

        // Click to show info
        map.on('click', 'gsp-fill', (e) => {
            const props = e.features[0].properties;

            new mapboxgl.Popup({
                closeButton: true,
                closeOnClick: true
            })
            .setLngLat(e.lngLat)
            .setHTML(`
                <div class="popup-title">Grid Supply Point</div>
                <div class="popup-row">
                    <div class="popup-label">Region</div>
                    <div class="popup-value">${props.RegionName || 'Unknown'}</div>
                </div>
                <div class="popup-row">
                    <div class="popup-label">ID</div>
                    <div class="popup-value">${props.RegionID || 'N/A'}</div>
                </div>
            `)
            .addTo(map);
        });

        // Hide loading
        document.getElementById('loading').classList.add('hidden');

        console.log('✓ Map loaded');
        console.log('✓ GSP Regions:', gspData.features.length);

    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('loading').innerHTML = `
            <div style="color: #e15554; font-size: 14px;">Error loading data</div>
            <div style="font-size: 11px; margin-top: 8px; color: #666;">
                ${error.message}
            </div>
        `;
    }
});

// Layer toggles
document.querySelectorAll('.layer-toggle').forEach(toggle => {
    toggle.addEventListener('click', function() {
        const layer = this.getAttribute('data-layer');

        if (layer) {
            this.classList.toggle('active');

            // Toggle layer visibility
            const isActive = this.classList.contains('active');
            layerState[layer] = isActive;

            // Update map layers
            if (map.getLayer(`${layer}-fill`)) {
                map.setLayoutProperty(
                    `${layer}-fill`,
                    'visibility',
                    isActive ? 'visible' : 'none'
                );
            }
            if (map.getLayer(`${layer}-outline`)) {
                map.setLayoutProperty(
                    `${layer}-outline`,
                    'visibility',
                    isActive ? 'visible' : 'none'
                );
            }
        }
    });
});

// Search functionality (placeholder)
document.getElementById('searchBox').addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase();
    console.log('Search:', query);
    // TODO: Implement search filtering
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close popups
        const popups = document.getElementsByClassName('mapboxgl-popup');
        if (popups.length) {
            popups[0].remove();
        }
    }

    if (e.key === 'r' || e.key === 'R') {
        // Reset view
        map.flyTo({
            center: [-2.5, 54.5],
            zoom: 5.8,
            pitch: 0,
            bearing: 0
        });
    }
});

console.log('UK Energy Grid - Minimal Interface');
console.log('Press R to reset view, ESC to close popups');
