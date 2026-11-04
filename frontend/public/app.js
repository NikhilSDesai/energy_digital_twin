// Mapbox Access Token from config
mapboxgl.accessToken = CONFIG.mapboxToken;

// Initialize map with dark theme
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11', // Dark theme
    center: [-2.5, 54.5], // Center on UK
    zoom: 5.5,
    pitch: 0,
    bearing: 0
});

// Add navigation controls
map.addControl(new mapboxgl.NavigationControl(), 'top-right');

// Add scale control
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 100,
    unit: 'metric'
}), 'bottom-left');

// Color scheme for plant types
const PLANT_TYPE_COLORS = {
    'Energy Storage System': '#667eea',
    'Energy Storage System;PV Array (Photo Voltaic/solar)': '#ffd93d',
    'Wind Onshore': '#6bcf7f',
    'Wind Offshore': '#4d9de0',
    'CCGT (Combined Cycle Gas Turbine)': '#e15554',
    'default': '#999999'
};

function getPlantTypeColor(plantType) {
    return PLANT_TYPE_COLORS[plantType] || PLANT_TYPE_COLORS['default'];
}

// Load and display data
map.on('load', async function() {
    try {
        // Load GSP Boundaries
        const gspResponse = await fetch('../../data/raw/infrastructure/gsp_boundaries_20261103.geojson');
        const gspData = await gspResponse.json();

        // Add GSP boundaries layer
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
                'fill-opacity': 0.05
            }
        });

        map.addLayer({
            id: 'gsp-outline',
            type: 'line',
            source: 'gsp-boundaries',
            paint: {
                'line-color': '#667eea',
                'line-width': 1,
                'line-opacity': 0.3
            }
        });

        // Add hover effect for GSP regions
        map.on('mouseenter', 'gsp-fill', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'gsp-fill', () => {
            map.getCanvas().style.cursor = '';
        });

        // Show GSP info on click
        map.on('click', 'gsp-fill', (e) => {
            const properties = e.features[0].properties;

            new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(`
                    <div class="popup-title">GSP Region</div>
                    <div class="popup-field">
                        <span class="popup-label">Region:</span>
                        <span class="popup-value">${properties.RegionName || 'Unknown'}</span>
                    </div>
                    <div class="popup-field">
                        <span class="popup-label">ID:</span>
                        <span class="popup-value">${properties.RegionID || 'N/A'}</span>
                    </div>
                `)
                .addTo(map);
        });

        // Update stats
        document.getElementById('gspRegions').textContent = gspData.features.length;

        // Try to load TEC Register stats
        await loadTECStats();

        // Hide loading screen
        document.getElementById('loading').classList.add('hidden');

        console.log('✓ Map loaded successfully');
        console.log(`✓ GSP Regions: ${gspData.features.length}`);

    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('loading').innerHTML = `
            <div style="color: #e15554;">Error loading data</div>
            <div style="font-size: 12px; margin-top: 10px; color: #999;">
                Check console for details
            </div>
        `;
    }
});

async function loadTECStats() {
    try {
        // For now, just set the stats we know from the data
        // In production, you'd fetch and parse the CSV
        document.getElementById('totalProjects').textContent = '2,219';
        document.getElementById('totalCapacity').textContent = '81.7';
        document.getElementById('connections').textContent = '1,259';
    } catch (error) {
        console.error('Error loading TEC stats:', error);
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'H' to toggle header
    if (e.key === 'h' || e.key === 'H') {
        const header = document.querySelector('.header');
        header.style.display = header.style.display === 'none' ? 'block' : 'none';
    }

    // Press 'L' to toggle legend
    if (e.key === 'l' || e.key === 'L') {
        const legend = document.querySelector('.legend');
        legend.style.display = legend.style.display === 'none' ? 'block' : 'none';
    }

    // Press 'R' to reset view
    if (e.key === 'r' || e.key === 'R') {
        map.flyTo({
            center: [-2.5, 54.5],
            zoom: 5.5,
            pitch: 0,
            bearing: 0
        });
    }
});

console.log('UK Energy Digital Twin - MVP v0.1');
console.log('Keyboard shortcuts:');
console.log('  H - Toggle header');
console.log('  L - Toggle legend');
console.log('  R - Reset view');
