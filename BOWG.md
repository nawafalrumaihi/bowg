# BOWG: Bahrain Open Weather Gateway

> Open-source weather data API contextualized to Bahrain and the Gulf.
> **Tagline:** *Open weather data for the Gulf, by the Gulf.*

---

## Status: Planning (May 2026)

---

## Why This Exists

- The Gulf is **data-poor** in global models. 0.25° GFS grid = ~25km. Bahrain is 50km across. Micro-climates invisible.
- No open portal exists. Commercial APIs gate historical data.
- Climate relevance is urgent — Gulf warming faster than global average.
- **Legacy project.** Outlives us. Scientists cite it. Students learn from it. Other Gulf states fork it.

---

## Data Sources

### Primary (Free/Open)
| Source | Type | Resolution | Update |
|--------|------|-----------|--------|
| GFS (NOAA) | Forecast | 0.25° | 6h |
| ERA5 (Copernicus CDS) | Reanalysis | 0.25° | Monthly (2-month lag) |
| MERRA-2 (NASA) | Reanalysis + Aerosol | 0.5° x 0.625° | Monthly |
| IMERG (GPM) | Precipitation | 0.1° | 30min |
| AERONET | Aerosol Optical Depth | Point (Bahrain station!) | Daily |

### Bahrain-Specific (Needs Investigation)
- Bahrain Meteorological Service — local observations
- Bahrain Air Quality Monitoring — PM2.5, PM10, O3
- University of Bahrain — research stations
- Regional dust storm reports — manual curation

### Derived Products (We Compute)
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

Full blueprint: see original spec at root `Bahrain-Open-Weather-Gateway.md` (migrate here over time).

---

## Tech Stack

| Layer | Tech | Why |
|-------|------|-----|
| Ingestion | Python + cron | Simple start, scale to Airflow |
| Processing | xarray, netCDF4, scipy | Geospatial standard |
| Storage | Zarr + TimescaleDB + Parquet | Multi-dimensional + fast time queries + archive |
| Cache | Redis | API response caching, rate limiting |
| API | FastAPI + Pydantic | Async, typed, auto-docs |
| Viz | Deck.gl / Mapbox GL JS | WebGL, performant |
| Infra | Docker Compose → K8s | Portable, reproducible |
| CI/CD | GitHub Actions | Open-source friendly |
| Monitoring | Prometheus + Grafana | Standard observability |

---

## Next Milestone

**Architecture freeze + first data pipeline**
- Lock API schema v1
- Implement ERA5 ingestion pipeline (simplest to start)
- Deploy ingest → process → store on local machine
- Validate output against known data points

---

## Links

- [[Bahrain-Open-Weather-Gateway|Original full blueprint (root)]]
- [[../notes/weather-data-sources]] (create when researched)
- [[../ideas/why-bahrain-needs-its-own-weather-api]] (create when synthesized)

---

*Project note created: 2026-05-12*
