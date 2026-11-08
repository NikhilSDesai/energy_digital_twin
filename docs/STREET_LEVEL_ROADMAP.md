# Street & Household-Level Grid Data - Comprehensive Roadmap

**Goal**: Build a UK Energy Digital Twin down to street-level and household-level distribution infrastructure

**Current Status**: ✅ Transmission (100%) + 25% Distribution (UKPN) + 29.5M Building Footprints
**Target**: 100% UK Coverage down to LV feeders, substations, and building connections

---

## 📊 Network Hierarchy (What We Need)

```
CURRENT ✅
├── Transmission (400kV, 275kV, 220kV) - 1,212 segments - DONE
├── Primary Substations (400/275kV → 132kV) - 395 sites - DONE
└── Distribution (UKPN only - 25% UK)
    ├── 132kV EHV - 685 lines - DONE
    ├── 66kV HV - 4 lines - DONE
    └── 33kV HV - 6,081 lines - DONE

TARGET 🎯
├── All 6 DNOs (100% UK Coverage)
│   ├── 132kV/66kV/33kV Primary Distribution
│   ├── 11kV High Voltage Distribution (STREET LEVEL)
│   ├── LV Substations (11kV → 400V transformers)
│   ├── LV Feeders (<1kV low voltage cables)
│   └── Service Connections (pole-to-building)
│
└── Building-Level Data
    ├── 29.5M Building Footprints - ALREADY HAVE ✅
    ├── Connection points
    ├── Estimated demand (via smart meter data)
    └── Supply capacity
```

---

## 🎯 Data Sources Identified

### **1. UK Power Networks (UKPN) - 25% UK** ✅ PARTIAL

**Coverage**: London (LPN), South East (SPN), East England (EPN)
**Status**: ✅ Already have 132kV, 66kV, 33kV
**Still Need**: 11kV feeders, LV substations, LV overhead lines

