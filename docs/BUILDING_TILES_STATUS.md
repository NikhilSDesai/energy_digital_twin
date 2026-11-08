# Building Tiles Processing Status
**Started**: 2024-11-07
**Status**: ⏳ In Progress

---

## 📊 Processing Details

### Input
- **File**: `data/processed/uk_buildings_overture.geojson`
- **Size**: 18 GB
- **Features**: 29,500,000 building footprints
- **Coverage**: Complete UK
- **Source**: Overture Maps Foundation

### Output
- **File**: `data/processed/buildings_optimized/uk_buildings.mbtiles`
- **Format**: MBTiles (vector tiles)
- **Zoom levels**: 17-22 (street level to maximum detail)
- **Tile format**: MVT (Mapbox Vector Tiles)

### Processing Command
```bash
tippecanoe \
  -o buildings_optimized/uk_buildings.mbtiles \
  -Z 17                          # Minimum zoom (start showing buildings)
  -z 22                          # Maximum zoom (highest detail)
  --drop-densest-as-needed       # Remove dense buildings at lower zooms
  --extend-zooms-if-still-dropping \
  --simplification=10            # Simplify geometries
  --buffer=5                     # Tile buffer
  -l buildings                   # Layer name
  --maximum-tile-bytes=500000    # 500 KB max per tile
  --maximum-tile-features=200000 # 200K features max per tile
  --force                        # Overwrite if exists
  --progress-interval=30         # Progress updates every 30s
  uk_buildings_overture.geojson
```

---

## ⏱️ Expected Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Read features | 15-20 min | ⏳ In progress |
| Create tiles Z17 | 10-15 min | ⏳ Pending |
| Create tiles Z18 | 15-20 min | ⏳ Pending |
| Create tiles Z19 | 20-25 min | ⏳ Pending |
| Create tiles Z20 | 15-20 min | ⏳ Pending |
| Create tiles Z21 | 10-15 min | ⏳ Pending |
| Create tiles Z22 | 5-10 min | ⏳ Pending |
| **TOTAL** | **1-2 hours** | ⏳ **In progress** |

---

## 📈 Progress Monitoring

### Monitor in Terminal
```bash
# Watch progress in real-time
tail -f /private/tmp/claude-501/-Users-nikhildesai-Documents-03-Personal-energy-dt/tasks/b247227.output

# Or use the monitoring script
./monitor_building_tiles.sh
```

### Check Output Size
```bash
# Check if file is being created
ls -lh data/processed/buildings_optimized/uk_buildings.mbtiles

# Watch file size grow
watch -n 30 'ls -lh data/processed/buildings_optimized/uk_buildings.mbtiles'
```

### Expected Output Size
- **Estimated**: 800 MB - 2 GB (compressed vector tiles)
- **Compression ratio**: ~90% (from 18 GB to ~1-2 GB)

---

## 🎯 After Completion

### 1. Verify Output
```bash
# Check file size
ls -lh data/processed/buildings_optimized/uk_buildings.mbtiles

# Inspect tiles with mbutil (if installed)
mb-util --show data/processed/buildings_optimized/uk_buildings.mbtiles

# Or use tippecanoe-decode
tippecanoe-decode data/processed/buildings_optimized/uk_buildings.mbtiles 17 65536 40960
```

### 2. Serve Tiles Locally (Testing)
```bash
# Option 1: Using tileserver-gl (recommended)
npm install -g tileserver-gl
tileserver-gl data/processed/buildings_optimized/uk_buildings.mbtiles

# Option 2: Using Python HTTP server with mbview
npm install -g mbview
mbview data/processed/buildings_optimized/uk_buildings.mbtiles
```

### 3. Deploy to Production

#### Option A: Self-Hosted Tile Server
1. Copy tiles to server:
   ```bash
   scp data/processed/buildings_optimized/uk_buildings.mbtiles user@server:/var/tiles/
   ```

2. Set up tileserver-gl on server
3. Update frontend to use tile server URL

#### Option B: Mapbox Upload (Free Tier: 750,000 tile requests/month)
1. Convert to Mapbox-compatible format
2. Upload via Mapbox Studio or CLI
3. Get tileset ID
4. Update frontend with Mapbox tiles

#### Option C: Cloud Storage + PMTiles
1. Convert MBTiles to PMTiles:
   ```bash
   npm install -g pmtiles
   pmtiles convert uk_buildings.mbtiles uk_buildings.pmtiles
   ```

2. Upload to cloud storage (S3, GCS, Cloudflare R2)
3. Serve via PMTiles protocol (range requests)
4. Update frontend to use PMTiles URL

