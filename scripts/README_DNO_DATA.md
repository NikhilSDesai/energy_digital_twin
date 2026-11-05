
# UK DNO Distribution Network Data - Complete Implementation Guide

This guide walks you through downloading, processing, and integrating distribution network data from all 6 UK DNOs to achieve **100% Great Britain coverage**.

## 📋 Overview

**Current Status**: 25% coverage (UKPN only)
**Target**: 100% coverage (all 6 DNOs)
**Data Types**: 132kV, 66kV, 33kV overhead lines + substations
**Expected Data Size**: ~25 MB raw, ~8-10 MB gzipped

---

## 🎯 DNO Coverage Map

| DNO | Coverage | Customers | Status |
|-----|----------|-----------|--------|
| **UKPN** | London, SE England, East | 8.4M | ✅ Complete |
| **NGED** | Midlands, SW England, Wales | 7.9M | 🟡 Manual download |
| **NPG** | NE England, Yorkshire | 3.9M | 🟡 Manual download |
| **SSEN** | N Scotland, S England | 3.9M | 🟡 Manual download |
| **SPEN** | Scotland, NW England, N Wales | 3.5M | 🟡 Manual download |
| **ENWL** | NW England (Manchester, Lancs) | 2.4M | 🟡 Manual download |
| **TOTAL** | **Great Britain** | **30M** | **Target: 100%** |

---

## 🚀 Quick Start (4-Step Process)

### Prerequisites

```bash
# Install required Python packages
pip install geopandas shapely requests tqdm
```

### Step 1: Download DNO Data

```bash
# Automated download for UKPN + manual instructions for others
python scripts/download_all_dno_network_data.py
```

**What this does:**
- ✅ Automatically downloads UKPN data (no registration needed)
- 📋 Displays manual download instructions for NGED, NPG, SSEN, SPEN, ENWL
- 📝 Creates download checklist at `data/dno/DOWNLOAD_CHECKLIST.md`

