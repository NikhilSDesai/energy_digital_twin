#!/bin/bash

# ============================================================================
# UK DNO Distribution Network Data - Master Processing Script
# ============================================================================
# This script runs all 4 steps in sequence to process DNO data
# Run this after manually downloading NGED, NPG, SSEN, SPEN, ENWL data
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${BOLD}============================================================================${NC}"
echo -e "${BOLD}UK DNO Distribution Network Data - Master Processing Script${NC}"
echo -e "${BOLD}============================================================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.${NC}"
    exit 1
fi

# Check if required packages are installed
echo -e "${BLUE}ℹ️  Checking Python dependencies...${NC}"
python3 -c "import geopandas, shapely, requests, tqdm" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Missing required Python packages.${NC}"
    echo -e "${BLUE}Installing: geopandas shapely requests tqdm${NC}"
    pip3 install geopandas shapely requests tqdm
}
echo -e "${GREEN}✅ Python dependencies OK${NC}"
echo ""

# Step 1: Download UKPN data
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}STEP 1/4: Download DNO Data${NC}"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 scripts/download_all_dno_network_data.py

echo ""
echo -e "${YELLOW}⚠️  MANUAL ACTION REQUIRED:${NC}"
echo -e "Before continuing, download data from NGED, NPG, SSEN, SPEN, ENWL portals"
echo -e "Follow the instructions above and save files to data/dno/*/raw/"
echo ""
echo -e "Check progress: ${BOLD}data/dno/DOWNLOAD_CHECKLIST.md${NC}"
echo ""
read -p "Have you downloaded all DNO data? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Exiting. Run this script again after downloading DNO data.${NC}"
    exit 0
fi

# Step 2: Convert shapefiles to GeoJSON
echo ""
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}STEP 2/4: Convert Shapefiles to GeoJSON${NC}"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 scripts/convert_dno_shapefiles.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Conversion failed. Check errors above.${NC}"
    exit 1
fi

# Step 3: Standardize properties
echo ""
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}STEP 3/4: Standardize Property Schemas${NC}"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 scripts/standardize_dno_properties.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Standardization failed. Check errors above.${NC}"
    exit 1
fi

# Step 4: Combine all DNO data
echo ""
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}STEP 4/4: Combine All DNO Data${NC}"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 scripts/combine_dno_data.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Combination failed. Check errors above.${NC}"
    exit 1
fi

# Success summary
echo ""
echo -e "${BOLD}${GREEN}============================================================================${NC}"
echo -e "${BOLD}${GREEN}✅ SUCCESS! DNO DATA PROCESSING COMPLETE${NC}"
echo -e "${BOLD}${GREEN}============================================================================${NC}"
echo ""

# Show combined file stats
echo -e "${BOLD}Combined Files:${NC}"
ls -lh frontend/public/data/all-dnos-*.geojson 2>/dev/null | awk '{printf "  %-45s %6s\n", $9, $5}'

echo ""
echo -e "${BOLD}Reports:${NC}"
echo -e "  Conversion: data/dno/conversion_report.json"
echo -e "  Combination: frontend/public/data/combination_report.json"
echo ""

# Next steps
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}NEXT STEPS:${NC}"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "1. Update ${BOLD}frontend/public/app.js${NC}"
echo -e "   See: scripts/app_js_updated_code.js"
echo ""
echo -e "2. Update ${BOLD}frontend/public/index.html${NC}"
echo -e "   Update bottom-info panel with all DNO coverage"
echo ""
echo -e "3. Test locally:"
echo -e "   cd frontend/public && python3 -m http.server 8000"
echo ""
echo -e "4. Deploy:"
echo -e "   git add . && git commit -m 'Add complete UK DNO coverage' && git push"
echo ""
echo -e "${GREEN}✅ You now have 100% UK distribution network coverage!${NC}"
echo ""
