#!/bin/bash

echo "============================================"
echo "UK Energy Digital Twin - Starting Frontend"
echo "============================================"
echo ""

# Check if Mapbox token is set
if grep -q "YOUR_MAPBOX_TOKEN_HERE" frontend/public/app.js; then
    echo "⚠️  WARNING: Mapbox token not set!"
    echo ""
    echo "To get your free Mapbox token:"
    echo "1. Go to https://account.mapbox.com/"
    echo "2. Sign up (free tier: 50k loads/month)"
    echo "3. Copy your default public token"
    echo "4. Edit frontend/public/app.js and replace YOUR_MAPBOX_TOKEN_HERE"
    echo ""
    echo "Press Enter to continue anyway (map won't load without token)..."
    read
fi

echo "Starting local server on http://localhost:8000"
echo ""
echo "✓ Open http://localhost:8000 in your browser"
echo ""
echo "Keyboard shortcuts:"
echo "  H - Toggle header"
echo "  L - Toggle legend  "
echo "  R - Reset view"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd frontend/public
python3 -m http.server 8000
