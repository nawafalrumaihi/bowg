# Project: Bahrain Open Weather Gateway (BOWG)

## Status: Planning (May 2026)

## Vision
An open-source weather data API gateway contextualized to Bahrain and the Gulf. Ingest global datasets, normalize, enrich with local context, and serve through clean APIs — free for scientists, students, and tinkerers. Build the infrastructure that should already exist but doesn't.

**Tagline:** *Open weather data for the Gulf, by the Gulf.*

## Why This Matters

- **The Gulf is data-poor.** Global models (GFS, ERA5) use 0.25° grids — that's ~25km. Bahrain is 50km across. You get maybe 4-6 grid points covering the entire country. Micro-climates, coastal effects, dust corridors — all invisible.
- **No open portal exists.** Commercial APIs (OpenWeatherMap, WeatherAPI) gate historical data behind paywalls. Researchers hit rate limits or can't afford bulk access.
- **Climate relevance is urgent.** The Gulf is warming faster than global average. Bahrain-specific longitudinal data is critical for researchers studying heat stress, dust storms, sea-level rise, and urban heat islands.
- **Legacy project.** This outlives you. Scientists could cite it. Students could learn from it. Other Gulf states could fork it.

## Data Sources (All Free/Open)

### Primary Ingestion
| Source | Type | Resolution | Update Frequency | Coverage |
|--------|------|-----------|-----------------|----------|
| **GFS** (NOAA) | Forecast | 0.25° | 6h | Global |
| **ERA5** (Copernicus CDS) | Reanalysis | 0.25° | Monthly (2-month lag) | Historical to 1950 |
| **MERRA-2** (NASA GES DISC) | Reanalysis + Aerosol | 0.5° x 0.625° | Monthly | 1980-present |
| **IMERG** (GPM) | Precipitation | 0.1° | 30min | Near real-time |
| **AERONET** | Aerosol Optical Depth | Point (Bahrain station!) | Daily | Varies |

### Bahrain-Specific (Needs Investigation)
| Source | Type | Access |
|--------|------|--------|
| **Bahrain Meteorological Service** | Local observations | Unknown — investigate API/scraping |
| **Bahrain Air Quality Monitoring** | PM2.5, PM10, O3 | Unknown — investigate |
| **University of Bahrain** | Research stations | Academic outreach |
| **Regional dust storm reports** | Event data | Manual curation |

### Derived Products (We Compute)
- **Heat Index** (temperature + humidity — critical for Bahrain summers)
- **Dewpoint Discomfort Score** (how oppressive it *feels*)
- **Dust Storm Probability Index** (MERRA-2 aerosol + wind + visibility)
- **Solar Irradiance** (for renewable energy research)
- **Urban Heat Island Delta** (modeled vs observed, when local data available)
- **Sea Surface Temperature** (Gulf waters drive humidity + cyclone risk)
- **Wet Bulb Globe Temperature** (occupational health standard — construction workers)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   BOWG SYSTEM                       │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌───────────┐     │
│  │ INGEST   │───▶│ PROCESS  │───▶│  STORE    │     │
│  │          │    │          │    │           │     │
│  │ GFS      │    │ xarray   │    │ Zarr      │     │
│  │ ERA5     │    │ netCDF4  │    │ Parquet   │     │
│  │ MERRA-2  │    │ derive   │    │ TimescaleDB│    │
│  │ IMERG    │    │ resample │    │ Redis     │     │
│  │ AERONET  │    │ validate │    │           │     │
│  └──────────┘    └──────────┘    └─────┬─────┘     │
│                                        │            │
│  ┌──────────┐    ┌──────────┐          │            │
│  │   VIZ    │◀───│   API    │◀─────────┘            │
│  │          │    │          │                       │
│  │ Deck.gl  │    │ FastAPI  │                       │
│  │ Mapbox   │    │ REST     │                       │
│  │ WebGL    │    │ WebSocket│                       │
│  │ Static   │    │ GraphQL? │                       │
│  └──────────┘    └──────────┘                       │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │              SHARED INFRA                    │   │
│  │  Docker · Monitoring · Auth (API keys)       │   │
│  │  Rate Limiting · Logging · CI/CD             │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Ingestion** | Python + cron (→ Airflow later) | Simple start, scale when needed |
| **Processing** | xarray, netCDF4, scipy | Industry standard for geospatial |
| **Storage** | Zarr (gridded), TimescaleDB (time-series), Parquet (archive) | Zarr for multi-dim, TimescaleDB for fast time queries |
| **Cache** | Redis | API response caching, rate limiting |
| **API** | FastAPI + Pydantic | Async, typed, auto-docs (Swagger) |
| **Viz** | Deck.gl / Mapbox GL JS | WebGL, performant, Earth Nullschool vibe |
| **Infra** | Docker Compose → K8s later | Portable, reproducible |
| **CI/CD** | GitHub Actions | Open-source friendly |
| **Monitoring** | Prometheus + Grafana | Standard observability |

