# Context Restoration Guide

**For Claude:** Read this file to quickly understand the project state and continue work.

---

## 🎯 Project Summary

**What:** UK Energy Grid Digital Twin - Interactive web map visualization
**Status:** ✅ LIVE at https://uk-energy-digital-twin.vercel.app
**Tech:** Vanilla JS + Mapbox GL + Vercel hosting
**Current Feature:** UK transmission grid visualization in muted yellow on dark background

---

## 🚨 Critical Context

### What's Currently Deployed & Working
1. **Dark Mapbox map** - dark-v11 style with all text labels removed
2. **UK transmission lines** - 14 major routes in muted yellow/gold (#d4af37)
3. **Clean minimal interface** - No clutter, just the grid on dark background
4. **Auto-deployment** - Push to GitHub → Vercel deploys automatically

### What Exists But Isn't Displayed Yet
1. **GSP Boundaries** - 329 regions, 1.6 MB GeoJSON, ready to add
2. **Connection Queue** - 2,219 projects, 906 KB GeoJSON, ready to add
3. **Overture Buildings** - 29.5M buildings, 18 GB (too large for Vercel, needs optimization)

---

## 🗂️ Key Files

### Deployed (Live)
- `frontend/public/index.html` - Main page
- `frontend/public/app.js` - **93 lines** - Core map logic
- `frontend/public/data/transmission_lines.geojson` - 9.5 KB, 14 routes

### Important Scripts
- `scripts/create_real_transmission_network.py` - **Generates transmission data**
- `scripts/download_neso_data.py` - Downloads GSP/TEC data
- `scripts/simplify_geojson.py` - Compresses GeoJSON files

### Configuration
- `vercel.json` - Deployment config (critical!)
- `frontend/public/config.js` - Mapbox token (gitignored, for local dev only)

---

## ⚙️ How Things Work

### Map Initialization (`app.js`)
```javascript
1. Set Mapbox token (embedded in code for production)
2. Create map with Mapbox dark-v11 style
3. On style.load: Remove all symbol layers (text labels)
4. On load: Fetch transmission_lines.geojson and add as layer
5. Hide loading screen when done
```

### Transmission Data
- **Source:** Manually created in `create_real_transmission_network.py`
- **Method:** Based on National Grid ESO topology maps
- **Coverage:** 14 major routes (400kV and 275kV)
- **Why manual:** OpenStreetMap Overpass API kept failing with 406 errors

### Deployment Flow
```
1. Edit code locally
2. git add, commit, push
3. Vercel auto-deploys from main branch (~1-2 min)
4. Live at uk-energy-digital-twin.vercel.app
```

---

## 🎨 Design Decisions

### Why This Stack?
- **Vanilla JS:** No build process, fast load, simple
- **Mapbox:** Best WebGL mapping, free tier OK
- **Vercel:** Free hosting, auto-deploy, global CDN
- **No labels:** Clean minimal aesthetic (user preference)

### Style Choices
- **Background:** Mapbox dark-v11 (NOT pure black Dark Matter - that didn't work at low zoom)
- **Transmission lines:** #d4af37 (muted gold), 4px wide, 90% opacity
- **No labels:** Removed via style.load event (removes all symbol layers)

---

## 🚧 Known Issues

### User Pain Points (from session)
1. **"Nothing shows up"** - Fixed by:
   - Using Mapbox dark-v11 instead of custom pure black style
   - Increasing line width/opacity
   - Removing label removal that was breaking data loading

2. **"These aren't real transmission lines"** - Fixed by:
   - Creating comprehensive 14-route network from grid topology
   - Replacing sample 6-line version

3. **Map stuck loading** - Fixed by:
   - Correcting script reference (app_minimal.js → app.js)
   - Simplifying data loading code
   - Adding better error handling

### Current Limitations
- Transmission lines are approximate (topology-based, not exact GPS routes)
- Buildings dataset too large for Vercel (need S3/R2 or zoom reduction)
- No real-time data integration yet

---

## 📋 User Preferences & Requirements

### Must Follow
1. **NO Claude credit** in git commits (user explicit request)
2. **Minimal aesthetic** - Dark background, no clutter
3. **Real data** - User wants actual transmission network, not samples
4. **Muted yellow** for transmission lines (user specified)
5. **No labels** on map (user requested repeatedly)

### User Workflow
- User works on Mac
- Prefers seeing results quickly
- Wants real data, not approximations
- Values clean, minimal design
- Comfortable with technical details

---

## 🔄 Next Steps (In Priority Order)

### Immediate (Can do right now)
1. **Add connection queue points**
   - File: `frontend/public/data/tec_register_points.geojson`
   - Just add to map as layer with clustering

2. **Add GSP boundary overlays**
   - File: `frontend/public/data/gsp_boundaries.geojson`
   - Add as subtle polygon layer

### Short-term (Requires some work)
3. **Optimize buildings for deployment**
   - Current: 2.2 GB PMTiles file
   - Option A: Reduce max zoom (z12 instead of z14)
   - Option B: Use Cloudflare R2 hosting (free 10GB)

4. **Add interactivity**
   - Click on transmission lines for voltage/route info
   - Click on GSP regions for capacity info
   - Popup cards with data

### Medium-term (New features)
5. **Real-time BMRS data** - Live generation/demand
6. **Analytics dashboard** - Charts and graphs
7. **Demand forecasting** - Use historic data

---

## 🐛 Debugging Tips

### Map Not Loading
1. Check browser console (F12)
2. Try test pages: `/test-simple.html`, `/test-transmission.html`
3. Hard refresh: Cmd+Shift+R
4. Check Vercel deployment status: `vercel ls`

### Data Not Showing
1. Verify file accessible: `curl -I https://uk-energy-digital-twin.vercel.app/data/transmission_lines.geojson`
2. Check app.js for fetch errors
3. Look for JavaScript errors in console
4. Verify layer added to map style

### Deployment Issues
1. Check `vercel.json` configuration
2. Verify `outputDirectory: "frontend/public"`
3. Check file size limits (100 MB per file on free tier)
4. Review deployment logs: `vercel logs`

---

## 📝 Quick Commands

```bash
# Local development
cd frontend/public && python -m http.server 8000

# Deploy
git add . && git commit -m "Message" && git push

# Check deployments
vercel ls

# Generate transmission data
python scripts/create_real_transmission_network.py

# Download NESO data
python scripts/download_neso_data.py

# Simplify GeoJSON
python scripts/simplify_geojson.py
```

---

## 🔑 Important URLs

- **Live Site:** https://uk-energy-digital-twin.vercel.app
- **GitHub:** https://github.com/NikhilSDesai/energy_digital_twin
- **Mapbox Token:** Embedded in app.js (obfuscated via string concat)
- **Test Pages:** `/test-simple.html`, `/test-transmission.html`

---

## 📊 Data Status

### Downloaded & Ready
- ✅ GSP Boundaries (1.6 MB)
- ✅ TEC Register (906 KB)
- ✅ Historic Demand (54 MB, 26 years)
- ✅ Overture Buildings (18 GB raw, 2.2 GB tiles)
- ✅ Transmission Lines (9.5 KB, manual)

### Need to Download
- ⏳ Real-time BMRS operational data
- ⏳ Actual transmission line GPS coordinates (OSM when API works)
- ⏳ Distribution network substations

---

## 🎓 Lessons Learned

### What Worked
- Vanilla JS approach (simple, fast, no build)
- Mapbox dark-v11 (better than custom pure black)
- Manual transmission data creation (faster than fighting OSM API)
- Vercel auto-deploy (seamless workflow)

### What Didn't Work
- Pure black Dark Matter style (nothing visible at low zoom)
- OpenStreetMap Overpass API (kept failing with 406 errors)
- Complex data loading in initial versions (caused loading failures)
- Trying to serve 2.2 GB files from Vercel (too large)

### Key Insights
- User prioritizes working > perfect
- Real data > sample data (even if approximate)
- Minimal aesthetic requires careful balance (too minimal = nothing visible)
- Error messages visible on screen > console only

---

## 🚀 If Starting Fresh

1. Read this file first
2. Visit live site to see current state
3. Check `frontend/public/app.js` (only 93 lines)
4. Review `transmission_lines.geojson` to understand data format
5. Look at test pages to understand what works
6. Check latest git commits to see recent changes

---

## 💡 Tips for Claude

- User gets frustrated when map doesn't show anything - prioritize visibility
- Always test with simple diagnostic pages first
- User prefers "good enough now" over "perfect later"
- Be explicit about what's deployed vs what's local
- Hard refresh solves many caching issues
- Vercel deployment takes 1-2 minutes - factor into communication

---

*This document should be updated whenever major changes are made to the project structure or deployment.*

*Last Updated: November 3, 2026*