**Available Datasets**:
- ✅ [LV Overhead Lines Shapefile](https://ukpowernetworks.opendatasoft.com/explore/assets/ukpn-lv-overhead-lines-shapefile/)
- ✅ [LV Poles](https://ukpowernetworks.opendatasoft.com/explore/assets/ukpn-lv-poles/)
- ⏳ 11kV Feeders (need to find)
- ⏳ LV Substations (need to find)

**Portal**: https://ukpowernetworks.opendatasoft.com/

---

### **2. National Grid Electricity Distribution (NGED) - 30% UK** 🎯 PRIORITY

**Coverage**: Midlands, South West, South Wales, West Midlands
**Customers**: 7.9 million (largest DNO)
**Status**: ❌ Not yet integrated

**Available Datasets**:
- ✅ [11kV Substations Shapefile](https://connecteddata.nationalgrid.co.uk/dataset/11kv-transformers) - ALL NGED AREAS
- ✅ [Distribution Substations](https://connecteddata.nationalgrid.co.uk/dataset/distribution-substations)
- ✅ [LV Load Monitor Data](https://connecteddata.nationalgrid.co.uk/dataset/lv-load-monitor-data)
- ✅ [Substation Loading Details](https://connecteddata.nationalgrid.co.uk/dataset/substation-loading-details)
- ✅ 11kV Overhead Lines, Poles - Shapefile/DWG/DGN formats

**Portal**: https://connecteddata.nationalgrid.co.uk/

**Formats Available**:
- ESRI Shapefile (SHP) ⭐
- AutoCAD DWG
- Bentley MicroStation DGN
- PDF Maps

---

### **3. Scottish & Southern Electricity Networks (SSEN) - 14% UK**

**Coverage**: North Scotland, South England (Hampshire, Berkshire)
**Customers**: 3.9 million
**Status**: ❌ Not yet integrated

**Available Datasets**:
- ✅ [Smart Meter Half-Hourly Consumption Data](https://www.ssen.co.uk/news-views/2024/SSEN-first-DNO-publish-smart-meter-half-hourly-consumption-datasets) - LV Feeder Level
- ✅ Network Visibility 100% through monitoring + smart meters
- ⏳ GIS shapefiles (need to locate portal)

**Portal**: https://www.ssen.co.uk/ (check for open data portal)

---

### **4. SP Energy Networks (SPEN) - 14% UK**

**Coverage**: Central & South Scotland, Merseyside, Cheshire, North Wales
**Customers**: 3.5 million
**Status**: ❌ Not yet integrated

**Datasets**: Need to research SP Energy Networks open data portal

---

### **5. Northern Powergrid (NPG) - 14% UK**

**Coverage**: North East England, Yorkshire
**Customers**: 3.9 million
**Status**: ❌ Not yet integrated

**Available Datasets**:
- ✅ [Aggregated Smart Meter Data](https://northernpowergrid.opendatasoft.com/explore/dataset/aggregated-smart-metering-data/) - LV Feeder & Substation Level

**Portal**: https://northernpowergrid.opendatasoft.com/

---

### **6. Electricity North West (ENWL) - 9% UK**

**Coverage**: North West England
**Customers**: 2.4 million
**Status**: ❌ Not yet integrated

**Available Datasets**:
- ✅ [Smart Meter Data Value Report](https://www.enwl.co.uk/globalassets/future-energy/dso/dso-consultation-documents/unlocking-value-from-smart-meter-data.pdf)

**Portal**: https://www.enwl.co.uk/ (check for open data)

---

## 🗺️ Additional Data Layers

### **Smart Meter Consumption Data** (NEW! Required from Feb 2024)

**Requirement**: All DNOs must publish Aggregated Smart Meter Consumption Data at LV Feeder level

**What This Gives Us**:
- Half-hourly consumption at LV substation level
- Aggregated demand per feeder
- Load profiles
- Peak demand times

**DNOs Publishing**:
- ✅ SSEN - Full half-hourly datasets
- ✅ Northern Powergrid - LV feeder & substation level
- ✅ NGED - LV Load Monitor Data
- ⏳ Others - check portals

---

### **Building Footprints** ✅ ALREADY HAVE

**Source**: Overture Maps
**Coverage**: 29.5 million UK buildings
**File Size**: 18 GB GeoJSON
**Location**: `data/processed/uk_buildings_overture.geojson`

**Properties**:
- Building footprint geometries
- Building types
- Addresses (where available)
- Height/levels (some buildings)

---

### **OpenStreetMap Power Infrastructure**

**Available via Overpass/Geofabrik**:
- LV poles and cables
- Distribution transformers
- Street-level infrastructure
- Community-mapped power lines

**Status**: Partial coverage, varies by area

---

## 📋 Phased Implementation Plan

### **Phase 1: Complete Primary Distribution (11kV+)** 🎯 NEXT

**Goal**: Get 11kV and primary substation data for all 6 DNOs

**Tasks**:
1. ✅ **NGED 11kV Substations** - Download from connecteddata.nationalgrid.co.uk
2. ✅ **NGED Distribution Network** - Get 33kV, 11kV shapefiles
3. ⏳ **SSEN Primary Network** - Find and download GIS data
4. ⏳ **SPEN Primary Network** - Research data portal
5. ⏳ **NPG Primary Network** - Check for GIS downloads
6. ⏳ **ENWL Primary Network** - Locate open data

**Data Volume**: ~50,000-100,000 line segments
**Coverage**: 100% UK at 11kV level

---

### **Phase 2: LV Substations & Transformers**

**Goal**: Map all 11kV → 400V distribution transformers (street-level substations)

**Sources**:
- NGED: LV Load Monitor Data
- UKPN: LV Substations (need to find dataset)
- SSEN/NPG/SPEN/ENWL: Request or find portals

**Estimated Count**: ~500,000-800,000 LV substations UK-wide
**Granularity**: **Street-level accuracy**

---

### **Phase 3: LV Feeders & Cables**

**Goal**: Map low voltage (<1kV) distribution cables from substations to buildings

**Sources**:
- UKPN: LV Overhead Lines ✅ Available
- NGED: Check for LV cable data
- OpenStreetMap: Community-mapped LV infrastructure
- Smart Meter Data: Infer feeder routes from consumption patterns

**Estimated**: Millions of LV feeder segments
**Granularity**: **Street/building-level**

---

### **Phase 4: Building Connections & Demand**

**Goal**: Link buildings to their supply substations and estimate demand

**Approach**:
1. **Spatial Join**: Match 29.5M buildings to nearest LV substation (within ~300m radius)
2. **Smart Meter Data**: Aggregate consumption per feeder
3. **Demand Estimation**:
   - Residential: ~3-5 kW average
   - Commercial: Varies widely
   - Use building type from Overture Maps

**Output**: Building-level supply source + estimated load

---

## 🛠️ Technical Implementation

### **Data Processing Pipeline**

```python
# 1. Download DNO Data
download_nged_11kv_substations()
download_nged_distribution_lines()
download_ukpn_lv_data()
download_all_dno_networks()

# 2. Standardize Formats
convert_to_geojson()
standardize_properties()
harmonize_voltage_classes()

# 3. Combine Datasets
merge_all_dnos()
create_national_11kv_network()
create_lv_substation_layer()

# 4. Link to Buildings
spatial_join_buildings_to_substations()
assign_feeder_zones()
estimate_building_demand()

# 5. Create Visualization Layers
generate_11kv_layer()  # Yellow-green lines
generate_lv_substation_layer()  # Small circles
generate_lv_feeder_layer()  # Very thin lines, only visible at high zoom
generate_building_demand_heatmap()  # Color by estimated kW
```

### **Frontend Integration**

```javascript
// Progressive disclosure by zoom level
map.on('zoom', () => {
  const zoom = map.getZoom();

  // Zoom 0-7: Transmission only (400kV, 275kV)
  // Zoom 8-10: + 132kV distribution
  // Zoom 11-13: + 33kV/66kV distribution
  // Zoom 14-16: + 11kV network (STREET LEVEL)
  // Zoom 17-19: + LV substations + building outlines
  // Zoom 20+: + LV feeders + building demand
});
```

---

## 📊 Expected File Sizes

| Layer | Features | File Size | Zoom Range |
|-------|----------|-----------|------------|
| **Transmission** | 1,212 | 883 KB | 0-24 |
| **132/66/33kV (All DNOs)** | ~50,000 | ~50 MB | 8-24 |
| **11kV Network (All DNOs)** | ~200,000 | ~150 MB | 14-24 |
| **LV Substations** | ~800,000 | ~80 MB | 17-24 |
| **LV Feeders** | ~5,000,000 | ~500 MB | 19-24 |
| **Buildings** | 29,500,000 | **18 GB** | 18-24 ⚠️ |
| **TOTAL** | ~35M features | **~19 GB** | - |

**Challenge**: 18 GB building layer too large for web browser

**Solutions**:
1. **Tile-based serving** (Mapbox/PMTiles)
2. **Server-side filtering** by viewport
3. **Simplified geometries** at lower zooms
4. **Aggregate to building clusters** until zoom 18+
5. **On-demand loading** only for visible area

---

## 🎯 Immediate Next Steps

### **Week 1-2: NGED Data Integration** 🚀

1. **Download NGED 11kV Data**
   ```bash
   # Visit https://connecteddata.nationalgrid.co.uk/
   # Download 11kV Substations Shapefile
   # Download 11kV Overhead Lines Shapefile
   # Download Distribution Substations
   ```

2. **Process & Convert**
   ```bash
   python scripts/download_nged_network.py
   python scripts/convert_nged_shapefiles.py
   python scripts/standardize_nged_properties.py
   ```

3. **Integrate to Frontend**
   ```javascript
   // Add 11kV layer (visible zoom 14+)
   // Add NGED substations
   // Color by voltage: 11kV green
   ```

4. **Deploy**
   - Test locally
   - Push to Vercel
   - Verify 30% more UK coverage

---

### **Week 3-4: UKPN LV Data**

1. Download UKPN LV Overhead Lines
2. Download UKPN LV Poles
3. Add LV layer (visible zoom 18+)

---

### **Month 2: Remaining DNOs**

1. SSEN network data
2. SPEN network data
3. NPG network data
4. ENWL network data

**Goal**: 100% UK coverage at 11kV level

---

### **Month 3: LV Substations**

1. Collect LV substation datasets from all DNOs
2. Process ~800K substations
3. Add to map at zoom 17+

---

### **Month 4: Building Integration**

1. Optimize 18 GB building dataset
2. Create vector tiles
3. Link buildings to substations
4. Add demand estimation layer

---

## 📚 Key Resources

### Data Portals
- [NGED Connected Data Portal](https://connecteddata.nationalgrid.co.uk/) ⭐ PRIORITY
- [UKPN Open Data Soft](https://ukpowernetworks.opendatasoft.com/)
- [Northern Powergrid Open Data](https://northernpowergrid.opendatasoft.com/)
- [Open Net Zero - All DNO Datasets](https://opennetzero.org/)
- [SSEN Network Data](https://www.ssen.co.uk/)

### Technical Guides
- [SSEN Network Visibility Strategy](https://www.ssen.co.uk/globalassets/about-us/stakeholder-engagement/annual-engagement-plans-and-reports/ssen-network-visibility-strategy-feb-2024.pdf)
- [UKPN Smart Grid Index](https://dso.ukpowernetworks.co.uk/smart-grid-index)
- [Awesome Electrical Grid Mapping](https://open-energy-transition.github.io/Awesome-Electrical-Grid-Mapping/)

### Regulations
- [Distribution Network Options Assessment (DNOA)](https://dso.nationalgrid.co.uk/downloads/15122/dnoa-methodology-february-2026.pdf)
- [Ofgem Data Best Practice Guidance](https://www.ofgem.gov.uk/)
- [Smart Meter Data Licensing](https://www.cse.org.uk/wp-content/uploads/2023/04/PIAG-phase-2-privacy-plans-annex.pdf)

---

## 🎯 Success Metrics

| Metric | Current | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|---------|
| **UK Coverage** | 25% | 100% | 100% | 100% | 100% |
| **Voltage Levels** | 132-400kV | +11kV | +LV substations | +LV feeders | +Buildings |
| **Granularity** | Regional | District | Street | Street | **Household** |
| **Zoom Detail** | 8+ | 14+ | 17+ | 19+ | 20+ |
| **Features** | 9,910 | ~250K | ~1M | ~5M | **~35M** |

---

## 💰 Cost & Licensing

### Data Licensing

All DNO data checked so far appears to be **Open Data** with various licenses:
- NGED: Shapefiles downloadable (check terms)
- UKPN: Open Data Soft (likely ODbL)
- Smart Meter: Aggregated only (privacy compliant)
- Overture Maps: CC-BY 4.0 (buildings)
- OpenStreetMap: ODbL

**Commercial Use**: Verify each DNO's licensing terms
**Attribution Required**: Yes for all sources

### Infrastructure Costs

- **Hosting**: Vercel Free Tier (current) or Pro ($20/month for larger datasets)
- **Tile Serving**: Mapbox (free up to 750K loads/month) or self-hosted PMTiles
- **Processing**: Local machine sufficient
- **Storage**: ~20 GB total (GeoJSON + tiles)

---

## 🚀 Vision: Household-Level Digital Twin

**End Goal**: Click any UK building and see:
- ✅ Connected substation (name, location)
- ✅ Supply voltage (11kV → 400V)
- ✅ Feeder circuit
- ✅ Estimated demand (kW)
- ✅ Estimated capacity (kVA)
- ✅ Network constraints (if any)
- ✅ Renewable connection potential
- ✅ Time-of-use pricing zone

**Use Cases**:
- 🏠 **Homeowners**: Check grid capacity for solar/EV/heat pump
- ⚡ **Developers**: Site renewable projects
- 🏗️ **Planners**: Assess grid capacity for new housing
- 🔌 **EV Installers**: Verify supply for chargers
- 📊 **Researchers**: Analyze grid constraints
- 🌍 **Climate Action**: Identify decarbonization opportunities

---

**Let's build the most detailed open-source power grid visualization in the world!** 🌍⚡

*Roadmap created: November 7, 2026*
