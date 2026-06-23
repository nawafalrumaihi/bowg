# BOWG Climatology Study Roadmap

> **Source:** Climatology (4th Edition) — Rohli & Vega + BOWG domain mapping
> **Created:** 2026-05-12
> **Purpose:** Structured learning path focused on GCC meteorology needs for building BOWG

---

## Background

Nawaf owns **Climatology (4th Edition)** by Robert V. Rohli & Anthony J. Vega. This roadmap maps textbook topics to BOWG's GCC-specific weather intelligence needs. The goal is to learn *why* weather happens in the Gulf so we can build better data products and derived metrics.

**Study approach:** Don't read linearly. Jump to the chapters below in priority order. Use the rest as reference when BOWG data raises questions.

---

## Priority 1: Atmospheric Dynamics & Circulation 🌍

### What to Study
- **General circulation patterns**
  - Hadley cells, Ferrel cells, Polar cells
  - Jet streams and their seasonal migration
  - How global circulation affects the Gulf region

- **Shamal winds** ⭐ *The regional weather driver*
  - NW wind system across Bahrain/Saudi/Iraq
  - Summer vs winter Shamal regimes
  - Dust storm generation and transport

- **Monsoon influence**
  - Indian/Asian monsoon effects on Gulf humidity
  - Cloud cover and precipitation during monsoon months

- **Pressure systems**
  - Siberian High (winter cold fronts)
  - Thermal lows (summer heat domes)
  - Bermuda-Azores High influence

### BOWG Application
- Predict wind direction/speed patterns
- Model dust storm probability
- Understand temperature anomaly sources

### Derived Products Needed
- Wind anomaly detection
- Dust storm probability index
- Pressure system classification

---

## Priority 2: Heat & Energy Balance 🔥

### What to Study
- **Sensible vs latent heat transfer**
  - Why Bahrain feels hotter than the thermometer says
  - Energy balance at surface-atmosphere interface

- **Wet Bulb Globe Temperature (WBGT)** ⭐ *Critical for GCC*
  - Calculation methodology
  - Human survivability thresholds
  - Why this matters more than dry temp in the Gulf

- **Solar irradiance**
  - Incoming shortwave radiation
  - Albedo effects (desert vs urban vs water)
  - **Dust attenuation on solar radiation** — critical for solar forecasting

- **Urban Heat Island effect**
  - Bahrain's urbanization amplifies heat
  - Nighttime temperature minimums

### BOWG Application
- Compute accurate heat stress indices
- Solar energy forecasting (solar irradiance is in BOWG pipeline)
- Urban planning heat maps

### Derived Products Needed
- WBGT calculator
- Heat Index (multiple formulations)
- Solar irradiance forecast
- Urban heat island analysis

---

## Priority 3: Humidity & Moisture 💧

### What to Study
- **Dew point dynamics** ⭐ *The Gulf's defining challenge*
  - Why Gulf summer is brutal (high dew point + high temp)
  - Dew point tracking vs relative humidity

- **Evaporative cooling limits**
  - Wet bulb temperature calculations
  - 35°C wet bulb = human survivability threshold
  - When does Bahrain approach this?

- **Sea Breeze circulation**
  - Bahrain's daily coastal wind patterns
  - Temperature moderation effects
  - Interaction with regional wind systems

- **Fog formation**
  - Winter/spring coastal fog
  - Radiation fog vs advection fog
  - Aviation and transportation impacts

### BOWG Application
- Humidity stress metrics
- Fog prediction for aviation
- Coastal breeze forecasting

### Derived Products Needed
- Dew point tracker
- Wet bulb temperature calculator
- Sea breeze detection
- Fog probability index

---

## Priority 4: Dust & Aerosols 🌫️

### What to Study
- **Aerosol Optical Depth (AOD)** ⭐ *Already in BOWG pipeline via AERONET*
  - How dust loads affect visibility
  - Solar radiation attenuation
  - Health impact correlation

- **Dust storm genesis**
  - Shamal-driven vs convective dust events
  - Source regions (Iraq, Saudi, Sahara influence)
  - Particle size distribution

- **Particulate dynamics**
  - PM2.5/PM10 transport modeling
  - Long-range vs local dust sources
  - Deposition patterns

- **AERONET data** ⭐ *BOWG data source*
  - Understanding the measurements
  - How to use AOD data in BOWG
  - Integration with GFS/ERA5

### BOWG Application
- Air quality index for Bahrain
- Dust storm early warning
- Solar power output attenuation (dust blocks sunlight)