**Follow the instructions to download from:**
1. **NGED** (Priority #1 - 7.9M customers)
   - Portal: https://connecteddata.nationalgrid.co.uk/
   - Download: 132kV, 66kV, 33kV overhead lines + substations
   - Save to: `data/dno/nged/raw/`

2. **NPG, SSEN, SPEN, ENWL** (Follow instructions in terminal output)

### Step 2: Convert Shapefiles to GeoJSON

```bash
# Convert all downloaded shapefiles to GeoJSON
python scripts/convert_dno_shapefiles.py
```

**What this does:**
- Extracts shapefiles from ZIP archives
- Reprojects to WGS84 (EPSG:4326) for web mapping
- Adds DNO identifier to each feature
- Saves GeoJSON files to `frontend/public/data/`
- Generates conversion report

### Step 3: Standardize Property Schemas

```bash
# Standardize property names across all DNOs
python scripts/standardize_dno_properties.py
```

**What this does:**
- Creates consistent property names (`voltage`, `dno`, `local_authority`, etc.)
- Preserves original DNO-specific properties
- Ensures uniform data structure for visualization

### Step 4: Combine All DNO Data

```bash
# Combine individual DNO files into unified datasets
python scripts/combine_dno_data.py
```

**What this does:**
- Combines all 132kV files → `all-dnos-132kv-overhead-lines.geojson`
- Combines all 66kV files → `all-dnos-66kv-overhead-lines.geojson`
- Combines all 33kV files → `all-dnos-33kv-overhead-lines.geojson`
- Combines all substations → `all-dnos-substations.geojson`

---

## 🎨 Update Frontend

### Update app.js

Replace the data loading section in `frontend/public/app.js` with the code from:

```
scripts/app_js_updated_code.js
```

Key changes:
- Load combined files instead of UKPN-only files
- Add DNO-specific popup information
- Display coverage statistics in console

### Update index.html

Update the bottom info panel in `frontend/public/index.html`:

```html
<div class="bottom-info">
    Data: NESO TEC Register • National Grid ESO Transmission • UK Distribution Networks (All 6 DNOs)<br>
    <span style="font-size: 10px; color: #555;">
        Updated Nov 2026 • Zoom in to see distribution network •
        Coverage: UKPN, NGED, NPG, SSEN, SPEN, ENWL
    </span>
</div>
```

---

## 📊 Expected Results

After completing all steps:

### Feature Counts

| Voltage | Estimated Features | Size |
|---------|-------------------|------|
| 132kV lines | ~3,000-5,000 | ~3 MB |
| 66kV lines | ~200-500 | ~200 KB |
| 33kV lines | ~25,000-35,000 | ~15 MB |
| Substations | ~8,000-12,000 | ~6 MB |
| **Total** | **~40,000** | **~25 MB raw** |

### Coverage Statistics

- **Geographic**: 100% of Great Britain
- **Population**: 30M customers covered
- **Data Sources**: 6 official DNO portals
- **Accuracy**: All data from verified DNO sources

---

## 🗂️ File Structure

```
energy_dt/
├── scripts/
│   ├── download_all_dno_network_data.py    # Step 1: Download
│   ├── convert_dno_shapefiles.py           # Step 2: Convert
│   ├── standardize_dno_properties.py       # Step 3: Standardize
│   ├── combine_dno_data.py                 # Step 4: Combine
│   ├── app_js_updated_code.js              # Frontend code
│   └── README_DNO_DATA.md                  # This file
│
├── data/dno/
│   ├── ukpn/raw/                           # UKPN shapefiles
│   ├── nged/raw/                           # NGED shapefiles
│   ├── npg/raw/                            # Northern Powergrid
│   ├── ssen/raw/                           # SSE Energy Networks
│   ├── spen/raw/                           # Scottish Power
│   ├── enwl/raw/                           # Electricity North West
│   ├── DOWNLOAD_CHECKLIST.md               # Track progress
│   └── conversion_report.json              # Conversion stats
│
└── frontend/public/data/
    ├── all-dnos-132kv-overhead-lines.geojson  # Combined 132kV
    ├── all-dnos-66kv-overhead-lines.geojson   # Combined 66kV
    ├── all-dnos-33kv-overhead-lines.geojson   # Combined 33kV
    ├── all-dnos-substations.geojson           # Combined substations
    └── combination_report.json                # Combination stats
```

---

## 🔍 Troubleshooting

### Issue: "No .shp file found in ZIP"

**Solution:** Some DNOs provide data in different formats. Check the ZIP contents and adjust the script or convert manually using QGIS/ogr2ogr.

### Issue: "CRS not found or invalid"

**Solution:** Most UK data uses British National Grid (EPSG:27700). The script handles this automatically.

### Issue: "Download requires authentication"

**Solution:** Some DNO portals require registration. Create a free account and download manually.

### Issue: "Combined file too large (>50MB)"

**Solution:** Consider:
- Simplifying geometries using `mapshaper` or QGIS
- Splitting by region
- Using vector tiles instead of GeoJSON

---

## 📈 Performance Optimization

### If Combined Files Are Too Large:

#### Option 1: Simplify Geometries

```bash
# Install mapshaper
npm install -g mapshaper

# Simplify to 10% of original points
mapshaper all-dnos-33kv-overhead-lines.geojson \
  -simplify 10% \
  -o all-dnos-33kv-overhead-lines-simplified.geojson
```

#### Option 2: Use Vector Tiles

Convert GeoJSON to vector tiles (.mbtiles) using `tippecanoe`:

```bash
# Install tippecanoe
brew install tippecanoe  # macOS

# Convert to vector tiles
tippecanoe -o distribution.mbtiles \
  -Z 8 -z 14 \
  --drop-densest-as-needed \
  all-dnos-*.geojson
```

#### Option 3: Split by Region

Keep individual DNO files and load based on map bounds.

---

## ✅ Verification Checklist

After implementation:

- [ ] All 4 scripts run without errors
- [ ] Combined files exist in `frontend/public/data/`
- [ ] `combination_report.json` shows expected feature counts
- [ ] Frontend loads without errors
- [ ] Zoom to different regions shows distribution networks
- [ ] Click handlers work for all DNOs
- [ ] Console shows DNO coverage breakdown
- [ ] Performance acceptable (60 FPS pan/zoom)

---

## 🎯 Next Steps

### After Complete UK Coverage:

1. **Add Real-Time Data**
   - Integrate NESO API for live generation/demand
   - Show current grid status

2. **Add Network Capacity**
   - Download headroom datasets from DNO portals
   - Visualize available capacity

3. **Add Future Scenarios**
   - Use FES (Future Energy Scenarios) data
   - Show planned infrastructure upgrades

4. **Interactive Filtering**
   - Filter by DNO
   - Filter by voltage
   - Toggle layers on/off

---

## 📚 Resources

### DNO Data Portals

- **UKPN**: https://ukpowernetworks.opendatasoft.com/
- **NGED**: https://connecteddata.nationalgrid.co.uk/
- **NPG**: https://northernpowergrid.opendatasoft.com/
- **SSEN**: https://data.ssen.co.uk/
- **SPEN**: https://spenergynetworks.opendatasoft.com/
- **ENWL**: https://electricitynorthwest.opendatasoft.com/

### Data Aggregators

- **Open Net Zero**: https://opennetzero.org/
- **NESO Data Portal**: https://data.nationalgrideso.com/

### Tools

- **GeoPandas**: https://geopandas.org/
- **Mapshaper**: https://mapshaper.org/
- **Tippecanoe**: https://github.com/felt/tippecanoe
- **QGIS**: https://qgis.org/

---

## 💡 Pro Tips

1. **Start with NGED** - Biggest impact (7.9M customers)
2. **Test incrementally** - Add one DNO at a time
3. **Monitor file sizes** - Use browser dev tools network tab
4. **Use CDN** - Consider uploading large files to CDN
5. **Enable gzip** - Vercel does this automatically
6. **Cache aggressively** - Distribution network changes slowly

---

## 🏆 Success Criteria

You'll know you're successful when:

✅ National view shows transmission network only (clean)
✅ Zoom to London shows UKPN distribution
✅ Zoom to Birmingham shows NGED distribution
✅ Zoom to Manchester shows ENWL distribution
✅ Zoom to Edinburgh shows SPEN distribution
✅ Zoom to Newcastle shows NPG distribution
✅ All 6 DNOs represented in console log
✅ Popups show correct DNO names
✅ Performance remains smooth

**You now have the most comprehensive open-source UK distribution network visualization!** 🎉

---

## 🐛 Support

If you encounter issues:

1. Check `data/dno/conversion_report.json` for processing errors
2. Verify file sizes are reasonable (<50 MB per file)
3. Test with one DNO first before combining all
4. Open an issue with error messages and file sizes

---

**Last Updated**: November 2026
**Version**: 1.0
**Status**: Production Ready
