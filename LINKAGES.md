# BOWG Linkages & Cross-Project Connections

*Auto-generated: 2026-05-22. Add manual linkages here as projects evolve.*

## Within BOWG

[[README|Phases]] → [[BOWG|Current Spec]] → [[BOWG-Summary|Full Context]] → [[DECISIONS|Locked Design]] → [[LOG|Next Steps]]

**Also:** [[CLAUDE.md|AI Conventions]] · [[BOWG-Study-Roadmap|Research Foundations]] · `research/` folder

## Cross-Project Linkages

### Malaeb → BOWG
- **Data layer convergence**: Malaeb's forecast pipeline (EOM, MAPE forecasting) could consume BOWG derived products (Heat Index, Dust Storm Probability)
- **Timeline**: BOWG ships Q4 2026. Malaeb pricing engine needs historical weather patterns. Could integrate after BOWG stabilizes.
- **Contact point**: `~/Documents/Ideas/Projects/Malaeb/` — see Cube.js semantic layer design

### Reef → BOWG
- **Community context**: Reef is Nawaf's community app. Weather data could enhance community features (outdoor event planning, air quality alerts)
- **Integration**: Post-launch. BOWG API becomes a service dependency for Reef's backend.

### Reflective Journaling LLM → BOWG
- **Not directly connected** — separate domain. But BOWG's infrastructure patterns (async pipelines, multi-source data fusion) could inform journaling LLM's architecture.

## Vault Interconnections

### Notes
- Create `~/Documents/Ideas/notes/weather-data-sources.md` — deep dive on each data source (accessibility, format, licensing)
- Create `~/Documents/Ideas/notes/geospatial-data-formats.md` — Zarr vs NetCDF vs GeoTIFF comparison
- Reference existing: `~/Documents/Ideas/notes/malaeb/` for forecast patterns

### Ideas
- Create `~/Documents/Ideas/ideas/why-bahrain-needs-its-own-weather-api.md` — vision doc (philosophy, use cases)
- Create `~/Documents/Ideas/ideas/climate-urgency-gulf.md` — context on why Gulf weather matters

### Knowledge
- Grandfathered: `~/Documents/Ideas/Knowledge/nawaf-context.md` — update if BOWG role changes
- Could add: Gulf climate crisis literature summary

## Timeline for Linkages

- **Now (May 2026)**: BOWG architecture freeze
- **June 2026**: Bahrain data source verification (moat research)
- **Q3 2026**: Phase 1 ERA5 POC + API v1
- **Q4 2026**: BOWG ships. Can then link Malaeb/Reef as consumers.

---

*Last updated: 2026-05-22 by Hermes*