## API Design (Draft)

### Base URL
```
https://api.bowg.dev/v1/
```

### Endpoints (Examples)
```
# Current conditions
GET /current?lat=26.23&lon=50.58
GET /current?city=manama

# Forecast
GET /forecast?lat=26.23&lon=50.58&hours=48
GET /forecast/dust-probability?lat=26.23&lon=50.58

# Historical
GET /historical?lat=26.23&lon=50.58&start=2019-07-15&end=2019-07-16
GET /historical/heat-index?city=manama&year=2023

# Derived products
GET /derived/heat-index?lat=26.23&lon=50.58
GET /derived/dust-storm-probability?bbox=25.5,50.0,26.5,51.0
GET /derived/solar-irradiance?lat=26.23&lon=50.58

# Gridded data (for researchers — returns netCDF/Zarr subset)
GET /gridded/gfs?variable=temp,humidity&bbox=25.5,50.0,26.5,51.0
GET /gridded/era5?variable=temp&level=surface&time=2019-07-15T14:00

# Station data
GET /stations/aeronet/bahrain
GET /stations/list

# Meta
GET /sources          # List available data sources and their coverage
GET /variables        # List all available variables with units and descriptions
GET /status           # System status, last update times
```

### Response Format
```json
{
  "location": {"lat": 26.23, "lon": 50.58, "city": "Manama"},
  "source": "GFS",
  "valid_time": "2026-05-04T02:00:00+03:00",
  "variables": {
    "temperature_2m": {"value": 33.2, "unit": "°C"},
    "relative_humidity": {"value": 72, "unit": "%"},
    "heat_index": {"value": 41.8, "unit": "°C"},
    "dust_storm_probability": {"value": 0.15, "unit": "fraction"},
    "wind_speed_10m": {"value": 12.4, "unit": "km/h"},
    "wind_direction_10m": {"value": 310, "unit": "°"}
  },
  "derived": {
    "dewpoint_discomfort": {"value": "severe", "scale": "moderate|severe|extreme"},
    "wbgt": {"value": 32.1, "unit": "°C", "risk": "high"}
  }
}
```

## Local LLM Delegation Strategy

This project will use local models for token-intensive tasks, keeping external API calls minimal.

| Task | Model | Why |
|------|-------|-----|
| **Code generation** (ingestion scripts, API endpoints) | gemma4 (local) | Good enough for boilerplate, saves tokens |
| **Code review** | qwen3:14b (local) | Better reasoning for catching bugs |
| **Documentation writing** | mistral-nemo:12b (local) | Journal model doubles as doc writer |
| **Data validation logic** | qwen3:14b (local) | Needs structured reasoning |
| **Complex debugging** | GLM-5.1 (Z.AI) | When local models can't crack it |
| **Architecture decisions** | GLM-5.1 (Z.AI) | Needs deep reasoning — worth the tokens |
| **Research (paper reading)** | gemma4 (local) | Summarize papers, extract data specs |

**Rule of thumb:** If it's generation/reformatting/summarization → local. If it's reasoning/architecture/debugging → main model.

## Phases

