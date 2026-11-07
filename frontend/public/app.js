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

// Hide loading screen and add data layers when map loads
map.on('load', async function() {
    try {
        // Load all data sources
        const [
            transmissionData,
            osmSubstationsData,
            gspData,
            tecData,
            distribution132Data,
            distribution66Data,
            distribution33Data,
            substationData,
            southWalesPrimaryData,
            spenBoundaryData,
            powerPlantsData
        ] = await Promise.all([
            fetch('/data/osm-transmission-lines-all.geojson').then(r => r.json()), // NEW: OSM data with 1,212 segments
            fetch('/data/osm-substations.geojson').then(r => r.json()), // NEW: OSM substations (395 sites)
            fetch('/data/gsp_boundaries.geojson').then(r => r.json()),
            fetch('/data/tec_register_points.geojson').then(r => r.json()),
            fetch('/data/ukpn-132kv-overhead-lines.geojson').then(r => r.json()),
            fetch('/data/ukpn-66kv-overhead-lines.geojson').then(r => r.json()),
            fetch('/data/ukpn-33kv-overhead-lines.geojson').then(r => r.json()),
            fetch('/data/grid-and-primary-sites.geojson').then(r => r.json()),
            fetch('/data/south_wales_primary.geojson').then(r => r.json()), // NGED South Wales primary substations (195 areas)
            fetch('/data/spen_boundary.geojson').then(r => r.json()), // SP Energy Networks license areas (SPD + SPM)
            fetch('/data/uk-power-plants.geojson').then(r => r.json()) // UK power plants: 2,587 sites (wind, solar, gas, etc)
        ]);

        // Add GSP boundaries (subtle background layer)
        map.addSource('gsp', {
            type: 'geojson',
            data: gspData
        });

        map.addLayer({
            id: 'gsp-fill',
            type: 'fill',
            source: 'gsp',
            paint: {
                'fill-color': '#3b82f6',
                'fill-opacity': 0.08
            }
        });

        map.addLayer({
            id: 'gsp-outline',
            type: 'line',
            source: 'gsp',
            paint: {
                'line-color': '#3b82f6',
                'line-width': 1,
                'line-opacity': 0.3
            }
        });

        console.log('✅ GSP boundaries loaded:', gspData.features.length);

        // Add South Wales Primary Substation Areas (NGED data)
        map.addSource('south-wales-primary', {
            type: 'geojson',
            data: southWalesPrimaryData
        });

        map.addLayer({
            id: 'south-wales-primary-fill',
            type: 'fill',
            source: 'south-wales-primary',
            minzoom: 8,
            paint: {
                'fill-color': '#10b981',
                'fill-opacity': 0.12
            }
        });

        map.addLayer({
            id: 'south-wales-primary-outline',
            type: 'line',
            source: 'south-wales-primary',
            minzoom: 8,
            paint: {
                'line-color': '#10b981',
                'line-width': 1.5,
                'line-opacity': 0.5
            }
        });

        console.log('✅ South Wales primary substations loaded:', southWalesPrimaryData.features.length, 'service areas');

        // Add SPEN License Area Boundaries
        map.addSource('spen-boundary', {
            type: 'geojson',
            data: spenBoundaryData
        });

        map.addLayer({
            id: 'spen-boundary-fill',
            type: 'fill',
            source: 'spen-boundary',
            minzoom: 5,
            paint: {
                'fill-color': '#8b5cf6',
                'fill-opacity': 0.08
            }
        });

        map.addLayer({
            id: 'spen-boundary-outline',
            type: 'line',
            source: 'spen-boundary',
            minzoom: 5,
            paint: {
                'line-color': '#8b5cf6',
                'line-width': 2,
                'line-opacity': 0.4
            }
        });

        console.log('✅ SPEN license areas loaded:', spenBoundaryData.features.length, 'regions (SPD + SPM)');

        // Add OSM transmission lines (400kV, 275kV, 220kV, DC)
        map.addSource('transmission', {
            type: 'geojson',
            data: transmissionData
        });

        map.addLayer({
            id: 'transmission-lines',
            type: 'line',
            source: 'transmission',
            paint: {
                'line-color': [
                    'match',
                    ['get', 'voltage_kv'],
                    400, '#FFD700',  // Bright gold for 400kV
                    275, '#FFA500',  // Orange for 275kV
                    220, '#FF6347',  // Tomato red for 220kV offshore
                    '#9370DB'        // Purple for DC links
                ],
                'line-width': [
                    'interpolate', ['linear'], ['zoom'],
                    5, [
                        'match',
                        ['get', 'voltage_kv'],
                        400, 2.5,
                        275, 2,
                        220, 1.5,
                        1.5
                    ],
                    10, [
                        'match',
                        ['get', 'voltage_kv'],
                        400, 5,
                        275, 4,
                        220, 3,
                        3
                    ],
                    14, [
                        'match',
                        ['get', 'voltage_kv'],
                        400, 7,
                        275, 5.5,
                        220, 4,
                        4
                    ]
                ],
                'line-opacity': 0.85
            }
        });

        console.log('✅ OSM Transmission lines loaded:', transmissionData.features.length, 'segments (400kV, 275kV, 220kV, DC)');

        // Add 132kV distribution lines
        map.addSource('distribution-132kv', {
            type: 'geojson',
            data: distribution132Data
        });

        map.addLayer({
            id: 'distribution-132kv-lines',
            type: 'line',
            source: 'distribution-132kv',
            minzoom: 8,
            maxzoom: 24,
            paint: {
                'line-color': '#d4af37',
                'line-width': [
                    'interpolate', ['linear'], ['zoom'],
                    8, 1.5,
                    11, 2.5,
                    14, 4
                ],
                'line-opacity': 0.7
            }
        });

        // Add 66kV distribution lines
        map.addSource('distribution-66kv', {
            type: 'geojson',
            data: distribution66Data
        });

        map.addLayer({
            id: 'distribution-66kv-lines',
            type: 'line',
            source: 'distribution-66kv',
            minzoom: 11,
            maxzoom: 24,
            paint: {
                'line-color': '#e6c968',
                'line-width': [
                    'interpolate', ['linear'], ['zoom'],
                    11, 1,
                    14, 2.5
                ],
                'line-opacity': 0.6
            }
        });

        // Add 33kV distribution lines
        map.addSource('distribution-33kv', {
            type: 'geojson',
            data: distribution33Data
        });

        map.addLayer({
            id: 'distribution-33kv-lines',
            type: 'line',
            source: 'distribution-33kv',
            minzoom: 11.5,
            maxzoom: 24,
            paint: {
                'line-color': '#f5e6a8',
                'line-width': [
                    'interpolate', ['linear'], ['zoom'],
                    11.5, 0.8,
                    14, 2
                ],
                'line-opacity': 0.5
            }
        });

        // Add connection queue points with clustering
        map.addSource('tec', {
            type: 'geojson',
            data: tecData,
            cluster: true,
            clusterMaxZoom: 10,
            clusterRadius: 50
        });

        // Clustered circles
        map.addLayer({
            id: 'tec-clusters',
            type: 'circle',
            source: 'tec',
            filter: ['has', 'point_count'],
            paint: {
                'circle-color': [
                    'step',
                    ['get', 'point_count'],
                    '#51bbd6', 10,
                    '#f1f075', 50,
                    '#f28cb1', 100,
                    '#e15554'
                ],
                'circle-radius': [
                    'step',
                    ['get', 'point_count'],
                    15, 10,
                    20, 50,
                    25, 100,
                    30
                ],
                'circle-opacity': 0.8,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.6
            }
        });

        // Cluster count labels
        map.addLayer({
            id: 'tec-cluster-count',
            type: 'symbol',
            source: 'tec',
            filter: ['has', 'point_count'],
            layout: {
                'text-field': '{point_count_abbreviated}',
                'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                'text-size': 12
            },
            paint: {
                'text-color': '#ffffff'
            }
        });

        // Individual unclustered points
        map.addLayer({
            id: 'tec-points',
            type: 'circle',
            source: 'tec',
            filter: ['!', ['has', 'point_count']],
            paint: {
                'circle-color': [
                    'match',
                    ['get', 'category'],
                    'Storage', '#667eea',
                    'Solar', '#f6ad55',
                    'Wind', '#48bb78',
                    'Other', '#cbd5e0',
                    '#cbd5e0'
                ],
                'circle-radius': 6,
                'circle-opacity': 0.7,
                'circle-stroke-width': 1,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.8
            }
        });

        console.log('✅ Connection queue loaded:', tecData.features.length);

        // Add UK power plants with clustering
        map.addSource('power-plants', {
            type: 'geojson',
            data: powerPlantsData,
            cluster: true,
            clusterMaxZoom: 9,
            clusterRadius: 40
        });

        // Power plant clusters
        map.addLayer({
            id: 'power-plants-clusters',
            type: 'circle',
            source: 'power-plants',
            filter: ['has', 'point_count'],
            minzoom: 5,
            paint: {
                'circle-color': [
                    'step',
                    ['get', 'point_count'],
                    '#22c55e', 10,
                    '#eab308', 50,
                    '#f97316', 100,
                    '#ef4444'
                ],
                'circle-radius': [
                    'step',
                    ['get', 'point_count'],
                    12, 10,
                    16, 50,
                    20, 100,
                    25
                ],
                'circle-opacity': 0.75,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.5
            }
        });

        // Power plant cluster count labels
        map.addLayer({
            id: 'power-plants-cluster-count',
            type: 'symbol',
            source: 'power-plants',
            filter: ['has', 'point_count'],
            minzoom: 5,
            layout: {
                'text-field': '{point_count_abbreviated}',
                'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                'text-size': 11
            },
            paint: {
                'text-color': '#ffffff'
            }
        });

        // Individual power plants
        map.addLayer({
            id: 'power-plants-points',
            type: 'circle',
            source: 'power-plants',
            filter: ['!', ['has', 'point_count']],
            minzoom: 9,
            paint: {
                'circle-color': [
                    'match',
                    ['get', 'plant_type'],
                    'wind', '#22c55e',
                    'offshore_wind', '#06b6d4',
                    'so', '#facc15',
                    'gas', '#f97316',
                    'bio', '#84cc16',
                    'hy', '#3b82f6',
                    'bat', '#a855f7',
                    '#94a3b8'
                ],
                'circle-radius': [
                    'interpolate', ['linear'], ['get', 'capacity_mw'],
                    0, 3,
                    50, 5,
                    500, 8,
                    2000, 12
                ],
                'circle-opacity': 0.75,
                'circle-stroke-width': 1,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.8
            }
        });

        console.log('✅ Power plants loaded:', powerPlantsData.features.length, 'generation sites');

        // Add substations with clustering
        map.addSource('substations', {
            type: 'geojson',
            data: substationData,
            cluster: true,
            clusterMaxZoom: 13,
            clusterRadius: 50
        });

        // Substations clustered circles
        map.addLayer({
            id: 'substations-clusters',
            type: 'circle',
            source: 'substations',
            filter: ['has', 'point_count'],
            minzoom: 8,
            maxzoom: 24,
            paint: {
                'circle-color': [
                    'step',
                    ['get', 'point_count'],
                    '#d4af37', 10,
                    '#e6c968', 50,
                    '#f5e6a8', 100,
                    '#a4b0be'
                ],
                'circle-radius': [
                    'step',
                    ['get', 'point_count'],
                    12, 10,
                    16, 50,
                    20, 100,
                    25
                ],
                'circle-opacity': 0.7,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.5
            }
        });

        // Substations cluster count labels
        map.addLayer({
            id: 'substations-cluster-count',
            type: 'symbol',
            source: 'substations',
            filter: ['has', 'point_count'],
            minzoom: 8,
            maxzoom: 24,
            layout: {
                'text-field': '{point_count_abbreviated}',
                'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                'text-size': 11
            },
            paint: {
                'text-color': '#ffffff'
            }
        });

        // Individual substations
        map.addLayer({
            id: 'substations-points',
            type: 'circle',
            source: 'substations',
            filter: ['!', ['has', 'point_count']],
            minzoom: 8,
            maxzoom: 24,
            paint: {
                'circle-color': [
                    'match',
                    ['get', 'sitevoltage'],
                    132, '#d4af37',
                    66, '#e6c968',
                    33, '#f5e6a8',
                    '#a4b0be'
                ],
                'circle-radius': [
                    'match',
                    ['get', 'sitevoltage'],
                    132, 8,
                    66, 6,
                    33, 5,
                    4
                ],
                'circle-opacity': [
                    'match',
                    ['get', 'sitevoltage'],
                    132, 0.8,
                    66, 0.7,
                    33, 0.6,
                    0.5
                ],
                'circle-stroke-width': 1.5,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.6
            }
        });
        // Add OSM transmission substations (395 major sites)
        map.addSource('osm-substations', {
            type: 'geojson',
            data: osmSubstationsData
        });

        map.addLayer({
            id: 'osm-substations',
            type: 'circle',
            source: 'osm-substations',
            minzoom: 6,
            maxzoom: 24,
            paint: {
                'circle-color': '#4CAF50',
                'circle-radius': [
                    'interpolate', ['linear'], ['zoom'],
                    6, 3,
                    10, 5,
                    14, 8
                ],
                'circle-opacity': 0.7,
                'circle-stroke-width': 1.5,
                'circle-stroke-color': '#fff',
                'circle-stroke-opacity': 0.8
            }
        });

        console.log('✅ OSM Substations loaded:', osmSubstationsData.features.length, 'major transmission sites');
        console.log('✅ 132kV distribution loaded:', distribution132Data.features.length);
        console.log('✅ 66kV distribution loaded:', distribution66Data.features.length);
        console.log('✅ 33kV distribution loaded:', distribution33Data.features.length);
        console.log('✅ UKPN Substations loaded:', substationData.features.length);
        console.log('Total features:',
            transmissionData.features.length +
            osmSubstationsData.features.length +
            gspData.features.length +
            tecData.features.length +
            distribution132Data.features.length +
            distribution66Data.features.length +
            distribution33Data.features.length +
            substationData.features.length +
            southWalesPrimaryData.features.length +
            spenBoundaryData.features.length +
            powerPlantsData.features.length
        );

    } catch (error) {
        console.error('Error loading data:', error);
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

// Add interactivity - popups on click
map.on('click', 'gsp-fill', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #1a1a1a; font-size: 13px;">
                <strong>${props.RegionName}</strong><br>
                <span style="color: #666; font-size: 11px;">GSP Region ${props.RegionID}</span>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'south-wales-primary-fill', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #1a1a1a; font-size: 13px;">
                <strong>Primary Substation ${props.PRIM_NR}</strong><br>
                <span style="color: #666; font-size: 11px;">ESA: ${props.ESA}</span><br>
                <span style="color: #666; font-size: 11px;">BSP: ${props.BSP_NRID_NAME}</span><br>
                <span style="color: #666; font-size: 11px;">GSP: ${props.GSP_NRID_NAME}</span><br>
                <span style="color: #10b981; font-size: 11px; font-weight: 500;">NGED - ${props.licence_area}</span>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'spen-boundary-fill', (e) => {
    const props = e.features[0].properties;
    const areaName = props.license_area === 'SPD' ? 'SP Distribution (Central & South Scotland)' : 'SP Manweb (Merseyside, Cheshire, North Wales)';
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #1a1a1a; font-size: 13px;">
                <strong>${areaName}</strong><br>
                <span style="color: #666; font-size: 11px;">License Area: ${props.license_area}</span><br>
                <span style="color: #8b5cf6; font-size: 11px; font-weight: 500;">SP Energy Networks</span>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'tec-clusters', (e) => {
    const features = map.queryRenderedFeatures(e.point, {
        layers: ['tec-clusters']
    });
    const clusterId = features[0].properties.cluster_id;
    map.getSource('tec').getClusterExpansionZoom(clusterId, (err, zoom) => {
        if (err) return;
        map.easeTo({
            center: features[0].geometry.coordinates,
            zoom: zoom
        });
    });
});

map.on('click', 'tec-points', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #1a1a1a; font-size: 12px; max-width: 250px;">
                <strong>${props.project_name}</strong><br>
                <span style="color: #666;">${props.plant_type}</span><br>
                ${props.capacity_mw > 0 ? `<span style="color: #333;">${props.capacity_mw} MW</span><br>` : ''}
                <span style="font-size: 11px; color: #888;">${props.connection_site}</span><br>
                <span style="font-size: 11px; color: #888;">Status: ${props.status}</span>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'power-plants-clusters', (e) => {
    const features = map.queryRenderedFeatures(e.point, {
        layers: ['power-plants-clusters']
    });
    const clusterId = features[0].properties.cluster_id;
    map.getSource('power-plants').getClusterExpansionZoom(clusterId, (err, zoom) => {
        if (err) return;
        map.easeTo({
            center: features[0].geometry.coordinates,
            zoom: zoom
        });
    });
});

map.on('click', 'power-plants-points', (e) => {
    const props = e.features[0].properties;
    const plantTypeNames = {
        'wind': 'Wind Farm',
        'offshore_wind': 'Offshore Wind',
        'so': 'Solar',
        'gas': 'Natural Gas',
        'bio': 'Biomass',
        'hy': 'Hydro',
        'bat': 'Battery Storage',
        'ti': 'Tidal'
    };
    const plantTypeName = plantTypeNames[props.plant_type] || props.plant_type;
    const plantColor = props.plant_type === 'wind' ? '#22c55e' : props.plant_type === 'offshore_wind' ? '#06b6d4' : props.plant_type === 'so' ? '#facc15' : props.plant_type === 'gas' ? '#f97316' : '#94a3b8';

    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #1a1a1a; font-size: 12px; max-width: 250px;">
                <strong>${props.name}</strong><br>
                <span style="color: ${plantColor}; font-weight: 500;">${plantTypeName}</span><br>
                ${props.capacity_mw > 0 ? `<span style="color: #333; font-weight: 600;">${props.capacity_mw} MW</span><br>` : ''}
                ${props.operator ? `<span style="font-size: 11px; color: #888;">${props.operator}</span><br>` : ''}
                <span style="font-size: 10px; color: #aaa;">OSM: ${props.osm_id}</span>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'transmission-lines', (e) => {
    const props = e.features[0].properties;
    const voltage = props.voltage_kv || props.voltage || 'Unknown';
    const voltageColor = voltage == 400 ? '#FFD700' : voltage == 275 ? '#FFA500' : voltage == 220 ? '#FF6347' : '#9370DB';

    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 200px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: ${voltageColor};">
                    ${voltage}kV Transmission Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Voltage</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${voltage}kV</span>
                </div>
                ${props.voltage === 'dc' || props.voltage === 'DC' || voltage > 300 && voltage < 350 ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Type</span>
                    <span style="color: #e0e0e0; font-weight: 500;">HVDC Interconnector</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    National Grid Transmission • OpenStreetMap Data
                </div>
            </div>
        `)
        .addTo(map);
});

// OSM Substations popup
map.on('click', 'osm-substations', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 250px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #4CAF50;">
                    ${props.name || 'Transmission Substation'}
                </div>
                ${props.capacity_mw ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Capacity</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.capacity_mw} MW</span>
                </div>
                ` : ''}
                ${props.operator ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Operator</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.operator}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    Transmission Network • OpenStreetMap Data
                </div>
            </div>
        `)
        .addTo(map);
});

// Distribution line popups
map.on('click', 'distribution-132kv-lines', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 200px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #d4af37;">
                    132kV Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Voltage</span>
                    <span style="color: #e0e0e0; font-weight: 500;">132kV</span>
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.dno === 'SPN' ? 'South East (SPN)' : props.dno === 'EPN' ? 'East England (EPN)' : 'London (LPN)'}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Power Networks Distribution
                </div>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'distribution-66kv-lines', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 200px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #e6c968;">
                    66kV Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Voltage</span>
                    <span style="color: #e0e0e0; font-weight: 500;">66kV</span>
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.dno === 'SPN' ? 'South East (SPN)' : props.dno === 'EPN' ? 'East England (EPN)' : 'London (LPN)'}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Power Networks Distribution
                </div>
            </div>
        `)
        .addTo(map);
});

map.on('click', 'distribution-33kv-lines', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 200px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #f5e6a8;">
                    33kV Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Voltage</span>
                    <span style="color: #e0e0e0; font-weight: 500;">33kV</span>
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.dno === 'SPN' ? 'South East (SPN)' : props.dno === 'EPN' ? 'East England (EPN)' : 'London (LPN)'}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Power Networks Distribution
                </div>
            </div>
        `)
        .addTo(map);
});

// Substation popups
map.on('click', 'substations-clusters', (e) => {
    const features = map.queryRenderedFeatures(e.point, {
        layers: ['substations-clusters']
    });
    const clusterId = features[0].properties.cluster_id;
    map.getSource('substations').getClusterExpansionZoom(clusterId, (err, zoom) => {
        if (err) return;
        map.easeTo({
            center: features[0].geometry.coordinates,
            zoom: zoom
        });
    });
});

map.on('click', 'substations-points', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 250px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #d4af37;">
                    ${props.sitename}
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Type</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.sitetype}</span>
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Voltage</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.sitevoltage}kV</span>
                </div>
                ${props.maxdemandwinter ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Max Demand</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.maxdemandwinter} MW</span>
                </div>
                ` : ''}
                ${props.siteclassification ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Classification</span>
                    <span style="color: ${props.siteclassification === 'HOT' ? '#e15554' : '#48dbfb'}; font-weight: 500;">${props.siteclassification}</span>
                </div>
                ` : ''}
                ${props.towncity ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 100px;">Location</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.towncity}${props.county ? ', ' + props.county : ''}</span>
                </div>
                ` : ''}
                ${props.licencearea ? `
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    ${props.licencearea}
                </div>
                ` : ''}
            </div>
        `)
        .addTo(map);
});

// Change cursor on hover
map.on('mouseenter', 'gsp-fill', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'gsp-fill', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'south-wales-primary-fill', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'south-wales-primary-fill', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'spen-boundary-fill', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'spen-boundary-fill', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'tec-clusters', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'tec-clusters', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'tec-points', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'tec-points', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'power-plants-clusters', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'power-plants-clusters', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'power-plants-points', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'power-plants-points', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'transmission-lines', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'transmission-lines', () => { map.getCanvas().style.cursor = ''; });
map.on('mouseenter', 'osm-substations', () => { map.getCanvas().style.cursor = 'pointer'; });
map.on('mouseleave', 'osm-substations', () => { map.getCanvas().style.cursor = ''; });

// Distribution lines hover
['distribution-132kv-lines', 'distribution-66kv-lines', 'distribution-33kv-lines'].forEach(layerId => {
    map.on('mouseenter', layerId, () => { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', layerId, () => { map.getCanvas().style.cursor = ''; });
});

// Substations hover
['substations-clusters', 'substations-points'].forEach(layerId => {
    map.on('mouseenter', layerId, () => { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', layerId, () => { map.getCanvas().style.cursor = ''; });
});

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
