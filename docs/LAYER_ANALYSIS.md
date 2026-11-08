# Deep Analysis: Missing Layer Categories & Organization

## 🤔 Current Categories (Initial Plan)

1. Transmission Network
2. Distribution Network
3. Power Generation
4. Substations
5. Network Boundaries
6. Buildings & Demand

---

## 🔍 What's Missing? Deep Analysis

### Critical Missing Category: **Connection Queue**

**We have TEC Register data (2,219 projects, 741 GW) but it's not categorized!**

This is arguably one of the most important datasets:
- Shows planned/queued generation projects
- Indicates future network constraints
- Shows where development is happening
- Massive capacity (741 GW vs 64 GW operational)

**Recommendation**: Add as major category between Generation and Substations

---

### Missing: **Base Layers & Context**

Users need context to understand the energy infrastructure:

**Geographic Context:**
- Satellite/aerial imagery
- Street map overlay
- Terrain/topography
- Water bodies (relevant for hydro, cooling)
- Coastline (relevant for offshore wind)

**Administrative Boundaries:**
- Countries (Scotland, Wales, England, NI)
- Regions
- Counties
- Cities/urban areas
- Protected areas (National Parks - affects planning)

**Recommendation**: Add "Base Layers" category at the top

---

### Missing: **Cable vs Overhead Distinction**

Current categories lump together overhead and underground:
- Distribution lines can be overhead OR underground
- Different visual representation needed
- Different constraints (underground = higher cost but less visual impact)
- We have some of this data (UKPN distinguishes)

**Current**: "132kV Lines"
**Better**:
- "132kV Overhead Lines"
- "132kV Underground Cables"

**Recommendation**: Split voltage levels by overhead/underground where data exists

---

### Missing: **Infrastructure Status/Timeline**

Not all infrastructure is operational:
- **Operational** (live now)
- **Under Construction** (work in progress)
- **Planned** (approved, not started)
- **Queued** (waiting for connection)
- **Decommissioned** (historical)

TEC Register has status field:
- "Accepted"
- "Awaiting Connection"
- "Awaiting Modification"
- etc.

**Recommendation**: Use color coding or separate layers by status

---

### Missing: **Network Detail Assets**

Smaller infrastructure components:
- **Poles & Towers** (we attempted download, got empty data)
- **Cable Joints**
- **Switchgear**
- **Circuit Breakers**
- **Transformers** (standalone, not in substations)

**Reality Check**: We don't have most of this data yet, and it may be too detailed for overview visualization.

**Recommendation**: Add category but mark as "Coming Soon" until we get data

---

### Missing: **Demand Side Infrastructure**

Current focus is supply (generation, transmission), but demand side matters:
- **EV Charging Points** (growing rapidly)
- **Heat Pump Installations** (future)
- **Major Industrial Loads** (data centers, factories)
- **District Heating Networks**

**Recommendation**: Add "Demand Infrastructure" category for future expansion

---

### Better Organization: **Generation Split**

Current "Power Generation" is too broad:

**Option A: By Status**
- Operational Generation (2,587 sites, 64 GW)
- Planned Generation (TEC: 2,219 projects, 741 GW)

**Option B: By Location**
- Onshore Generation
- Offshore Generation

**Option C: Keep by Technology** (current)
- Wind, Solar, Gas, etc.

**Recommendation**: Split into "Operational Generation" and "Connection Queue", each with technology subtypes

---

### Better Organization: **Substations by Function**

Current "Substations" mixes different types:

**By Voltage Transformation:**
- 400/275kV Transmission Substations
- 275/132kV Grid Supply Points (GSP)
- 132/33kV Bulk Supply Points (BSP)
- 33/11kV Primary Substations
- 11kV/LV Distribution Substations

**By Function:**
- Transformation (voltage change)
- Switching (routing only)
- Mixed (both)

**Recommendation**: Organize by voltage level transformation

---

### Better Organization: **Boundaries with Hierarchy**

Current "Network Boundaries" is flat:

**Better Hierarchy:**
```
Network Regions
├── National Grid ESO Area (GB)
├── GSP Group Regions (14 groups)
├── DNO License Areas (6 DNOs)
│   ├── UKPN (3 networks: LPN, SPN, EPN)
│   ├── NGED (4 networks: West Mids, East Mids, SW, S Wales)
│   ├── SPEN (2 networks: SPD, SPM)
│   └── ...
├── BSP Service Areas
└── Primary Substation Service Areas (195 South Wales + more)
```

**Recommendation**: Show hierarchy in UI, allow drilling down

---

## 🎯 REVISED COMPLETE CATEGORIZATION

Based on deep analysis, here's the recommended structure:

### 1. 🗺️ **Base Layers** (Context & Reference)
- Satellite Imagery
- Street Map
- Terrain
- Administrative Boundaries (Countries, Regions, Counties)
- Urban Areas
- Water Bodies & Coastline

### 2. 🔌 **Transmission Network** (400-220kV)
- 400kV Overhead Lines
- 275kV Overhead Lines
- 220kV Offshore Links
- DC Interconnectors
- International Interconnectors (to Ireland, France, Belgium, Norway, Netherlands)

### 3. ⚡ **Distribution Network** (132kV-LV)
**132kV Network**
  - Overhead Lines
  - Underground Cables

**66kV Network**
  - Overhead Lines
  - Underground Cables

**33kV Network**
  - Overhead Lines
  - Underground Cables

**11kV Network** (coming soon)
  - Overhead Lines
  - Underground Cables