### Derived Products Needed
- Dust storm probability
- AOD trend analysis
- PM2.5/PM10 estimation
- Visibility forecast

---

## Priority 5: Precipitation & Radar 🌧️

### What to Study
- **Convective rainfall**
  - Why Gulf rain is intense, brief, and unpredictable
  - Thunderstorm development in arid climates

- **IMERG precipitation** ⭐ *Already in BOWG pipeline*
  - Satellite-based rain estimation
  - Accuracy in arid vs wet climates
  - How to use IMERG data

- **Flash flood risk**
  - Flat terrain + poor drainage + intense rain = flooding
  - Bahrain's flood vulnerability
  - Early warning thresholds

### BOWG Application
- Rainfall anomaly detection
- Flood risk assessment
- Water resource planning

### Derived Products Needed
- Rain intensity index
- Flood risk score
- Precipitation anomaly tracker

---

## Priority 6: Marine & Coastal Meteorology 🌊

### What to Study
- **Sea Surface Temperature (SST)** ⭐ *Drives everything in the Gulf*
  - SST as humidity source
  - Fog and storm energy
  - Seasonal patterns in Arabian Gulf

- **Tidal effects**
  - Bahrain's tidal flats
  - Weather-tidal interactions
  - Coastal inundation risk

- **Red Sea / Arabian Gulf interaction**
  - Regional moisture recycling
  - How neighboring water bodies influence each other

### BOWG Application
- Marine weather forecasting
- Coastal hazard assessment
- Fishing industry support

### Derived Products Needed
- SST anomaly tracker
- Tidal flood risk
- Marine weather index

---

## Priority 7: Climate Change Signals 📈

### What to Study
- **Compound extremes**
  - Heat + humidity + dust occurring together
  - Multi-hazard events
  - Cascading impacts

- **Warming trends**
  - GCC warming faster than global average
  - Historical trend analysis
  - Future projections

- **Sea level rise**
  - Bahrain is low-lying
  - Long-term coastal vulnerability
  - Infrastructure impact

### BOWG Application
- Long-term climate trend analysis
- Future risk assessment
- Policy support data

### Derived Products Needed
- Climate trend indices
- Compound event detection
- Sea level rise tracker

---

## Textbook Chapter Mapping

| Textbook Chapter | Priority | BOWG Relevance |
|------------------|----------|----------------|
| Atmospheric Circulation | 1 | Foundation for all weather patterns |
| Heat & Energy Balance | 2 | WBGT, heat index, solar irradiance |
| Humidity & Moisture | 3 | Gulf's defining characteristic |
| Aerosols/Dust | 4 | GCC's unique challenge |
| Precipitation | 5 | Flash flood prediction |
| Marine Climatology | 6 | Coastal weather forecasting |
| Climate Change | 7 | Long-term trends |

---

## Study Schedule Suggestion

| Week | Focus | Textbook Chapters | BOWG Product |
|------|-------|-------------------|--------------|
| 1-2 | Atmospheric Dynamics | General circulation, pressure systems | Wind pattern analysis |
| 3-4 | Heat & Energy | Balance, irradiance | WBGT calculator |
| 5-6 | Humidity | Dew point, sea breeze | Humidity stress index |
| 7-8 | Dust & Aerosols | AOD, dust storms | Dust storm probability |
| 9-10 | Precipitation | Convective rain | Flood risk assessment |
| 11-12 | Marine Climate | SST, tides | Marine weather index |
| 13-14 | Climate Change | Trends, extremes | Long-term analysis |

*Adjust pace based on depth needed and BOWG development progress*

---

## BOWG Data Sources & Their Climatology Context

| BOWG Data Source | Related Climate Topic | Why It Matters |
|------------------|----------------------|----------------|
| GFS | All weather patterns | Primary forecast model |
| ERA5 | Historical climate | Reanalysis for training/validation |
| MERRA-2 | Aerosols, reanalysis | Dust/air quality context |
| IMERG | Precipitation | Satellite rain estimates |
| AERONET | Aerosol optical depth | Ground-truth dust measurements |

---

## Next Steps

1. **Read textbook chapters** in priority order
2. **Cross-reference** with BOWG data sources as they become available
3. **Document insights** in this file as you learn
4. **Update BOWG pipeline** specs based on new understanding
5. **Build derived products** that reflect real climatology, not just arbitrary metrics

---

## Learning Notes

*Add insights and connections here as you study*

---

*Created: 2026-05-12*
*Last updated: 2026-05-12*
*Source: Climatology (4th Edition) — Rohli & Vega + BOWG domain mapping*
