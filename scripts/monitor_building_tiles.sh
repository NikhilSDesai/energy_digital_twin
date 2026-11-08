#!/bin/bash
# Monitor building tile creation progress

echo "======================================================================"
echo "BUILDING TILE CREATION MONITOR"
echo "======================================================================"
echo ""
echo "Input: 29.5M buildings, 18 GB GeoJSON"
echo "Output: data/processed/buildings_optimized/uk_buildings.mbtiles"
echo "Expected time: 1-2 hours"
echo ""
echo "======================================================================"
echo "CURRENT PROGRESS"
echo "======================================================================"
echo ""

# Show latest output from tippecanoe
tail -30 /private/tmp/claude-501/-Users-nikhildesai-Documents-03-Personal-energy-dt/tasks/b247227.output

echo ""
echo "======================================================================"
echo "To monitor in real-time, run:"
echo "  tail -f /private/tmp/claude-501/-Users-nikhildesai-Documents-03-Personal-energy-dt/tasks/b247227.output"
echo ""
echo "To check output file size:"
echo "  ls -lh data/processed/buildings_optimized/uk_buildings.mbtiles"
echo "======================================================================"
