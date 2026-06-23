# BOWG — Phase 0 Findings

*The night we discovered Bahrain is smaller than the pixel. 2026-05-22.*

This is the story doc for Phase 0 — what we built, what each data layer is, and
what the numbers taught us. For the terse log see [[LOG]]; for locked choices see
[[DECISIONS]]; for the phase tracker see [[README]].

---

## TL;DR

We pulled real ERA5 weather data for Bahrain, validated it three independent
ways, and proved with hard numbers that **at standard global resolution
(0.25°, ~25 km) Bahrain is too small to register as land** — the grid cell
enclosing the island is 82–95% sea, so it reports a sea-moderated temperature
several degrees too cool. Going finer (ERA5-Land, 0.1°, ~9 km) helps but does
not solve it, and *why* it falls short points directly at the project's hardest
dependency: local Bahraini station data. We then **found that data** — the real
airport thermometer reads **44 °C** where standard global reanalysis says 36 °C
(an **8 °C** gap) — and confirmed the "moat" sources are openly accessible.

---

## The six data layers

We touched six datasets tonight. They form a ladder from "fast and approximate"
to "the real ground truth."

| #   | Layer                         | Resolution              | Access                | Role                        | Headline number               |
| --- | ----------------------------- | ----------------------- | --------------------- | --------------------------- | ----------------------------- |
| 1   | **Open-Meteo point**          | point (ERA5-derived)    | HTTP JSON, no key     | Instant reference           | 35.7 °C peak                  |
| 2   | **ERA5 0.25° (CDS)**          | 0.25° (~25 km)          | `cdsapi` → NetCDF     | The source BOWG owns        | 36.1 °C (matches #1 to +0.4)  |
| 3   | **ARCO-ERA5 (Google)**        | 0.25°                   | public Zarr, one line | The ingestion shortcut      | 36.1 °C (matches #2 to −0.04) |
| 4   | **ERA5 land–sea mask**        | 0.25°                   | from ARCO             | The diagnosis               | Bahrain cells 5–18% land      |
| 5   | **ERA5-Land 0.1° (CDS)**      | 0.1° (~9 km), land-only | `cdsapi` → NetCDF     | The partial cure            | 38.5 °C (+2.4 over #2)        |
| 6   | **OBBI METAR (Iowa Mesonet)** | point (airport)         | URL API, no key       | **The ground truth / moat** | **44.0 °C** (+7.9 over #2)    |

Each has a reproducible script in `phase0/`:
- `sanity_check_openmeteo.py` — layer 1
- `fetch_era5_bahrain.py` — layer 2
- `verify_arco_era5.py` — layer 3
- `land_sea_mask_grid.py` — layer 4
- `fetch_era5land_bahrain.py` — layer 5
- `fetch_obbi_metar.py` — layer 6

---

## Finding 1 — The pipeline is correct (triple validation)

Three independent paths to ERA5 agree at the Bahrain cell to a fraction of a
degree:

```
Open-Meteo point    35.7 °C
ERA5 0.25° (our CDS pull)   36.1 °C   (+0.4 vs Open-Meteo)
ARCO-ERA5 (Google Zarr)     36.1 °C   (−0.04 vs our pull)
```

This matters two ways: the data path BOWG owns produces trustworthy numbers, and
ARCO-ERA5 is bit-for-bit the same data — so we can skip building a custom
ingestion pipeline and just read the public Zarr. (See [[DECISIONS]].)

---

## Finding 2 — Bahrain is smaller than the pixel

At 26°N, one 0.25° grid cell is roughly **25 km × 28 km ≈ 700 km²**. Bahrain's
*entire* land area is ~786 km². So **one grid cell is nearly the size of the
whole country**, and because the island is long and thin (~50 km N–S but only
~15–18 km E–W), no 0.25° cell is ever majority-land.

ERA5's land–sea mask makes this exact. Land fraction of the cells over Bahrain:

| Cell | Land fraction | Peak temp |
|------|--------------|-----------|
| 26.25 N, 50.5 E | 11% | 36 °C |
| 26.00 N, 50.5 E *(Manama side)* | 18% | 34 °C |
| 25.75 N, 50.5 E | 5% | 35 °C |
| *any mainland Saudi cell* | 100% | 47–49 °C |

**Temperature is essentially a readout of land fraction.** Mostly-sea cells
(Bahrain) read ~35 °C; 100%-land cells (Saudi, Qatar) read ~49 °C. Widening the
search box does **not** capture Bahraini land — it captures *Saudi and Qatari*
land. There is no zoom level or aggregation that recovers Bahrain, because the
island never dominates a cell. The resolution is a hard ceiling.

---

## Finding 3 — ERA5-Land helps, but can't finish the job (the key insight)

ERA5-Land runs at 0.1° (~9 km) and is **land-only** — sea points are masked out,
so there's no sea to average into Bahrain's cells.

```
Bahrain footprint at 0.1°: 6 land cells register (vs ZERO at 0.25°)
Bahrain LAND peak:  38.5 °C   (+2.4 °C recovered)
0.25° sea-smeared cell:  36.1 °C
0.25° mainland desert:   49.5 °C   (still 11 °C above)
real Manama land station (extreme July): ~42–45 °C
```

So 0.1° claws back ~2.4 °C and gives genuine land cells — real progress — but
still lands ~4–6 °C short of what a thermometer on the ground records. **Why
matters more than the gap itself:**

> **ERA5-Land refines the land *surface*, but it is forced by ERA5's coarse
> 0.25° *atmosphere*.** The air mass driven across Bahrain is still the
> sea-moderated air from the parent model. You fix the ground but inherit the
> marine boundary layer above it. **Land-surface downscaling ≠ atmospheric
> downscaling.**

### Bonus: the diurnal flip
At night the land/sea relationship reverses. In the 03:00-local snapshot, the
land-only 0.1° product dips to ~25.8 °C while the sea-blended 0.25° product
floors at ~28.5 °C — land radiates heat away faster and goes *cooler* than the
sea after dark, then hotter by day. Same physics as the noon contrast, running
in reverse. The fine land grid keeps this swing; the coarse grid smooths it away.

---

## Finding 4 — The ground truth, and the size of the gap

The real OBBI (Bahrain International Airport) thermometer, same window, free from
the Iowa Environmental Mesonet:

```
ERA5 0.25 (sea-smeared global grid) ... 36.1 C
ERA5-Land 0.1 (land-only, finer) ...... 38.5 C   (+2.4)
OBBI METAR (actual thermometer) ....... 44.0 C   <- ground truth
---------------------------------------------------------------
Standard global reanalysis is  +7.9 C  too cool.
Even finer land-only is still  +5.5 C  short.
```

**The real island reads 44 C; the data source most people would reach for says
36.** That 8 C gap is the whole reason BOWG exists, measured end to end.

A second bias hides in the dewpoint: at noon OBBI reads 42 C with a 17 C dewpoint
= **~24% relative humidity** — hot and dry. The sea-smeared ERA5 cell showed
55–75% RH. So marine contamination didn't just cool the temperature, it roughly
**tripled the apparent humidity** — wrong air mass entirely (cool-humid sea vs
hot-dry land). Critical for Heat Index / WBGT products.

Caveat: OBBI sits on Muharraq, on the coast, so even this ground truth is a bit
coastal — the island interior likely runs hotter still.

## The moat is accessible (source recon, 2026-05-22)

| Source | Status | What you get | How |
|---|---|---|---|
| **OBBI airport (METAR)** | Open, programmatic, decades | Hourly T / dewpoint / wind / pressure | Iowa Mesonet URL API, no key |
| **AERONET Bahrain** | Open, 1998–2024 | Aerosol optical depth (dust), ~15-min | NASA download tool / raw `.txt` |
| **SCE air quality (BHmonitor)** | Open API | PM2.5, PM10, NO₂ | Bahrain Open Data Portal (`data.gov.bh`) |
| **Bahrain Met Directorate** | Partial | Real-time + monthly PDF summaries; archive to 1902 likely on request | `bahrainweather.gov.bh` |

Three of four are openly reachable now. The airport feed alone is a decades-long
hourly ground truth sitting exactly in the gap the physics opened — the
calibration data that turns ERA5/ERA5-Land into real Bahrain climate.

## Finding 5 — The bias breathes (it's a missing diurnal cycle, not an offset)

`phase0/diurnal_bias.py` builds the 24-hour climatology at the airport. The ERA5
cool-bias is not constant:

```
   5h  +0.2   (dawn: ERA5 slightly WARMER than the station)
  13h  -6.0
  14h  -6.2   (worst, mid-afternoon)
  20h  -1.0
```

Swing: **6.4 °C across the day** (worst −6.2, best +0.2). Two deeper reads:

1. **ERA5's cell barely has a day.** Its temperature sits ~33.8–34.4 °C across all
   24 hours, while the real station swings 34.6 → 40.6 °C. The sea's heat capacity
   damps the diurnal cycle, and Bahrain's mostly-water cell inherits an *ocean's*
   thermal personality. The error is **missing diurnal amplitude**, not an offset.
2. **The dawn flip.** At 5 a.m. ERA5 reads warmer than the station — overnight the
   sea holds heat while the land radiates away and cools below it. The bias changes
   sign. (Predicted from the QGIS night snapshot; confirmed here.)

Consequence: a flat correction constant is wrong at every hour. Real correction
must be time-of-day aware — and really, it must *restore physics* (the diurnal
cycle), which is why this is downscaling, not a patch. (See STUDYLIST S15–S16.)

## Finding 6 — A correction that works at the station, and proof the rest is external

Train an hour-of-day bias correction on summer 2022, test on summer 2023
(`bias_correction_experiment.py`, out-of-sample, no leakage):

```
              TEST (2023)   bias    MAE   RMSE
raw ERA5                   -2.35   2.44   3.15
flat-offset                +0.01   1.72   2.10
hour-of-day                +0.01   0.91   1.20   <- 62% RMSE cut vs raw
```

It generalizes across years and removes the midday diurnal residual a flat offset
leaves behind. **But it's per-station** (calibrates ERA5 *at OBBI*), and a ~1.2 C
residual remains.

Then: can ERA5's *own* fields explain that residual? (`feature_bias_correction.py`,
OLS on ERA5 dewpoint/wind/season, same 2022→2023 split.)

```
hour-of-day (baseline)      1.20 C RMSE
feature model (OLS)         1.15 C RMSE   <- only +5%
```

**No.** ERA5's own variables shrink the residual by only 5%. The missing signal is
**not in the reanalysis** — it is genuinely external information. This is the hard
proof that independent observations (the moat) are *required*, not optional, to go
further. (Small physical signals it did find: dry clear afternoons grow the bias,
windy afternoons shrink it — both real, both tiny.) See STUDYLIST S24–S29.

## What this means for BOWG

1. **0.25° ERA5 is "Gulf-regional climate including Bahrain's cell," NOT
   "Bahrain weather."** Marketing must match physics.
2. **ERA5-Land (0.1°) is the best *free* Bahrain-land baseline** — use it for
   anything land-specific. Still one product, still simple.
3. **Closing the final gap to ground truth requires either** dynamical
   downscaling (a regional model like WRF that grows its own boundary layer over
   the island) **or** statistical correction against **local station
   observations**.
4. Therefore the "moat" — Bahrain Meteorological Service / university station
   data — is **not optional polish. It is a physical necessity** for true island
   climate. Tonight turned the project's biggest unverified dependency into its
   most clearly required one.

---

## Reading the QGIS layers (reference)

When a time-aware NetCDF loads, QGIS adds it twice:
- **Singleband pseudocolor** — one timestep, colour-ramped. *Read this one.*
- **Multiband (Band 001/002/003)** — three consecutive hours mapped to R/G/B
  channels. Not physically meaningful; an artifact of RGB rendering.

Gotchas:
- **Units are Kelvin.** Subtract 273.15 for °C (298.9 K = 25.8 °C).
- **`valid_time` is Unix epoch seconds.** `1689379200` = 2023-07-15 00:00 UTC =
  03:00 Bahrain. The big afternoon land/sea contrast lives in the ~12:00-UTC
  band, not the first one.
- ERA5-Land tiles show coastlines crisply because sea is masked (NaN); 0.25°
  ERA5 blurs the coast because each cell blends land and sea.

---

## Next

Phase 0 is complete. Next is Phase 1 — mirror a Gulf-region subset from
ARCO-ERA5 into a local Zarr and serve it via a FastAPI `/point` endpoint, with
ERA5-Land as the candidate Bahrain-land layer — and, finally, verifying whether
local Bahraini station data is actually obtainable. See [[LOG]] for the live
next-step list.
