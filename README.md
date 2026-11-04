# UK Energy Grid Digital Twin

**🌐 LIVE:** https://uk-energy-digital-twin.vercel.app

A minimal dark-themed interactive visualization of the UK's energy transmission infrastructure.

---

## 📊 Current Status

**✅ DEPLOYED & WORKING:**
- Interactive web map with UK transmission grid
- Dark Mapbox background (labels removed for clean aesthetic)
- 14 major transmission corridors visualized in muted yellow/gold
- Real-time deployment via Vercel

**📍 What You See:**
- UK transmission network (400kV and 275kV lines)
- Scotland-England interconnectors
- Major power corridors connecting all regions
- Clean, minimal dark interface

---

## 🚀 Quick Links

- **Live Site:** https://uk-energy-digital-twin.vercel.app
- **GitHub:** https://github.com/NikhilSDesai/energy_digital_twin
- **Test Pages:**
  - Simple: https://uk-energy-digital-twin.vercel.app/test-simple.html
  - Transmission: https://uk-energy-digital-twin.vercel.app/test-transmission.html

---

## 🗺️ What's Visualized

### Current (Live)
1. **UK Transmission Grid** - Muted yellow/gold lines
   - 14 major corridors covering entire UK
   - 400kV and 275kV routes
   - Based on National Grid ESO topology
   - Includes:
     - Scotland-England interconnectors (East & West)
     - Eastern 400kV spine (London → Edinburgh)
     - Western 400kV spine (London → Manchester → Scotland)
     - Midlands ring
     - Wales network (North & South)
     - Southwest peninsula
     - East Anglia & Humber regions

### Available (Not Yet Displayed)
- **GSP Boundaries:** 329 regions (1.6 MB GeoJSON)
- **Connection Queue:** 2,219 projects, 81.7 GW (906 KB GeoJSON)
- **Building Footprints:** 29.5M buildings from Overture Maps (2.2 GB)

---

## 🏗️ Tech Stack

**Frontend:**
- Vanilla JavaScript (no framework - for speed)
- Mapbox GL JS v3.0.1
- HTML/CSS

**Data:**
- Transmission: Manual GeoJSON based on National Grid topology
- Geographic: NESO official datasets
- Buildings: Overture Maps (downloaded but not deployed)

**Hosting & Deployment:**
- **Vercel** - Free tier, auto-deploy from GitHub
- **GitHub** - Version control
- No build process - pure static files

---

## 📁 Project Structure

```
energy_dt/
├── frontend/public/              # 🚀 DEPLOYED TO VERCEL
│   ├── index.html               # Main page
│   ├── app.js                   # Map logic (93 lines)
│   ├── data/
│   │   ├── transmission_lines.geojson     # 9.5 KB - UK grid
│   │   ├── gsp_boundaries.geojson         # 1.6 MB - GSP regions
│   │   └── tec_register_points.geojson    # 906 KB - Connection queue
│   ├── config.example.js        # Mapbox token template
│   └── test-*.html              # Debug/diagnostic pages
│
├── scripts/                      # Data processing
│   ├── create_real_transmission_network.py   # ⭐ Generates transmission data
│   ├── download_neso_data.py                 # NESO API downloads
│   ├── download_overture_buildings.py        # Overture Maps downloader
│   └── simplify_geojson.py                   # Reduce GeoJSON file sizes
│
├── data/
│   ├── raw/                     # Downloaded datasets (54 MB)
│   │   ├── infrastructure/      # GSP boundaries, substations
│   │   ├── queue/              # TEC Register, NGED queues
│   │   ├── demand/             # Historic demand (26 years)
│   │   └── operational/        # Real-time generation/demand
│   └── processed/              # Processed data
│       └── uk_buildings_overture.geojson  # 18 GB - not deployed
│
├── vercel.json                  # Deployment configuration
├── README.md                    # This file
└── CONTEXT.md                   # Context restoration guide
```

---

## 🎯 How It Works

### Map Rendering
```javascript
// 1. Load Mapbox dark-v11 style
// 2. Remove all text labels for clean look
// 3. Load transmission lines GeoJSON
// 4. Render as muted yellow lines (4px, 90% opacity)
```

### Data Flow
```
1. User visits site
2. Vercel serves frontend/public/
3. Browser loads app.js
4. Fetches transmission_lines.geojson
5. Mapbox renders on dark background
6. Interactive map ready (~2 seconds)
```

---

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone https://github.com/NikhilSDesai/energy_digital_twin.git
cd energy_dt