### 4. Integrate into Frontend

Update `frontend/public/app.js`:

```javascript
// Add building tiles source
map.addSource('buildings', {
    type: 'vector',
    url: 'https://your-tile-server.com/tiles.json' // Or use tiles: ['url/{z}/{x}/{y}.pbf']
    // OR for PMTiles:
    // url: 'pmtiles://https://storage.com/uk_buildings.pmtiles'
});

// Add building fill layer
map.addLayer({
    id: 'buildings-fill',
    type: 'fill',
    source: 'buildings',
    'source-layer': 'buildings',
    minzoom: 17,
    maxzoom: 24,
    paint: {
        'fill-color': '#888',
        'fill-opacity': 0.5
    }
});

// Add building outline layer
map.addLayer({
    id: 'buildings-outline',
    type: 'line',
    source: 'buildings',
    'source-layer': 'buildings',
    minzoom: 18,
    maxzoom: 24,
    paint: {
        'line-color': '#555',
        'line-width': 1,
        'line-opacity': 0.8
    }
});
```

---

## 🔧 Troubleshooting

### If Process Fails

**Out of Memory Error**:
- Current system needs ~20 GB RAM
- Try reducing zoom range: `-z 20` instead of `-z 22`
- Or process in smaller geographic chunks using `--bbox`

**File Too Large Error**:
- Increase `--maximum-tile-bytes` to 1000000 (1 MB)
- Increase `--maximum-tile-features` to 500000
- Or use more aggressive `--simplification=20`

**Process Killed/Stopped**:
- Check available disk space (need ~5 GB free)
- Check RAM usage: `top` or `htop`
- Restart with `--continue` flag if tippecanoe supports it

### Manual Restart
```bash
cd data/processed
tippecanoe \
  -o buildings_optimized/uk_buildings.mbtiles \
  -Z 17 -z 22 \
  --drop-densest-as-needed \
  --extend-zooms-if-still-dropping \
  --simplification=10 \
  --buffer=5 \
  -l buildings \
  --maximum-tile-bytes=500000 \
  --maximum-tile-features=200000 \
  --force \
  --progress-interval=30 \
  uk_buildings_overture.geojson
```

---

## 📚 Background Information

### Why Vector Tiles?

**Problem**: 18 GB GeoJSON is impossible to load in browser

**Solution**: Vector tiles provide:
- ✅ Progressive loading (only visible tiles)
- ✅ Client-side rendering (styleable)
- ✅ 90% compression (18 GB → 1-2 GB)
- ✅ Fast rendering (GPU accelerated)
- ✅ Zoom-appropriate detail (simplified at lower zooms)

### Tippecanoe Features Used

- **`--drop-densest-as-needed`**: Removes dense clusters of buildings at lower zoom levels to keep tile sizes manageable
- **`--extend-zooms-if-still-dropping`**: If buildings are still being dropped at max zoom, extends one more level
- **`--simplification=10`**: Removes vertices from building polygons while maintaining shape (10 = moderate)
- **`--maximum-tile-bytes=500KB`**: Ensures each tile is ≤500 KB for fast loading
- **`--maximum-tile-features=200K`**: Limits features per tile to prevent browser slowdown

### Zoom Level Strategy

| Zoom | Coverage | Use Case | Buildings Shown |
|------|----------|----------|-----------------|
| 17 | ~4 km² | Neighborhood view | Major buildings only |
| 18 | ~1 km² | Street view | Most buildings |
| 19 | ~250 m² | Block view | All buildings |
| 20 | ~60 m² | Building view | Full detail |
| 21 | ~15 m² | Individual building | Maximum detail |
| 22 | ~4 m² | Building detail | Highest precision |

---

## 🎯 Success Criteria

After processing completes, verify:
- ✅ Output file exists: `uk_buildings.mbtiles`
- ✅ File size: 800 MB - 2 GB
- ✅ Contains zoom levels 17-22
- ✅ Layer name is "buildings"
- ✅ Can be opened by tile viewer
- ✅ Buildings appear at zoom 17+
- ✅ Detail increases with zoom

---

## 📊 UK Building Coverage

Once deployed, the digital twin will show:
- **29.5 million** building footprints
- **Complete UK** coverage
- **Street-level** detail (zoom 17+)
- **Individual buildings** (zoom 19+)
- **Building outlines** at highest zoom

### Building Data Attribution
- Source: Overture Maps Foundation
- License: ODbL (Open Database License)
- Must attribute: "Building data © Overture Maps Foundation"

---

**Status**: Processing started, estimated completion in 1-2 hours
**Next**: Monitor progress, then deploy tiles to production
