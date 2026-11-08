# UI Design Plan - Dual Sidebar Interface
**Date**: 2024-11-07
**Status**: Planning Phase

---

## 🎯 Design Goals

1. **Left Sidebar**: Infrastructure layer selection with hierarchical controls
2. **Right Sidebar**: (To be defined - stats? details? filters?)
3. **Clean, professional interface** for energy grid visualization
4. **Hierarchical data organization** - infrastructure types → families → specific layers

---

## 📐 Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Top Bar (60px)                                             │
│  Logo | Stats | Controls                                    │
├──────────┬───────────────────────────────────┬──────────────┤
│          │                                   │              │
│   Left   │                                   │    Right     │
│  Sidebar │          MAP (full screen)        │   Sidebar    │
│  320px   │                                   │    280px     │
│          │                                   │   (optional) │
│  Layers  │                                   │              │
│  Control │                                   │              │
│          │                                   │              │
└──────────┴───────────────────────────────────┴──────────────┘
```

---

## 🗂️ Left Sidebar: Infrastructure Layer Control

### Primary Function
**Select and visualize different spatial datasets with hierarchical organization**

### Data Structure

```
Infrastructure Categories:
├── 🔌 Transmission Network
│   ├── 400kV Lines (gold)
│   ├── 275kV Lines (orange)
│   ├── 220kV Lines (red)
│   └── DC Interconnectors (purple)
│
├── ⚡ Distribution Network
│   ├── 132kV Lines (dark blue)
│   ├── 66kV Lines (medium blue)
│   ├── 33kV Lines (light blue)
│   ├── 11kV Lines (cyan) - coming soon
│   └── LV Network (gray) - coming soon
│
├── 🏭 Power Generation
│   ├── Wind Farms (1,227 sites, 13.6 GW)
│   ├── Solar Plants (580 sites, 12.6 GW)
│   ├── Natural Gas (166 plants, 20.3 GW)
│   ├── Nuclear (active plants)
│   ├── Hydro (105 sites, 1.5 GW)
│   ├── Biomass (304 sites, 3.8 GW)
│   ├── Battery Storage (178 sites, 9.7 GW)
│   └── Offshore Wind (26 farms, 2.9 GW)
│
├── 🏢 Substations
│   ├── Transmission Substations (395 sites)
│   ├── Primary Substations (195 South Wales)
│   ├── Distribution Substations (UKPN)
│   └── Grid Supply Points (GSP)
│
├── 🗺️ Network Boundaries
│   ├── GSP Regions
│   ├── DNO License Areas
│   │   ├── UKPN (London, SE, East)
│   │   ├── NGED South Wales
│   │   ├── SPEN Scotland & NW
│   │   ├── SSEN (coming soon)
│   │   ├── NPG (coming soon)
│   │   └── ENWL (coming soon)
│   └── Primary Substation Areas
│
└── 🏘️ Buildings & Demand
    ├── Building Footprints (29.5M) - processing
    ├── LV Feeders (coming soon)
    └── Demand Estimation (future)
```

---

## 🎨 Left Sidebar UI Components

### Header Section
```
┌─────────────────────────┐
│  INFRASTRUCTURE LAYERS  │ ← Section title
│  [🔍 Search layers...]  │ ← Search/filter box
└─────────────────────────┘
```

### Layer Category (Expandable/Collapsible)
```
┌─────────────────────────────────────┐
│ ▼ 🔌 Transmission Network           │ ← Category header (clickable)
│   ┌─────────────────────────────┐   │
│   │ ☑ 400kV Lines        1,212  │   │ ← Individual layer toggle
│   │   🟡 Gold • Visible  🔽     │   │    Color indicator • Status • Options
│   ├─────────────────────────────┤   │
│   │ ☑ 275kV Lines          847  │   │
│   │   🟠 Orange • Visible       │   │
│   ├─────────────────────────────┤   │
│   │ ☐ DC Links              25  │   │ ← Unchecked = hidden
│   │   🟣 Purple • Hidden        │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ▶ 🏭 Power Generation               │ ← Collapsed category
│   2,587 sites • 64.4 GW             │
└─────────────────────────────────────┘
```

### Layer Item Details
Each layer shows:
- ✅ **Checkbox**: Toggle visibility
- 🎨 **Color indicator**: Layer color
- 📊 **Feature count**: Number of items
- 👁️ **Visibility status**: Visible/Hidden
- ⚙️ **Options dropdown**: Style, opacity, zoom range

### Interaction Patterns

1. **Category Level**:
   - Click header → Expand/collapse children
   - Toggle icon (▶/▼) shows state
   - Show aggregate stats when collapsed

2. **Layer Level**:
   - Click checkbox → Show/hide layer
   - Click layer name → Zoom to extent
   - Click dropdown (🔽) → Advanced options
     - Adjust opacity (0-100%)
     - Set min/max zoom
     - Change color
     - Export data
     - View metadata

3. **Bulk Actions**:
   - "Show All" / "Hide All" buttons per category
   - "Transmission Only" / "Generation Only" presets
   - Save custom layer configurations

---

## 🎛️ Advanced Features

### Search & Filter
```
[🔍 Search layers...]
  └─ Fuzzy search across:
      - Layer names
      - Categories
      - Feature properties
      - Locations
