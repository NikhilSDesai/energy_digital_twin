# NGED 11kV Network Data - Manual Download Guide

**Goal**: Download 11kV+ network data for Midlands, South West, South Wales (30% UK, 7.9M customers)

---

## 🎯 What We Need

### Priority Datasets
1. **11kV Overhead Lines** (Shapefile) - Street-level power lines
2. **11kV Underground Cables** (Shapefile) - Underground distribution
3. **11kV Substations** (Shapefile) - Distribution transformers
4. **33kV Network** (Shapefile) - Primary distribution
5. **Distribution Substations** (CSV) - Substation details

---

## 📍 Data Portal Access

### Option 1: Connected Data Portal (Metadata + Links)
**URL**: https://connecteddata.nationalgrid.co.uk/

**Available Datasets**:
1. [11kV Overhead Lines](https://connecteddata.nationalgrid.co.uk/dataset/11kv_ohl_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
2. [11kV Underground Cables](https://connecteddata.nationalgrid.co.uk/dataset/11kv_ug_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
3. [11kV Substations](https://connecteddata.nationalgrid.co.uk/dataset/11kv-transformers)
4. [11kV Towers](https://connecteddata.nationalgrid.co.uk/dataset/11kv_towers_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
5. [11kV Poles](https://connecteddata.nationalgrid.co.uk/dataset/11kv_poles_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
6. [Distribution Substations](https://connecteddata.nationalgrid.co.uk/dataset/distribution-substations)

### Option 2: Main Data Portal (Actual Downloads)
**URL**: https://dataportal2.nationalgrid.co.uk/ → Redirects to https://dataportal2.westernpower.co.uk/

**Note**: This is where the actual shapefile downloads are hosted

---

## 📋 Step-by-Step Download Instructions

### Step 1: Visit the Data Portal
1. Go to https://connecteddata.nationalgrid.co.uk/
2. Or go directly to https://dataportal2.westernpower.co.uk/

### Step 2: Registration (If Required)
- You may need to create a free account
- Provide email and organization details
- Accept terms and conditions

### Step 3: Browse Datasets
Look for these categories:
- System and Network
- Distribution Network
- 11kV Assets
- Shapefiles

### Step 4: Download Files
For each dataset:
1. Click on the dataset page
2. Look for "Download" or "Export" button
3. Choose **ESRI Shapefile (SHP)** format
4. Save to: `data/official_sources/nged/`

### Step 5: Extract Files
```bash
cd data/official_sources/nged/
unzip 11kv_overhead_lines.zip
unzip 11kv_underground_cables.zip
unzip 11kv_substations.zip
```

---

## 🗺️ Alternative: OpenStreetMap Data

If the NGED portal is too difficult, we can use OpenStreetMap data for 11kV networks:

### Download OSM 11kV Data

```python
# Overpass API query for 11kV lines in NGED area
query = """
[out:json][timeout:300];
// NGED areas: Midlands, SW, Wales
(
  way["power"="line"]["voltage"="11000"](50.0,-6.0,54.0,0.0);
  way["power"="line"]["voltage"="11kV"](50.0,-6.0,54.0,0.0);
  node["power"="substation"]["voltage"="11000"](50.0,-6.0,54.0,0.0);
);
out geom;
"""
```

**Pros**:
- ✅ Free and open
- ✅ No registration required
- ✅ ODbL license
- ✅ Community-verified

**Cons**:
- ⚠️ May not be 100% complete
- ⚠️ Varies by area
- ⚠️ Less detailed than official data

---

## 📊 Expected File Sizes

| Dataset | Estimated Size | Features |
|---------|---------------|----------|
| 11kV Overhead Lines | 50-100 MB | ~50,000 segments |
| 11kV Underground | 50-100 MB | ~50,000 segments |
| 11kV Substations | 5-10 MB | ~10,000 sites |
| 33kV Lines | 20-30 MB | ~5,000 segments |
| Distribution Subs | 5 MB | ~500 sites |
| **TOTAL** | **~200 MB** | **~115,000 features** |

---

## 🔧 After Download

### Convert to GeoJSON
```bash
cd data/official_sources/nged/

# Convert each shapefile to GeoJSON
ogr2ogr -f GeoJSON \
  ../../processed/nged-11kv-overhead.geojson \
  11kv_overhead_lines/11kv_overhead.shp

ogr2ogr -f GeoJSON \
  ../../processed/nged-11kv-underground.geojson \
  11kv_underground/11kv_underground.shp

ogr2ogr -f GeoJSON \
  ../../processed/nged-11kv-substations.geojson \
  11kv_substations/11kv_substations.shp
```

### Or use Python script
```bash
python scripts/convert_nged_shapefiles.py
```

---

## 📞 Contact for Help

If you encounter issues:

**Email**: nged.planningdata@nationalgrid.co.uk
**Subject**: "Open Data Request - 11kV Network Shapefiles"

**Request Template**:
```
Dear NGED Data Team,

I am building an open-source UK energy grid digital twin and would like
to download the following datasets from your open data portal:

- 11kV Overhead Lines (Shapefile)
- 11kV Underground Cables (Shapefile)
- 11kV Substations (Shapefile)
- 33kV Distribution Network (Shapefile)

I have visited connecteddata.nationalgrid.co.uk but the direct download
links redirect to dataportal2.westernpower.co.uk which I cannot access.

Could you please provide:
1. Direct download links, or
2. Access instructions for the dataportal2 site, or
3. Alternative methods to obtain this data

The data will be used for non-commercial research and visualization
purposes with full attribution to NGED.

Thank you for maintaining open data access.

Best regards,
[Your Name]
```

---

## ✅ Quick Win: Use Existing UKPN Data as Template

While waiting for NGED data, you can:

1. **Analyze UKPN structure** (we already have this)
2. **Create 11kV layer template** in frontend
3. **Test with UKPN 11kV data** (if available)
4. **Plug in NGED data** when downloaded

This way the infrastructure is ready when NGED data arrives!

---

## 🌐 Coverage Once Complete

**Before**: 25% UK (UKPN only)
- London, South East, East England
- 132kV, 66kV, 33kV

**After**: 55% UK (UKPN + NGED)
- + Midlands, South West, South Wales, West Midlands
- + 11kV street-level detail
- + ~115,000 more features

---

## 📚 Useful Links

- [NGED Connected Data Portal](https://connecteddata.nationalgrid.co.uk/)
- [NGED System & Network Data](https://connecteddata.nationalgrid.co.uk/group/system-and-network)
- [11kV Overhead Lines Dataset](https://connecteddata.nationalgrid.co.uk/dataset/11kv_ohl_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
- [11kV Underground Cables Dataset](https://connecteddata.nationalgrid.co.uk/dataset/11kv_ug_full_nged_area_4_dnos_in_esri_shapefile_shp_format)
- [11kV Substations Dataset](https://connecteddata.nationalgrid.co.uk/dataset/11kv-transformers)
- [Open Net Zero - NGED Datasets](https://opennetzero.org/western-power-distribution)

---

**Status**: Awaiting manual download from NGED portal
**Priority**: HIGH - This adds 30% more UK coverage
**Timeline**: 1-2 hours manual download + 1 hour processing

Let me know once you've downloaded the files and I'll process them immediately!
