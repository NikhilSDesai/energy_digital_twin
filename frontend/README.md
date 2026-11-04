# UK Energy Digital Twin - Frontend

Mapbox-based dark theme visualization of UK energy infrastructure.

## Quick Start

1. **Get a Mapbox Token** (free tier: 50,000 loads/month)
   - Go to https://account.mapbox.com/
   - Sign up for free
   - Copy your default public token

2. **Add your token to `app.js`**
   ```javascript
   mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN_HERE';
   ```

3. **Run a local server**
   ```bash
   # Option 1: Python
   cd frontend/public
   python3 -m http.server 8000

   # Option 2: Node.js
   npx serve public

   # Option 3: PHP
   php -S localhost:8000
   ```

4. **Open in browser**
   ```
   http://localhost:8000
   ```

## Features

### Current (MVP v0.1)
- ✅ Dark Mapbox basemap
- ✅ GSP boundary visualization (329 regions)
- ✅ Interactive popups for GSP info
- ✅ Stats dashboard
- ✅ Keyboard shortcuts (H, L, R)

### Coming Soon
- [ ] Connection queue projects (TEC Register)
- [ ] Project filtering by technology
- [ ] Capacity heat maps
- [ ] Timeline slider
- [ ] 3D view (Deck.gl integration)

## Keyboard Shortcuts

- `H` - Toggle header
- `L` - Toggle legend
- `R` - Reset view to UK

## Data Layers

Currently visualizing:
- **GSP Boundaries** - 329 Grid Supply Point regions
- **Stats** - Connection queue metrics

## Tech Stack

- **Mapbox GL JS v3.0** - Dark theme mapping
- **Pure JS** - No framework (for simplicity)
- **GeoJSON** - Spatial data format

## Next Steps

To add connection queue projects:
1. Geocode connection sites (match to GSP regions or get coordinates)
2. Convert TEC Register CSV to GeoJSON
3. Add as point layer with clustering
4. Implement filters and search

## File Structure

```
frontend/
├── public/
│   ├── index.html    # Main HTML with Mapbox
│   ├── app.js        # Map initialization & data loading
│   └── (data files)  # Served from ../../data/raw/
└── README.md
```

## Customization

### Change Map Style
In `app.js`:
```javascript
style: 'mapbox://styles/mapbox/dark-v11'  // Current
// OR
style: 'mapbox://styles/mapbox/navigation-night-v1'
style: 'mapbox://styles/mapbox/satellite-streets-v12'
```

### Adjust Colors
Edit `PLANT_TYPE_COLORS` in `app.js`:
```javascript
const PLANT_TYPE_COLORS = {
    'Energy Storage System': '#667eea',  // Purple
    'Wind Onshore': '#6bcf7f',           // Green
    // Add more...
};
```

## Troubleshooting

**Map not loading?**
- Check Mapbox token is set
- Check browser console for errors
- Verify local server is running

**GSP boundaries not showing?**
- Check path to GeoJSON file
- Verify data file exists at `../../data/raw/infrastructure/`

**CORS errors?**
- Must use local server (can't open HTML directly)
- Use one of the server options above

## Performance

Current performance:
- **GSP Boundaries**: 329 polygons - instant load
- **Memory**: ~50MB
- **Render**: 60 FPS

When adding 2,219 TEC projects:
- Expected: ~100MB memory
- Recommend: Enable clustering for >1000 points

---

**Version:** 0.1.0 (MVP)
**Last Updated:** November 3, 2026