# Serve locally
cd frontend/public
python -m http.server 8000
# Visit http://localhost:8000
```

### Deploy Changes
```bash
git add .
git commit -m "Your changes"
git push
# Vercel auto-deploys in 1-2 minutes
```

### Create Mapbox Token
1. Get token from https://account.mapbox.com
2. For local dev: Create `frontend/public/config.js`:
```javascript
const CONFIG = { mapboxToken: 'pk.your-token-here' };
```
3. For production: Token embedded in app.js (already configured)

---

## 📊 Data Inventory

### Deployed (Live on Site)
| Dataset | Size | Features | Source |
|---------|------|----------|--------|
| Transmission Lines | 9.5 KB | 14 routes | Manual (National Grid topology) |

### Available (In Repo)
| Dataset | Size | Features | Source |
|---------|------|----------|--------|
| GSP Boundaries | 1.6 MB | 329 regions | NESO |
| TEC Register | 906 KB | 2,219 projects | NESO |
| Historic Demand | 54 MB | 26 years | NESO |
| Overture Buildings | 18 GB | 29.5M buildings | Overture Maps |

### Data Sources
- **NESO** (National Energy System Operator): https://www.neso.energy/data-portal
- **BMRS** (Balancing Mechanism): https://data.elexon.co.uk/bmrs/api/v1
- **NGED** (Distribution Network): https://connecteddata.nationalgrid.co.uk
- **Overture Maps**: https://overturemaps.org

---

## 🎨 Map Features

**Controls:**
- **Scroll:** Zoom in/out
- **Click + Drag:** Pan around
- **Press 'R':** Reset to UK view

**Styling:**
- Background: Dark Mapbox theme
- Labels: Removed (minimal aesthetic)
- Transmission Lines: #d4af37 (muted gold), 4px wide, 90% opacity
- Initial View: Full UK (center: -2.5, 54.5, zoom: 5.8)

---

## 🔧 Scripts

### Generate Transmission Network
```bash
python scripts/create_real_transmission_network.py
# Creates frontend/public/data/transmission_lines.geojson
```

### Download NESO Data
```bash
python scripts/download_neso_data.py
# Downloads: GSP boundaries, TEC Register, Historic demand
```

### Download Buildings (29.5M buildings, ~10 minutes)
```bash
source venv/bin/activate
pip install overturemaps
python scripts/download_overture_buildings.py
# Creates 18 GB GeoJSON file
```

### Simplify GeoJSON
```bash
python scripts/simplify_geojson.py
# Reduces coordinate precision
# 6.4 MB → 1.6 MB (GSP boundaries)
```

---

## 🚧 Known Issues & Limitations

### Current Limitations
- ❌ Connection queue not visualized (data exists, not displayed)
- ❌ GSP boundaries not shown (data exists, not displayed)
- ❌ Buildings not deployed (too large for Vercel - 2.2 GB)
- ❌ No real-time data integration
- ❌ Transmission lines approximate (based on topology, not exact GPS routes)

### Deployment Constraints
- Vercel free tier: 100 MB per file limit
- Buildings dataset: 2.2 GB (needs external hosting: S3/R2)

### Future Enhancements
1. Display connection queue projects as points
2. Show GSP boundary overlays
3. Add building footprints (via external tile hosting)
4. Real-time generation/demand data from BMRS
5. Analytics dashboard with charts
6. Demand forecasting tools

---

## 🐛 Troubleshooting

**Map shows pure black:**
- This is CORRECT at low zoom (country-wide view)
- Transmission lines should be visible as yellow lines
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+F5` (Windows)

**Map not loading:**
- Check browser console for errors (F12)
- Try test pages to isolate issue
- Verify Mapbox token is valid

**Transmission lines not visible:**
- Ensure latest deployment (check vercel ls)
- Lines are muted yellow (#d4af37), should be visible at all zooms
- Try test-transmission.html page

---

## 📈 Performance

- **Initial Load:** ~2 seconds
- **Data Transfer:** ~10 KB (transmission lines only)
- **Map Tiles:** Loaded on-demand from Mapbox
- **Browser:** Modern browsers with WebGL support

---

## 🎯 Original Vision vs. Current State

### Original Goals
1. ✅ **Visualize UK energy grid** - DONE
2. ⏳ **Run infrastructure simulations** - NOT STARTED
3. ⏳ **Forecast demand** - NOT STARTED
4. ⏳ **Analyze connection queue** - DATA READY, NOT DISPLAYED

### What We Built
- Clean, minimal web visualization of transmission grid
- Real data foundation (54 MB datasets downloaded)
- Deployable, shareable product (live on Vercel)
- Extensible platform for future features

---

## 📝 Git Workflow

```bash
# Check status
git status

# Commit (NO Claude credit in messages)
git add <files>
git commit -m "Description of changes"

# Deploy
git push  # Auto-deploys to Vercel

# Monitor deployments
vercel ls
```

---

## 📚 Documentation

- **README.md** (this file) - Project overview
- **CONTEXT.md** - Context restoration guide for Claude
- **LAUNCH.md** - Original launch summary (outdated)
- **DATA_INVENTORY.md** - Detailed data documentation

---

## 🏆 Achievement Summary

**What We Accomplished:**
- ✅ Researched UK vs US energy data landscape
- ✅ Downloaded 54 MB of UK energy data (33 files)
- ✅ Built interactive web map visualization
- ✅ Deployed to production (Vercel)
- ✅ Created transmission network from grid topology
- ✅ Downloaded 29.5M UK building footprints
- ✅ Established data pipeline and processing scripts

**Time:** Single extended session
**Cost:** $0
**Status:** Live and accessible

---

## 🔄 Next Session Priorities

1. **Add connection queue visualization** - Data ready, just needs map layer
2. **Show GSP boundaries** - Data ready, just needs map layer
3. **Deploy buildings** - Either reduce dataset or use external hosting
4. **Add interactivity** - Click on lines/regions for info popups
5. **Real-time data** - Integrate BMRS API for live generation

---

## 📧 Links

- **Live Site:** https://uk-energy-digital-twin.vercel.app
- **GitHub:** https://github.com/NikhilSDesai/energy_digital_twin
- **Vercel:** Auto-deployed from main branch

---

## 📄 License

MIT - Open source

**Data Attribution:**
- National Energy System Operator (NESO) - Open Data License
- Elexon BMRS - BSC Open Data License
- Overture Maps - Community Data License

---

*Last Updated: November 3, 2026*
*Version: 1.0 - Live Web Application*