```

### Layer Presets
```
📋 Quick Views:
├── Overview (all major infrastructure)
├── Transmission Only
├── Distribution Only
├── Generation Only
├── UKPN Area Only
└── Custom View 1, 2, 3...
```

### Layer Statistics (per category)
```
🔌 Transmission Network
   Total: 1,212 lines
   Length: 45,826 km
   Capacity: 400-275 kV
   Coverage: 100% UK
```

---

## 🔄 Right Sidebar: Options

### Option A: Data Details Panel
**Purpose**: Show detailed information about selected features

```
┌──────────────────────────┐
│  SELECTION DETAILS       │
├──────────────────────────┤
│  Selected: 400kV Line    │
│  ID: TL_0482            │
│  Voltage: 400kV         │
│  Length: 87.3 km        │
│  Operator: National Grid│
│  Route: Sundon - Pelham │
│                         │
│  [View Full Details]    │
│  [Export Data]          │
└──────────────────────────┘
```

### Option B: Network Statistics
**Purpose**: Real-time stats about visible data

```
┌──────────────────────────┐
│  NETWORK STATISTICS      │
├──────────────────────────┤
│  Visible Features: 3,421 │
│                         │
│  Transmission: 1,212    │
│  Distribution: 842      │
│  Generation: 1,367      │
│                         │
│  Total Capacity         │
│  ⚡ 64.4 GW             │
│                         │
│  Coverage: 35% UK       │
└──────────────────────────┘
```

### Option C: Analysis Tools
**Purpose**: Spatial analysis and queries

```
┌──────────────────────────┐
│  ANALYSIS TOOLS          │
├──────────────────────────┤
│  🎯 Find Nearest         │
│  📏 Measure Distance     │
│  📐 Calculate Area       │
│  🔍 Query by Location    │
│  📊 Generate Report      │
│  💾 Export Selection     │
└──────────────────────────┘
```

### Option D: Timeline/Temporal
**Purpose**: Show changes over time

```
┌──────────────────────────┐
│  TIMELINE               │
├──────────────────────────┤
│  Show data from:        │
│  ────●────────────      │
│  2020      2024         │
│                         │
│  📅 Historical Data     │
│  🔮 Planned Projects    │
│  📈 Growth Trends       │
└──────────────────────────┘
```

### Option E: No Right Sidebar (Recommended for MVP)
- Keep interface clean
- More map space
- Add right panel later when needed
- Use modals/popups for details instead

---

## 🎨 Visual Design Specifications

### Color Scheme (Dark Theme)
```css
Background:         #0a0e17 (dark blue-black)
Sidebar BG:         rgba(10, 14, 23, 0.85) + blur
Border:             rgba(255, 255, 255, 0.05)
Text Primary:       #e0e0e0 (light gray)
Text Secondary:     #999999 (medium gray)
Text Muted:         #666666 (dark gray)
Accent:             #667eea (purple-blue)
Success:            #10b981 (green)
Warning:            #f59e0b (amber)
```

### Typography
```
Header:      14px, 600 weight, uppercase, 1px letter-spacing
Category:    13px, 500 weight
Layer:       12px, 400 weight
Stats:       11px, 400 weight, monospace
```

### Spacing
```
Sidebar padding:    20px
Item padding:       12px 16px
Category margin:    16px bottom
Layer gap:          8px
Icon size:          16px
Color dot:          12px circle
```

### Animations
```
Expand/collapse:    200ms ease
Hover:              150ms ease
Toggle:             100ms ease
Sidebar slide:      300ms ease-out
```

---

## 🔧 Technical Implementation Notes

### State Management
```javascript
layerState = {
  transmission: {
    visible: true,
    expanded: true,
    layers: {
      '400kv': { visible: true, opacity: 0.85 },
      '275kv': { visible: true, opacity: 0.85 },
      '220kv': { visible: false, opacity: 0.85 },
      'dc': { visible: true, opacity: 0.85 }
    }
  },
  generation: {
    visible: true,
    expanded: false,
    layers: {
      'wind': { visible: true, opacity: 0.75 },
      'solar': { visible: true, opacity: 0.75 },
      // ...
    }
  },
  // ...
}
```

### Map Layer Control
```javascript
// When user toggles layer
function toggleLayer(category, layerId, visible) {
  const layerIds = getMapLayerIds(category, layerId);
  layerIds.forEach(id => {
    map.setLayoutProperty(id, 'visibility',
      visible ? 'visible' : 'none'
    );
  });
  updateLayerState(category, layerId, { visible });
}
```

### Performance Considerations
- Lazy load layer lists (virtualization for many items)
- Debounce search input (300ms)
- Cache layer visibility states in localStorage
- Use CSS transforms for smooth animations
- Minimize reflows during expand/collapse

---

## 📱 Responsive Behavior

### Desktop (> 1200px)
- Left sidebar: 320px fixed
- Right sidebar: 280px fixed (if used)
- Map: Remaining space

### Tablet (768px - 1200px)
- Left sidebar: 280px fixed
- Right sidebar: Hidden (use modals)
- Map: Remaining space

### Mobile (< 768px)
- Both sidebars: Slide-in drawers
- Map: Full screen
- Toggle button to open left drawer
- Bottom sheet for quick stats

---

## ✅ Implementation Phases

### Phase 1: Left Sidebar Structure (MVP)
1. Create sidebar container and styling
2. Implement category components (expandable)
3. Add layer toggles with checkboxes
4. Wire up to existing map layers
5. Add basic search functionality

### Phase 2: Enhanced Controls
1. Layer opacity sliders
2. Color pickers
3. Zoom range controls
4. Layer ordering (drag & drop)
5. Preset configurations

### Phase 3: Right Sidebar (Optional)
1. Choose right sidebar purpose
2. Implement selected features panel
3. Add statistics display
4. Create analysis tools UI

### Phase 4: Polish
1. Smooth animations
2. Keyboard shortcuts
3. Accessibility (ARIA labels)
4. Mobile responsive drawers
5. User preferences persistence

---

## 🎯 User Stories

1. **As a user**, I want to see all transmission lines, so I can understand the high-voltage network
   - Action: Click "Transmission Network" → Toggle all transmission sublayers

2. **As a user**, I want to compare wind farms to solar plants, so I can see generation distribution
   - Action: Expand "Power Generation" → Check Wind + Solar → Uncheck others

3. **As a user**, I want to hide everything except UKPN distribution, so I can focus on South East England
   - Action: Use "UKPN Only" preset OR manually hide other layers

4. **As a user**, I want to find all substations near London, so I can understand local infrastructure
   - Action: Search "London substations" → Zoom to results

5. **As a user**, I want to see what data covers my area, so I know what's available
   - Action: Check DNO boundaries → See coverage overlays

---

## 💡 Key Design Decisions

### Why Hierarchical Categories?
- ✅ Organizes 5,584 features logically
- ✅ Reduces visual clutter
- ✅ Matches mental model (transmission → distribution → generation)
- ✅ Scalable to 100K+ features with buildings

### Why Left Sidebar for Layers?
- ✅ Industry standard (QGIS, ArcGIS, Google Earth)
- ✅ Natural reading direction (left-to-right)
- ✅ Keeps important controls visible
- ✅ Doesn't interfere with Mapbox navigation (right)

### Why No Right Sidebar Initially?
- ✅ Maximizes map space
- ✅ Reduces complexity for MVP
- ✅ Can add later when needed
- ✅ Mobile-first approach

---

## 📊 Success Metrics

After implementation, measure:
- ⏱️ **Time to find specific layer**: < 5 seconds
- 🎯 **Clicks to toggle layer**: 1-2 clicks max
- 👁️ **Visible layers at once**: Support 20+ without lag
- 📱 **Mobile usability**: Drawer opens in < 300ms
- 💾 **State persistence**: Preferences saved correctly

---

## 🚀 Next Steps

1. **Review this plan** - Does it match your vision?
2. **Clarify right sidebar** - What should it show? Or skip for now?
3. **Prioritize features** - What's must-have vs nice-to-have?
4. **Begin Phase 1** - Implement left sidebar structure

---

**Question for you**:
1. Does this hierarchical structure match what you envisioned?
2. Should we skip the right sidebar for now, or do you have a specific use for it?
3. Any categories or layer types I'm missing?
4. Ready to start implementing, or want to adjust the plan first?
