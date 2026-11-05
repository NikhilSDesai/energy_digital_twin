// ============================================================================
// UPDATED CODE FOR frontend/public/app.js
// Complete UK Distribution Network Coverage (All 6 DNOs)
// ============================================================================

// Replace the existing Promise.all() section (around line 35) with this:

const [
    transmissionData,
    gspData,
    tecData,
    // Combined distribution data (all DNOs)
    distribution132Data,
    distribution66Data,
    distribution33Data,
    substationData
] = await Promise.all([
    fetch('/data/transmission_lines.geojson').then(r => r.json()),
    fetch('/data/gsp_boundaries.geojson').then(r => r.json()),
    fetch('/data/tec_register_points.geojson').then(r => r.json()),
    // Use combined files for complete UK coverage
    fetch('/data/all-dnos-132kv-overhead-lines.geojson').then(r => r.json()),
    fetch('/data/all-dnos-66kv-overhead-lines.geojson').then(r => r.json()),
    fetch('/data/all-dnos-33kv-overhead-lines.geojson').then(r => r.json()),
    fetch('/data/all-dnos-substations.geojson').then(r => r.json())
]);

// Update console logging (after line 168):

console.log('✅ Transmission lines loaded:', transmissionData.features.length);
console.log('✅ GSP boundaries loaded:', gspData.features.length);
console.log('✅ Connection queue loaded:', tecData.features.length);
console.log('✅ 132kV distribution loaded:', distribution132Data.features.length);
console.log('✅ 66kV distribution loaded:', distribution66Data.features.length);
console.log('✅ 33kV distribution loaded:', distribution33Data.features.length);
console.log('✅ Substations loaded:', substationData.features.length);

// Log DNO coverage breakdown
const dno132Count = {};
distribution132Data.features.forEach(f => {
    const dno = f.properties.dno || 'Unknown';
    dno132Count[dno] = (dno132Count[dno] || 0) + 1;
});
console.log('📊 132kV Coverage by DNO:', dno132Count);

console.log('Total features:',
    transmissionData.features.length +
    gspData.features.length +
    tecData.features.length +
    distribution132Data.features.length +
    distribution66Data.features.length +
    distribution33Data.features.length +
    substationData.features.length
);

// ============================================================================
// UPDATED POPUP CODE - DNO-specific information
// ============================================================================

// Replace the existing distribution line click handlers with these enhanced versions:

// 132kV Distribution Lines Popup
map.on('click', 'distribution-132kv-lines', (e) => {
    const props = e.features[0].properties;
    const dnoNames = {
        'UKPN': 'UK Power Networks',
        'UKPN-LPN': 'UK Power Networks (London)',
        'UKPN-SPN': 'UK Power Networks (South East)',
        'UKPN-EPN': 'UK Power Networks (East)',
        'NGED': 'National Grid Electricity Distribution',
        'NPG': 'Northern Powergrid',
        'SSEN': 'SSE Energy Networks',
        'SPEN': 'Scottish Power Energy Networks',
        'SPEN-SPD': 'SP Distribution (Scotland)',
        'SPEN-SPM': 'SP Manweb (Wales/NW)',
        'ENWL': 'Electricity North West'
    };
    const dnoFull = dnoNames[props.dno] || props.dno;

    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 220px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #d4af37;">
                    ${props.voltage || '132kV'} Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${dnoFull}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                ${props.status ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Status</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.status}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Distribution Network
                </div>
            </div>
        `)
        .addTo(map);
});

// 66kV Distribution Lines Popup
map.on('click', 'distribution-66kv-lines', (e) => {
    const props = e.features[0].properties;
    const dnoNames = {
        'UKPN': 'UK Power Networks',
        'UKPN-LPN': 'UK Power Networks (London)',
        'UKPN-SPN': 'UK Power Networks (South East)',
        'UKPN-EPN': 'UK Power Networks (East)',
        'NGED': 'National Grid Electricity Distribution',
        'NPG': 'Northern Powergrid',
        'SSEN': 'SSE Energy Networks',
        'SPEN': 'Scottish Power Energy Networks',
        'SPEN-SPD': 'SP Distribution (Scotland)',
        'SPEN-SPM': 'SP Manweb (Wales/NW)',
        'ENWL': 'Electricity North West'
    };
    const dnoFull = dnoNames[props.dno] || props.dno;

    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 220px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #e6c968;">
                    ${props.voltage || '66kV'} Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${dnoFull}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                ${props.status ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Status</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.status}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Distribution Network
                </div>
            </div>
        `)
        .addTo(map);
});

// 33kV Distribution Lines Popup
map.on('click', 'distribution-33kv-lines', (e) => {
    const props = e.features[0].properties;
    const dnoNames = {
        'UKPN': 'UK Power Networks',
        'UKPN-LPN': 'UK Power Networks (London)',
        'UKPN-SPN': 'UK Power Networks (South East)',
        'UKPN-EPN': 'UK Power Networks (East)',
        'NGED': 'National Grid Electricity Distribution',
        'NPG': 'Northern Powergrid',
        'SSEN': 'SSE Energy Networks',
        'SPEN': 'Scottish Power Energy Networks',
        'SPEN-SPD': 'SP Distribution (Scotland)',
        'SPEN-SPM': 'SP Manweb (Wales/NW)',
        'ENWL': 'Electricity North West'
    };
    const dnoFull = dnoNames[props.dno] || props.dno;

    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`
            <div style="color: #fff; font-size: 13px; min-width: 220px;">
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #f5e6a8;">
                    ${props.voltage || '33kV'} Distribution Line
                </div>
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">DNO</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${dnoFull}</span>
                </div>
                ${props.local_authority ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Authority</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.local_authority}</span>
                </div>
                ` : ''}
                ${props.status ? `
                <div style="display: flex; margin-bottom: 4px;">
                    <span style="color: #666; min-width: 80px;">Status</span>
                    <span style="color: #e0e0e0; font-weight: 500;">${props.status}</span>
                </div>
                ` : ''}
                <div style="color: #999; font-size: 11px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    UK Distribution Network
                </div>
            </div>
        `)
        .addTo(map);
});

// ============================================================================
// UPDATED HTML INFO PANEL
// Update frontend/public/index.html bottom-info section:
// ============================================================================

/*
<div class="bottom-info">
    Data: NESO TEC Register • National Grid ESO Transmission • UK Distribution Networks (All 6 DNOs)<br>
    <span style="font-size: 10px; color: #555;">
        Updated Nov 2026 • Zoom in to see distribution network •
        Coverage: UKPN, NGED, NPG, SSEN, SPEN, ENWL
    </span>
</div>
*/

// ============================================================================
// That's it! Your visualization now covers 100% of Great Britain
// ============================================================================
