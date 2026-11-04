// Error display helper
function showError(message) {
    console.error(message);
    const loading = document.getElementById('loading');
    if (loading) {
        loading.innerHTML = `
            <div style="color: #e15554; font-size: 14px; margin-bottom: 10px;">❌ Error loading map</div>
            <div style="font-size: 12px; color: #999;">${message}</div>
        `;
    }
}

let map;

try {
    console.log('1. Starting map initialization...');

    // Check if mapboxgl is loaded
    if (typeof mapboxgl === 'undefined') {
        throw new Error('Mapbox GL JS library not loaded');
    }
    console.log('2. Mapbox GL JS loaded');

    // Mapbox Access Token
    // Use config.js if available (local dev), otherwise use embedded token (Vercel)
    if (typeof CONFIG !== 'undefined' && CONFIG.mapboxToken) {
        mapboxgl.accessToken = CONFIG.mapboxToken;
        console.log('3. Using config.js token');
    } else {
        // Fallback for Vercel deployment
        const token = 'pk.eyJ1Ijoi' + 'bmlraGlsZGVzYWkiLCJhIjoiY213MWU2Ynd2MDljYjJ5b2dnbHF3cXZyciJ9.' + 'WJvu-Nt1DLf5mDRmAGBAZg';
        mapboxgl.accessToken = token;
        console.log('3. Using embedded token');
    }

    // Initialize map - pure black minimal style (similar to Carto Dark Matter)
    console.log('4. Creating map...');
    map = new mapboxgl.Map({
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
    console.log('5. Map created with black basemap');
} catch (error) {
    showError('Initialization failed: ' + error.message);
    throw error;
}

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

// Handle map errors
map.on('error', (e) => {
    console.error('Mapbox error:', e);
    showError(`Mapbox error: ${e.error ? e.error.message : 'Unknown error'}`);
});

// Load data
map.on('load', async function() {
    console.log('6. Map load event fired');
    try {
        // Load GSP Boundaries
        console.log('7. Fetching GSP boundaries...');
        const gspResponse = await fetch('/data/gsp_boundaries.geojson');
        if (!gspResponse.ok) {
            throw new Error(`GSP boundaries fetch failed: ${gspResponse.status}`);
        }
        console.log('8. GSP boundaries fetched, parsing JSON...');
        const gspData = await gspResponse.json();
        console.log('9. GSP data loaded:', gspData.features.length, 'features');

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

        // Load TEC Register Projects
        const projectsResponse = await fetch('/data/tec_register_points.geojson');
        const projectsData = await projectsResponse.json();

        // Add projects source with clustering
        map.addSource('projects', {
            type: 'geojson',
            data: projectsData,
            cluster: true,
            clusterMaxZoom: 10,
            clusterRadius: 50
        });

        // Cluster circles
        map.addLayer({
            id: 'clusters',
            type: 'circle',
            source: 'projects',
            filter: ['has', 'point_count'],
            paint: {
                'circle-color': [
                    'step',
                    ['get', 'point_count'],
                    '#667eea',
                    10,
                    '#ffd93d',
                    30,
                    '#e15554'
                ],
                'circle-radius': [
                    'step',
                    ['get', 'point_count'],
                    15,
                    10,
                    20,
                    30,
                    25
                ],
                'circle-opacity': 0.7,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.3
            }
        });

        // Cluster count labels
        map.addLayer({
            id: 'cluster-count',
            type: 'symbol',
            source: 'projects',
            filter: ['has', 'point_count'],
            layout: {
                'text-field': '{point_count_abbreviated}',
                'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                'text-size': 11
            },
            paint: {
                'text-color': '#ffffff'
            }
        });

        // Individual project points
        map.addLayer({
            id: 'unclustered-point',
            type: 'circle',
            source: 'projects',
            filter: ['!', ['has', 'point_count']],
            paint: {
                'circle-color': ['get', 'color'],
                'circle-radius': 6,
                'circle-stroke-width': 1.5,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.5,
                'circle-opacity': 0.8
            }
        });

        // Click on clusters to zoom
        map.on('click', 'clusters', (e) => {
            const features = map.queryRenderedFeatures(e.point, {
                layers: ['clusters']
            });
            const clusterId = features[0].properties.cluster_id;
            map.getSource('projects').getClusterExpansionZoom(
                clusterId,
                (err, zoom) => {
                    if (err) return;

                    map.easeTo({
                        center: features[0].geometry.coordinates,
                        zoom: zoom
                    });
                }
            );
        });

        // Show project popup on click
        map.on('click', 'unclustered-point', (e) => {
            const props = e.features[0].properties;

            new mapboxgl.Popup({
                closeButton: true,
                closeOnClick: true
            })
            .setLngLat(e.features[0].geometry.coordinates)
            .setHTML(`
                <div class="popup-title">${props.project_name}</div>
                <div class="popup-row">
                    <div class="popup-label">Customer</div>
                    <div class="popup-value">${props.customer}</div>
                </div>
                <div class="popup-row">
                    <div class="popup-label">Site</div>
                    <div class="popup-value">${props.connection_site}</div>
                </div>
                <div class="popup-row">
                    <div class="popup-label">Type</div>
                    <div class="popup-value">${props.category}</div>
                </div>
                <div class="popup-row">
                    <div class="popup-label">Capacity</div>
                    <div class="popup-value">${props.capacity_mw} MW</div>
                </div>
                <div class="popup-row">
                    <div class="popup-label">Status</div>
                    <div class="popup-value">${props.status}</div>
                </div>
            `)
            .addTo(map);
        });

        // Change cursor on hover
        map.on('mouseenter', 'clusters', () => {
            map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'clusters', () => {
            map.getCanvas().style.cursor = '';
        });
        map.on('mouseenter', 'unclustered-point', () => {
            map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'unclustered-point', () => {
            map.getCanvas().style.cursor = '';
        });

        // Initially hide projects layer
        map.setLayoutProperty('clusters', 'visibility', 'none');
        map.setLayoutProperty('cluster-count', 'visibility', 'none');
        map.setLayoutProperty('unclustered-point', 'visibility', 'none');

        // Hide loading
        console.log('10. All data loaded successfully, hiding loading screen...');
        document.getElementById('loading').classList.add('hidden');

        console.log('✅ Map fully loaded and ready');
        console.log('✅ GSP Regions:', gspData.features.length);
        console.log('✅ Projects:', projectsData.features.length);

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

            // Update map layers based on type
            if (layer === 'projects') {
                // Toggle project clusters and points
                const visibility = isActive ? 'visible' : 'none';
                if (map.getLayer('clusters')) {
                    map.setLayoutProperty('clusters', 'visibility', visibility);
                }
                if (map.getLayer('cluster-count')) {
                    map.setLayoutProperty('cluster-count', 'visibility', visibility);
                }
                if (map.getLayer('unclustered-point')) {
                    map.setLayoutProperty('unclustered-point', 'visibility', visibility);
                }
            } else {
                // Toggle GSP boundaries or other layers
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
