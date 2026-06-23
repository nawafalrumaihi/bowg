# BOWG: Bahrain Open Weather Gateway — Project Summary

**Status:** Planning (May 2026)  
**Next Milestone:** Architecture freeze + first ERA5 data pipeline  
**Timeline Goal:** Ship as legacy-grade, open-source infrastructure for Gulf climate data

---

## Why This Exists

The Gulf region is **data-poor** in global climate models:
- GFS grid resolution: 0.25° (~25km) — Bahrain is only 50km across, so micro-climates are invisible
- No open portal for historical weather data — commercial APIs gate access
- Climate urgency: Gulf warming faster than global average
- **Philosophy:** Build infrastructure that outlives us. Scientists cite it. Students learn from it. Other Gulf states can fork it.

---

## Data Sources

### Primary (Free/Open)
| Source | Type | Resolution | Update Frequency |
|--------|------|-----------|------------------|
| GFS (NOAA) | Forecast | 0.25° | 6 hours |
| ERA5 (Copernicus CDS) | Reanalysis | 0.25° | Monthly (2-month lag) |
| MERRA-2 (NASA) | Reanalysis + Aerosol | 0.5° x 0.625° | Monthly |
| IMERG (GPM) | Precipitation | 0.1° | 30 minutes |
| AERONET | Aerosol Optical Depth | Point (Bahrain station exists!) | Daily |

### Bahrain-Specific (Investigation Needed)
- Bahrain Meteorological Service — local observations
- Bahrain Air Quality Monitoring — PM2.5, PM10, O3
- University of Bahrain — research stations
- Regional dust storm reports — manual curation

### Derived Products (Computed)
- Heat Index
- Dewpoint Discomfort Score
- Dust Storm Probability Index
- Solar Irradiance
- Urban Heat Island Delta
- Sea Surface Temperature
- Wet Bulb Globe Temperature (WBGT)

---

## Architecture

```
INGEST (Python + cron → Airflow)
  ├─ GFS, ERA5, MERRA-2, IMERG, AERONET
  ↓
PROCESS (xarray, netCDF4, scipy)
  ├─ Derive, resample, validate
  ↓
STORE
  ├─ Zarr (gridded)
  ├─ TimescaleDB (time-series)
  ├─ Parquet (archive)
  └─ Redis (cache)
  ↓
API (FastAPI + Pydantic)
  └─ REST / WebSocket / GraphQL?
  ↓
VIZ (Deck.gl / Mapbox GL JS)
  └─ Earth Nullschool vibe
```

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Ingestion** | Python + cron | Simple start, scales to Airflow later |
| **Processing** | xarray, netCDF4, scipy | Geospatial standard. Multi-dimensional arrays. |
| **Storage** | Zarr + TimescaleDB + Parquet | Zarr = gridded data, TimescaleDB = fast time queries, Parquet = archive |
| **Cache** | Redis | API response caching, rate limiting |
| **API** | FastAPI + Pydantic | Async, typed, auto-generated docs. Lean. |
| **Visualization** | Deck.gl / Mapbox GL JS | WebGL, performant. Earth Nullschool aesthetic. |
| **Infrastructure** | Docker Compose → Kubernetes | Portable, reproducible. Easy to fork. |
| **CI/CD** | GitHub Actions | Open-source native |
| **Monitoring** | Prometheus + Grafana | Standard observability stack |

---

## Design Decisions (Locked)

- **Resolution:** Start with 0.25° globally (ERA5 native), downscale/interpolate for Bahrain micro-climates later
- **Historical depth:** ERA5 goes back to 1943 — full reanalysis available
- **Real-time vs. historical:** Separate pipelines (GFS = forecast bucket, ERA5 = archive bucket)
- **Data format:** Zarr for gridded (CF-compliant), Parquet for tabular time-series
- **Derived products:** Compute on-demand or cache? Start with cache (Redis), measure query patterns, optimize
- **Visualization:** Web-first (Mapbox GL JS), mobile-responsive

---

## Open Questions (For Architecture Freeze)

1. **API Schema:**
   - Query method? (lat/lon bounding box, point, grid?)
   - Time ranges? (recent, full history, forecast horizon?)
   - What fields in response? (all sources, or user-specified?)
   - Rate limiting strategy?

2. **Storage Trade-offs:**
   - Zarr pros: multi-dimensional, CF-compliant, cloud-native. Cons: new format, smaller ecosystem.
   - TimescaleDB pros: SQL, time queries fast. Cons: separate infrastructure.
   - Decision: Start with Zarr for gridded data (ERA5), TimescaleDB for point observations (AERONET)?

3. **Infra Deployment:**
   - Docker Compose locally, GitHub Actions for CI, then what? VPS? Cloud? Self-hosted?
   - Data volume: How much disk for full ERA5 1943–2026? (Estimate: ~500GB uncompressed, ~50GB Zarr-compressed)

4. **Validation & QA:**
   - Baseline metrics? (Compare gridded ERA5 against AERONET point obs?)
   - Automated checks? (Data freshness, pipeline health, anomaly detection?)

---

## First Sprint: ERA5 Ingestion Pipeline

**Goal:** Get data from Copernicus CDS into local Zarr store, validate against a known point.

### Tasks
1. **Copernicus CDS Setup**
   - Create account at https://cds.climate.copernicus.eu/
   - Generate API key
   - Document auth flow

2. **ERA5 Data Fetch**
   - Use `cdsapi` Python client
   - Fetch 1 month of 2m temperature + 10m wind for Bahrain area (24°–27°N, 49°–52°E)
   - Save as NetCDF

3. **Process & Store**
   - Load NetCDF with xarray
   - Resample to uniform grid (0.25°)
   - Save to Zarr format
   - Validate: Check values against known weather points (AERONET if available)

4. **API Endpoint**
   - FastAPI route to query Zarr by lat/lon and date
   - Return JSON (temperature, wind, metadata)

5. **Validation**
   - Spot-check output vs. ERA5 ECMWF plots
   - Compare AERONET retrievals if available

---

## Key Links & References

- **Full original blueprint:** `~/Documents/Ideas/Bahrain-Open-Weather-Gateway.md` (to migrate here)
- **Data source exploration:** Create `~/Documents/Ideas/notes/weather-data-sources.md`
- **Philosophy & vision:** Create `~/Documents/Ideas/ideas/why-bahrain-needs-its-own-weather-api.md`

---

## Aligned Goals (From Nawaf's 2026 Roadmap)

> Ships BOWG — Bahrain Open Weather Gateway. Open-source, legacy-grade infrastructure for Gulf climate data.

By shipping BOWG, Nawaf achieves:
- Infrastructure that outlives any one person or company
- Contribution to Gulf climate science and education
- Proof of full-stack geospatial data engineering
- Foundation for future (e.g., integrating into Reef community app)

---

## Immediate Next Steps

**For Claude (your higher-limit subscription):**
1. Flesh out API schema — what queries matter most?
2. Design Zarr structure — how to organize multi-source, multi-temporal data?
3. Plan storage layer — Zarr + TimescaleDB split, or all-in on one?
4. Write storage layer POC — demonstrate Zarr write/read locally

---

*Last updated: 2026-05-22 by Hermes*  
*Saved to: ~/Desktop/BOWG-Summary.md*