### Phase 0: Foundation (Week 1-2)
- [ ] Set up project repo (GitHub, MIT license)
- [ ] Docker Compose dev environment
- [ ] Register CDS API key (ERA5 access)
- [ ] Register NASA Earthdata login (MERRA-2, GFS)
- [ ] Test data download scripts for each source
- [ ] Define Bahrain bbox: approximately `25.5°N, 50.0°E` to `26.5°N, 51.0°E`
- [ ] First successful GFS subset download

### Phase 1: Ingestion Pipeline (Week 3-4)
- [ ] GFS ingestion script (automated, 6h cycle)
- [ ] ERA5 historical backfill (1950-present for Bahrain bbox)
- [ ] MERRA-2 aerosol data ingestion
- [ ] IMERG precipitation ingestion
- [ ] AERONET Bahrain station data
- [ ] Data validation checks (range, missing, units)
- [ ] Storage: Zarr for gridded, Parquet for tabular
- [ ] Ingestion monitoring (last update, data freshness)

### Phase 2: Processing & Derived Products (Week 5-6)
- [ ] Heat index computation
- [ ] Dewpoint discomfort scoring
- [ ] Dust storm probability model (MERRA-2 aerosol + wind)
- [ ] Solar irradiance estimation
- [ ] Wet Bulb Globe Temperature
- [ ] Time-series aggregation (hourly → daily → monthly)
- [ ] Store derived products alongside raw data

### Phase 3: API (Week 7-8)
- [ ] FastAPI project structure
- [ ] /current endpoint
- [ ] /forecast endpoint
- [ ] /historical endpoint with time range queries
- [ ] /derived endpoints for computed products
- [ ] /gridded endpoints for raw data access
- [ ] Redis caching layer
- [ ] API key authentication (simple, free tier)
- [ ] Rate limiting
- [ ] Swagger docs (auto-generated)

### Phase 4: Visualization (Week 9-10)
- [ ] Interactive map (Mapbox or Deck.gl)
- [ ] Wind flow visualization (Earth Nullschool style)
- [ ] Temperature/heat index overlay
- [ ] Dust aerosol visualization
- [ ] Historical animation (time slider)
- [ ] Static map generation for sharing

### Phase 5: Open Source & Community (Week 11-12)
- [ ] Documentation site (MkDocs or Docusaurus)
- [ ] Contributor guide
- [ ] API examples in Python, curl, JavaScript
- [ ] Publish on academic channels (Bahrain researchers, Gulf studies)
- [ ] Submit to open data registries
- [ ] Blog post / write-up explaining the gap this fills

## Economics (To Be Developed)

Nawaf is working on proper economics. Key questions:

- **Compute costs:** Local machine handles ingestion + processing. VPS for API serving (~$10-20/mo for a small DigitalOcean/Hetzner instance)
- **Storage costs:** ERA5 backfill for Bahrain bbox ≈ 50-100GB compressed. GFS rolling ≈ 5GB/month. Affordable on local disk.
- **Bandwidth:** API serving — start free tier, scale with usage
- **API key tiers:** Free (researchers/students), Paid (commercial), Enterprise (SLA)
- **Grants:** Possible funding from Bahrain's Supreme Council for the Environment, UoB research grants, GCC climate research programs
- **Token costs:** Heavy use of local LLMs minimizes this. Main model only for complex tasks.

## Domain: bowg.dev (available as of planning)

## License
MIT — maximum openness, minimum friction. Data should be CC-BY or CC0 where source licenses permit.

## GCP ML Certification Alignment
- Data pipeline (Dataflow / Apache Beam for processing at scale)
- Cloud Storage for data lake
- Vertex AI for any ML-based products (e.g., dust storm prediction model)
- Cloud Run for API serving
- BigQuery for analytical queries on historical data
- Monitoring and observability

## North Star
*A 19-year-old student at UoB can curl the API and get heat index data for their neighborhood. A climate researcher at MIT can download 40 years of dust aerosol data for the Gulf. A developer in Dubai can fork it for UAE.*

**This is infrastructure. It should be boring, reliable, and always there.**