**LV Network** (<1kV, future)

### 4. 🏭 **Generation - Operational** (64.4 GW)
- Wind Farms (Onshore) - 580 sites, 13.6 GW
- Wind Farms (Offshore) - 26 sites, 2.9 GW
- Solar PV - 1,227 sites, 12.6 GW
- Natural Gas - 166 plants, 20.3 GW
- Nuclear - (identify from existing data)
- Hydro - 105 sites, 1.5 GW
- Biomass - 304 sites, 3.8 GW
- Battery Storage - 178 sites, 9.7 GW
- Tidal - 1 site, 6 MW
- Other

### 5. 📋 **Connection Queue** (741 GW planned)
**By Technology:**
- Queued Wind
- Queued Solar
- Queued Storage
- Queued Other

**By Status:**
- Accepted
- Awaiting Connection
- Awaiting Modification
- Under Construction

### 6. 🏢 **Substations & Transformation**
- Transmission Substations (400/275kV)
- Grid Supply Points (275/132kV GSP)
- Bulk Supply Points (132/33kV BSP)
- Primary Substations (33/11kV) - 195 South Wales
- Distribution Substations (11kV/LV)

### 7. 🗺️ **Network Regions & Boundaries**
**National Grid ESO**
  - GB Transmission Network Area

**GSP Groups**
  - 14 GSP Group Regions

**DNO License Areas**
  - UKPN (London, SE, East England) - 8.4M customers
  - NGED (Midlands, SW, Wales) - 7.9M customers
  - SPEN (Scotland, NW England) - 3.5M customers
  - SSEN (N Scotland, S England) - 3.9M customers
  - NPG (NE England, Yorkshire) - 3.9M customers
  - ENWL (NW England) - 2.4M customers

**Service Areas**
  - BSP Service Areas
  - Primary Substation Areas (195 South Wales)

### 8. 🏘️ **Buildings & Demand**
- Building Footprints (29.5M UK-wide)
- LV Feeders (future)
- Major Demand Centers (future)
- EV Charging Infrastructure (future)
- Heat Pump Installations (future)

### 9. 🔧 **Network Assets** (Detail - Future)
- Poles & Towers
- Cable Joints
- Switchgear
- Circuit Breakers
- Protection Devices
*(Mark as "Coming Soon" - data not available yet)*

---

## 📊 Key Insights & Recommendations

### 1. **Must Add: Connection Queue**
This is critical data we have but haven't categorized. Should be prominent.

### 2. **Must Add: Base Layers**
Users need context - satellite, streets, boundaries. Currently missing.

### 3. **Should Split: Operational vs Planned Generation**
Clear distinction between what exists (64 GW) vs what's planned (741 GW)

### 4. **Should Distinguish: Overhead vs Underground**
Where data exists (UKPN), show the distinction. Important for planning/constraints.

### 5. **Should Organize: Substations by Voltage**
More logical than mixing transmission/distribution/primary together.

### 6. **Could Add: Network Assets**
But mark as future - we don't have this data yet.

### 7. **Future: Demand Infrastructure**
EV charging, heat pumps - important for future planning but no data yet.

---

## 🎯 Recommended Implementation Priority

### Phase 1 (Implement Now):
1. ✅ Base Layers
2. ✅ Transmission Network
3. ✅ Distribution Network (split overhead/underground where available)
4. ✅ Generation - Operational (by technology)
5. ✅ Connection Queue (NEW - TEC Register)
6. ✅ Substations (organized by voltage)
7. ✅ Network Regions & Boundaries
8. ✅ Buildings (when tiles ready)

### Phase 2 (Future):
9. Network Assets (when data available)
10. Demand Infrastructure (when data available)

---

## 💡 Final Category Structure for Implementation

```
🗺️ Base Layers
   └─ Satellite, Streets, Terrain, Boundaries

🔌 Transmission (400-220kV)
   ├─ 400kV Lines
   ├─ 275kV Lines
   ├─ 220kV Offshore
   └─ DC Interconnectors

⚡ Distribution (132kV-LV)
   ├─ 132kV (Overhead, Underground)
   ├─ 66kV (Overhead, Underground)
   ├─ 33kV (Overhead, Underground)
   └─ 11kV (Coming Soon)

🏭 Operational Generation (64.4 GW)
   ├─ Wind (Onshore)
   ├─ Wind (Offshore)
   ├─ Solar
   ├─ Gas
   ├─ Nuclear
   ├─ Hydro
   ├─ Biomass
   └─ Battery Storage

📋 Connection Queue (741 GW)
   ├─ Queued Wind
   ├─ Queued Solar
   ├─ Queued Storage
   └─ By Status (Accepted, Awaiting, etc.)

🏢 Substations
   ├─ Transmission (400/275kV)
   ├─ GSP (275/132kV)
   ├─ BSP (132/33kV)
   ├─ Primary (33/11kV)
   └─ Distribution (11kV/LV)

🗺️ Network Regions
   ├─ National Grid Area
   ├─ GSP Groups (14)
   ├─ DNO Areas (6)
   └─ Service Areas

🏘️ Buildings (29.5M)
   └─ Building Footprints
```

---

**This structure:**
- ✅ Includes all data we currently have
- ✅ Organizes logically by infrastructure type and voltage
- ✅ Distinguishes operational vs planned
- ✅ Adds critical context (base layers)
- ✅ Shows hierarchy where it matters (substations, regions)
- ✅ Leaves room for future expansion
- ✅ Matches user mental model of the electricity system

**Ready to implement this?**
