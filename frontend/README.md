# UK Energy Digital Twin - Frontend

Modern web-based visualization of UK energy infrastructure using MapLibre GL JS with purple/blue-purple (BuPu) color scheme.

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (Python, Node.js, or PHP)
- MapTiler API key (free tier: 100,000 loads/month)

### Setup

1. **Get a MapTiler API Key** (Optional - already configured)
   - Go to https://www.maptiler.com/cloud/
   - Sign up for free account
   - Copy your API key
   - Create `frontend/public/config.js`:
   ```javascript
   window.MAPTILER_KEY = 'YOUR_API_KEY_HERE';
   ```

2. **Run a Local Server**
   ```bash
   # Navigate to public directory
   cd frontend/public

   # Option 1: Python (recommended)
   python3 -m http.server 8001

   # Option 2: Node.js
   npx serve

   # Option 3: PHP
   php -S localhost:8001
   ```

3. **Open in Browser**
   ```
   http://localhost:8001
   ```

## 🎨 Visual Design

### Color Scheme

**Primary Colors:**
- **Electric Blue (#00D9FF)**: All transmission and distribution lines
- **Purple (#9D4EDD)**: Substations, GSP boundaries
- **White (#FFFFFF)**: Transmission constraint boundaries

**BuPu Gradient (ColorBrewer-inspired):**
```
#BFD3E6 → #9ECAE1 → #8C96C6 → #8C6BB1 → #88419D
(Very Light Blue → Light Blue → Blue-Purple → Purple → Dark Purple)
```

**Applied to:**
- Power plant clusters (by density)
- Connection queue clusters
- Individual power plants (by technology)

### UI Components

**Left Sidebar (320px)**
- 7 collapsible categories
- Layer checkboxes with counts
- Clean dark theme (rgba(0, 0, 0, 0.95))
- Smooth expand/collapse animations

**Top Bar (60px)**
- Project title
- Real-time statistics
- Minimal design

**Interactive Popups**
- Blue gradient background (dark #1e3a8a → light #3b82f6)
- White dotted border (3px, semi-transparent)
- Rounded corners (24px border-radius)
- Center-aligned title
- Structured data rows

**Map Controls**
- Navigation controls (top-right)
- Dark themed
- Keyboard shortcut: R to reset view

## 📊 Data Layers

### Layer Categories

**1. Transmission (Electric Blue)**
```
✓ 400kV Lines (1,212 segments)
✓ 275kV Lines
✓ 220kV Lines
✓ DC Interconnectors
  Transmission Substations (395 sites)
  Constraint Boundaries (34 NESO boundaries)
```

**2. Distribution (Electric Blue)**
```
✓ 132kV Lines
✓ 66kV Lines
✓ 33kV Lines
```

**3. Operational Generation (Purple/BuPu)**
```
  All Power Plants (2,587 sites, 64.4 GW)
  - Clustered visualization
  - Technology-based colors
  - Capacity-based sizing
```

**4. Connection Queue (Purple)**
```
  TEC Register (2,219 projects)
  - Status indicators
  - Technology categories
  - Capacity information
```

**5. Substations (Purple)**
```
  UKPN Substations
  - Clustered by zoom level
  - Detailed information popups
```

**6. Network Regions (Purple)**
```
  GSP Boundaries (329 regions)
  South Wales Primary (195 areas)
  SPEN License Areas (2 regions)
```

**7. Buildings (Grey)**
```
  UK Building Footprints (29.5M)
  - Vector tiles (35GB)
  - Zoom 17-20
  - Served via tileserver-gl-light
```

### Layer Visibility

**Default Visible:**
- All transmission lines (400kV, 275kV, 220kV, DC)
- All distribution lines (132kV, 66kV, 33kV)

**Default Hidden:**
- Substations
- Power plants
- Connection queue
- Boundaries
- Buildings

**Zoom-Based Visibility:**
- Transmission: Always visible
- Distribution 132kV: zoom ≥ 8
- Distribution 66kV: zoom ≥ 11
- Distribution 33kV: zoom ≥ 11.5
- Buildings: zoom ≥ 17

## 🛠️ Technical Details

### Map Configuration

**MapLibre GL JS v3.6.2**
- Open-source fork of Mapbox GL JS
- Compatible with any vector tile provider
- No licensing restrictions

**MapTiler Backdrop Dark**
- Clean terrain visualization
- No labels or borders
- Dark mode optimized
- Free tier: 100,000 loads/month

**Initial View:**
```javascript
{
  center: [-2.5, 54.5],  // UK center
  zoom: 5.8,
  pitch: 0,
  bearing: 0
}
```

### Line Styling

**Transmission Lines (Electric Blue)**
```javascript
{
  'line-color': '#00D9FF',
  'line-width': [
    'interpolate', ['linear'], ['zoom'],
    5, [voltage-based: 1-2px],
    10, [voltage-based: 2-3px],
    14, [voltage-based: 2.5-4px]
  ],
  'line-opacity': 0.9,
  'line-blur': [2px at z5, 2.5px at z10, 3px at z14]
}
```

**Distribution Lines (Electric Blue)**
- Similar styling with smaller widths
- Voltage-based thickness hierarchy
- Zoom-dependent blur for glow effect

**Transmission Boundaries (White)**
```javascript
{
  'line-color': '#FFFFFF',
  'line-width': [2px-4px],
  'line-opacity': 0.6,
  'line-dasharray': [3, 2],  // Dashed pattern
  'line-blur': 1
}
```

### Circle Styling (Purple/BuPu)

**Power Plant Clusters**
```javascript
{
  'circle-color': [
    'step', ['get', 'point_count'],
    '#BFD3E6', 10,    // Very light blue
    '#9ECAE1', 50,    // Light blue
    '#8C96C6', 100,   // Blue-purple
    '#88419D'         // Dark purple
  ]
}
```

**Substations**
```javascript
{
  'circle-color': '#9D4EDD',  // Purple
  'circle-radius': [3-8px based on zoom],
  'circle-opacity': 0.7
}
```

## 🎮 Features

### Interactive Controls

**Sidebar Functionality**
- Click category header to expand/collapse
- Click layer item to toggle visibility
- Real-time layer count display
- Smooth animations

**Transmission Line Filtering**
- Independent control of each voltage level
- Filter-based implementation (not just visibility)
- Maintains performance with complex filtering

**Map Interactions**
- Click on any feature for detailed popup
- Hover for cursor change feedback
- Scroll to zoom
- Drag to pan
- Pinch to zoom (mobile)

**Keyboard Shortcuts**
- `R` - Reset view to UK center (zoom 5.8)

### Popup System

**Customized Popups**
```javascript
new maplibregl.Popup({
  className: 'custom-popup'
})
```

**Popup Styling**
- Blue gradient background
- Dotted white border
- Rounded corners (24px)
- White text on dark background
- Structured data rows
- Centered title

**Popup Content**
- Feature name/title
- Key attributes (voltage, capacity, type, etc.)
- Location information
- Status indicators
- Operator details

## 📁 File Structure

```
frontend/
├── public/
│   ├── index.html           # UI structure, styling, sidebar
│   ├── app.js               # Map logic, layers, interactions
│   ├── config.js            # API keys (gitignored)
│   └── data/                # GeoJSON datasets
│       ├── osm-transmission-lines-all.geojson
│       ├── osm-substations.geojson
│       ├── gsp_boundaries.geojson
│       ├── tec_register_points.geojson
│       ├── ukpn-132kv-overhead-lines.geojson
│       ├── ukpn-66kv-overhead-lines.geojson
│       ├── ukpn-33kv-overhead-lines.geojson
│       ├── grid-and-primary-sites.geojson
│       ├── south_wales_primary.geojson
│       ├── spen_boundary.geojson
│       ├── uk-power-plants.geojson
│       └── transmission_boundaries.geojson
└── README.md                # This file
```

## 🎨 Customization

### Change Base Map Style

Currently using MapTiler Backdrop Dark:
```javascript
style: 'https://api.maptiler.com/maps/backdrop-dark/style.json?key=' + maptilerKey
```

**Alternatives:**
```javascript
// MapTiler Basic
'https://api.maptiler.com/maps/basic/style.json?key=' + maptilerKey

// MapTiler Streets
'https://api.maptiler.com/maps/streets/style.json?key=' + maptilerKey

// MapTiler Satellite
'https://api.maptiler.com/maps/satellite/style.json?key=' + maptilerKey
```

### Adjust Colors

**Change Transmission Color:**
```javascript
// In app.js, find transmission-lines layer
'line-color': '#00D9FF',  // Change to your color
```

**Modify Purple Tones:**
```javascript
// Substations
'circle-color': '#9D4EDD',  // Adjust purple shade

// GSP boundaries
'fill-color': '#9D4EDD',
```

**Customize BuPu Gradient:**
```javascript
// Power plant clusters
'circle-color': [
  'step', ['get', 'point_count'],
  '#YOUR_COLOR_1', 10,
  '#YOUR_COLOR_2', 50,
  '#YOUR_COLOR_3', 100,
  '#YOUR_COLOR_4'
]
```

### Modify Line Widths

```javascript
'line-width': [
  'interpolate', ['linear'], ['zoom'],
  5, 1.5,  // Width at zoom 5
  10, 2.5, // Width at zoom 10
  14, 3.5  // Width at zoom 14
]
```

## 🔧 Troubleshooting

### Map Not Loading

**Symptoms:** Black screen or "Error loading map"

**Solutions:**
1. Check MapTiler API key is set in `config.js`
2. Verify you're using a local server (not opening HTML directly)
3. Check browser console for errors
4. Ensure data files exist in `data/` folder
5. Try clearing browser cache

### Data Layers Not Showing

**Symptoms:** Layers toggle but nothing appears

**Solutions:**
1. Check layer is toggled ON in sidebar
2. Verify you're at correct zoom level
3. Check file paths in `app.js` match actual data files
4. Inspect browser console for 404 errors
5. Verify GeoJSON files are valid

### CORS Errors

**Symptoms:** "Access-Control-Allow-Origin" errors

**Solutions:**
- **Must use local server** - Cannot open HTML file directly
- Use Python: `python3 -m http.server 8001`
- Or Node.js: `npx serve`
- Or PHP: `php -S localhost:8001`

### Performance Issues

**Symptoms:** Slow rendering, lag when panning

**Solutions:**
1. Disable building layer (29.5M footprints)
2. Increase cluster radius for point data
3. Reduce line blur values
4. Simplify line geometries
5. Use Chrome for best performance

### Popup Not Styled

**Symptoms:** Plain white popups instead of gradient

**Solutions:**
1. Verify `className: 'custom-popup'` is set
2. Check CSS in `index.html` includes `.custom-popup` styles
3. Clear browser cache
4. Inspect popup element for applied classes

## 📊 Performance Metrics

**Current Performance (Desktop, Chrome):**
- Initial load: ~2-3 seconds
- Memory usage: ~150MB
- FPS: 60 (smooth panning/zooming)
- Total features rendered: 5,584+

**Data Layer Performance:**
- Transmission lines: Instant
- Distribution lines: Instant
- Power plants (clustered): ~100ms
- Buildings (vector tiles): ~500ms per tile
- GSP boundaries: Instant

**Optimization Techniques:**
- Clustering for dense point data (>1000 points)
- Vector tiles for building footprints
- Zoom-based layer visibility
- Filter-based layer control (not remove/add)
- GeoJSON simplification where appropriate

## 🚀 Deployment

### Vercel Deployment

**Automatic:**
- Push to main branch → auto-deploy
- Live at: https://uk-energy-digital-twin.vercel.app

**Manual:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Production deployment
vercel --prod
```

### Static Hosting

Works on any static host:
- **Netlify**: Drag & drop `frontend/public` folder
- **GitHub Pages**: Push to gh-pages branch
- **AWS S3**: Upload and enable static hosting
- **Cloudflare Pages**: Connect repository

### Building Tiles Server

**For Buildings Layer:**
```bash
# Install tileserver-gl-light
npm install -g tileserver-gl-light

# Serve tiles
tileserver-gl-light data/processed/buildings_optimized/uk_buildings.mbtiles

# Access at localhost:8080
```

## 📚 Additional Resources

- **MapLibre GL JS Docs**: https://maplibre.org/maplibre-gl-js-docs/api/
- **MapTiler Docs**: https://docs.maptiler.com/
- **GeoJSON Spec**: https://geojson.org/
- **ColorBrewer**: https://colorbrewer2.org/
- **Tippecanoe**: https://github.com/felt/tippecanoe

## 🤝 Contributing to Frontend

### Adding New Layers

1. **Add data file** to `frontend/public/data/`
2. **Load data** in `app.js`:
   ```javascript
   fetch('/data/your-data.geojson').then(r => r.json())
   ```
3. **Add source and layer**:
   ```javascript
   map.addSource('your-layer', { type: 'geojson', data: yourData });
   map.addLayer({ id: 'your-layer', ... });
   ```
4. **Add to sidebar** in `index.html`
5. **Add to layer mapping** in `app.js`
6. **Add popup handler** for interactivity

### Modifying Existing Layers

1. Find layer in `app.js` (search for layer ID)
2. Modify `paint` or `layout` properties
3. Test locally
4. Commit and push

### UI Improvements

1. Modify HTML structure in `index.html`
2. Update CSS styles in `<style>` tag
3. Adjust JavaScript interactions in `app.js`
4. Test responsiveness

## 📝 Code Style

- **Indentation**: 4 spaces
- **Comments**: Explain why, not what
- **Naming**: Descriptive, camelCase for JS
- **Layer IDs**: kebab-case (e.g., `transmission-lines`)
- **Colors**: Hex codes with comments

## 🏆 Version History

- **v0.3.0** (2026-11-11) - Purple/BuPu color scheme, MapLibre migration
- **v0.2.0** (2026-11-08) - Sidebar, building tiles, aesthetic overhaul
- **v0.1.0** (2026-11-03) - Initial MVP with basic visualization

---

**Version:** 0.3.0
**Last Updated:** November 11, 2026
**Built with:** MapLibre GL JS + MapTiler + Claude Code
