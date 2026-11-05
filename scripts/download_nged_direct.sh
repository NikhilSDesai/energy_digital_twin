#!/bin/bash

# ============================================================================
# NGED Direct Download Helper
# ============================================================================
# Since NGED API requires authentication, this script provides direct
# download URLs you can use while logged into the portal
# ============================================================================

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                    NGED SPATIAL DATASETS - DOWNLOAD GUIDE                  ║
╚════════════════════════════════════════════════════════════════════════════╝

The NGED API requires browser authentication. Here are your options:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION 1: Direct Browser Download (Recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

While logged into https://connecteddata.nationalgrid.co.uk, visit these URLs:

1. 132kV Overhead Lines:
   https://connecteddata.nationalgrid.co.uk/dataset/spatial-datasets

   → Search for "132" or "132kV overhead"
   → Click "Explore" on the dataset
   → Click download button
   → Save as: data/dno/nged/raw/132kv_ohl_nged.gpkg

2. 66kV Overhead Lines:
   → Search for "66" or "66kV overhead"
   → Click "Explore" → Download
   → Save as: data/dno/nged/raw/66kv_ohl_nged.gpkg

3. 33kV Overhead Lines:
   → Search for "33" or "33kV overhead"
   → Click "Explore" → Download
   → Save as: data/dno/nged/raw/33kv_ohl_nged.gpkg

4. Primary Substations:
   → Search for "primary substation"
   → Click "Explore" → Download
   → Save as: data/dno/nged/raw/primary_substations_nged.gpkg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION 2: Browser Session Export (Advanced)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you want to use curl/wget with your browser session:

1. In your browser (Chrome/Firefox), open Developer Tools (F12)
2. Go to Network tab
3. Visit: https://connecteddata.nationalgrid.co.uk/dataset/spatial-datasets
4. Find a request in Network tab
5. Right-click → Copy → Copy as cURL
6. Extract the Cookie header
7. Use it with curl:

   curl -H "Cookie: YOUR_COOKIE_HERE" \
        "https://connecteddata.nationalgrid.co.uk/dataset/spatial-datasets/datapackage.json" \
        -o nged_datapackage.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION 3: Alternative Data Source
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NGED also provides data via a secondary portal:

   https://dataportal2.nationalgrid.co.uk/

This may have different authentication requirements.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AFTER DOWNLOADING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Once you have all 4 files in data/dno/nged/raw/, run:

   python3 scripts/convert_dno_shapefiles.py

This will convert the .gpkg files to GeoJSON and save to frontend/public/data/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

# Create directory
mkdir -p data/dno/nged/raw

echo ""
echo "✅ Created directory: data/dno/nged/raw"
echo ""
echo "📥 Ready to receive NGED downloads!"
echo ""
