# BOWG — Experiment Log

*A lab notebook. One entry per experiment: the question, what we did, what came
back, and what we concluded. Reproducible — every entry names its script, data,
and command. Append new entries at the bottom; never rewrite an old result (if a
later run changes it, add a new entry that supersedes).*

Companion docs: [[LOG]] (chronological session journal) · [[DECISIONS]]
(architecture choices) · [[BOWG-Phase0-Findings]] (narrative) · [[STUDYLIST]]
(concepts). This file is the **evidence trail**: every number we trust traces to
an entry here.

All runs use the project venv: `.venv/bin/python <script>`. Data files are
gitignored; scripts + this log are the durable record.

## Template

```
## E## — <title>            (YYYY-MM-DD)
- **Question:** what we're testing / hypothesis.
- **Method:** script, data source, key parameters, train/test split.
- **Result:** the numbers.
- **Verdict:** what we concluded + any decision it triggered.
- **Reproduce:** the command.
- **Caveats / links:** honest limits; pointers to [[DECISIONS]], STUDYLIST IDs.
```

## Summary

| ID | Experiment | Headline result |
|----|-----------|-----------------|
| E01 | Open-Meteo sanity check | Bahrain peak 35.7 °C (key-free reference) |
| E02 | ERA5 0.25° gridded pull | 36.1 °C; matches Open-Meteo +0.4 °C — pipeline valid |
| E03 | ARCO-ERA5 verification | 36.1 °C; matches CDS −0.04 °C — public-Zarr shortcut real |
| E04 | Land–sea mask grid | Bahrain cells 5–18% land → read as sea |
| E05 | ERA5-Land 0.1° probe | 38.5 °C; +2.4 vs 0.25° but still short |
| E06 | OBBI ground truth + moat recon | Real airport 44.0 °C (+7.9 vs ERA5); 3/4 moat sources open |
| E07 | Diurnal bias curve | Bias swings 0 → −6.2 °C across the day (6.4 °C) |
| E08 | Hour-of-day correction | Test RMSE 3.15 → 1.20 °C out-of-sample |
| E09 | Feature-based correction | 1.20 → 1.15 °C only: residual is external |
| E10 | Bahrain Open Data station survey | Temp is national-only; 5–7 spatial stations are air-quality-only |

---

## E01 — Open-Meteo sanity check            (2026-05-22)
- **Question:** what does real Bahrain summer temperature look like, fast, with no account?
- **Method:** `phase0/sanity_check_openmeteo.py`. Open-Meteo archive API (ERA5-derived), Manama point, 15–22 Jul 2023, hourly 2m temp/RH/apparent.
- **Result:** peak 35.7 °C; "feels like" 42.9 °C at 75% RH. All temps in plausible range.
- **Verdict:** plausible numbers; adopt Open-Meteo as a validation reference, not a source ([[DECISIONS]]). 35.7 °C looked suspiciously low → flagged marine smearing.
- **Reproduce:** `.venv/bin/python phase0/sanity_check_openmeteo.py`
- **Caveats:** point JSON, not gridded; same ERA5 limitation as everything downstream.

## E02 — ERA5 0.25° gridded pull + validation            (2026-05-22)
- **Question:** can we pull the real gridded ERA5 file BOWG will own, and is it correct?
- **Method:** `phase0/fetch_era5_bahrain.py`. CDS `reanalysis-era5-single-levels`, 2m temp, box 24–27 N/49–52 E, 15–22 Jul 2023. Opened in xarray, K→C.
- **Result:** 13×13 @ 0.25°. Manama cell peak 36.1 °C (Open-Meteo +0.4 °C). Domain peak 49.5 °C inland; 16.1 °C spread across the box.
- **Verdict:** pipeline correct (independent agreement). Marine-smear quantified.
- **Reproduce:** `.venv/bin/python phase0/fetch_era5_bahrain.py`
- **Caveats:** needs `~/.cdsapirc` + ERA5 licence accepted. STUDYLIST S1–S4.

## E03 — ARCO-ERA5 public-Zarr verification            (2026-05-22)
- **Question:** does Google's public ARCO-ERA5 Zarr match our CDS pull (i.e., can we skip building ingestion)?
- **Method:** `phase0/verify_arco_era5.py`. `xarray.open_zarr` on `gs://gcp-public-data-arco-era5/...`, anonymous, same cell/window.
- **Result:** 36.1 °C, −0.04 °C vs our CDS pull. Opened in 6.9 s, 273 vars, no GCP account.
- **Verdict:** shortcut is real → consume ARCO, mirror Gulf subset, drop bespoke ingestion ([[DECISIONS]]). Added `gcsfs`.
- **Reproduce:** `.venv/bin/python phase0/verify_arco_era5.py`
- **Caveats:** spatially-chunked → efficient for maps, not long point series. STUDYLIST S9–S11.

## E04 — Land–sea mask grid            (2026-05-22)
- **Question:** how much land does each cell over Bahrain actually contain — can a wider box capture Bahraini land?
- **Method:** `phase0/land_sea_mask_grid.py`. ERA5 land fraction + peak temp over the Gulf box, from ARCO.
- **Result:** Bahrain cells 5–18% land, read 34–36 °C (= sea); 100%-land Saudi/Qatar cells read 47–49 °C. Temperature ≈ readout of land fraction.
- **Verdict:** widening captures Saudi/Qatari land, never Bahraini. At 0.25° the island never dominates a cell — a hard resolution ceiling.
- **Reproduce:** `.venv/bin/python phase0/land_sea_mask_grid.py`
- **Caveats:** land-sea mask read at a real timestamp (1900 floor is empty). STUDYLIST S5–S6.

## E05 — ERA5-Land 0.1° probe            (2026-05-22)
- **Question:** does finer, land-only ERA5-Land give Bahrain its own land cells?
- **Method:** `phase0/fetch_era5land_bahrain.py`. CDS `reanalysis-era5-land`, 0.1°, same window.
- **Result:** only 6 land cells over the island; LAND peak 38.5 °C (+2.4 vs 0.25°), still ~11 °C below mainland.
- **Verdict:** helps but doesn't solve — ERA5-Land refines the surface but inherits ERA5's coarse atmosphere (land-surface ≠ atmospheric downscaling).
- **Reproduce:** `.venv/bin/python phase0/fetch_era5land_bahrain.py`
- **Caveats:** OBBI not yet involved. STUDYLIST S13–S14.

## E06 — OBBI ground truth + moat accessibility recon            (2026-05-22)
- **Question:** what does a real Bahraini thermometer read, and is local observation data obtainable?
- **Method:** `phase0/fetch_obbi_metar.py` (Iowa Mesonet, OBBI, same window) + web recon of Bahrain Met / AERONET / SCE air quality.
- **Result:** OBBI peak **44.0 °C** (ERA5 +7.9, ERA5-Land +5.5). Noon 42 °C / 17 °C dewpoint ≈ 24% RH (ERA5 implied 55–75%). 3/4 moat sources openly accessible.
- **Verdict:** the 8 °C gap is the project thesis, measured. Adopt OBBI METAR as ground truth/calibration source; moat moves Phase 4 → Phase 1 ([[DECISIONS]]).
- **Reproduce:** `.venv/bin/python phase0/fetch_obbi_metar.py`
- **Caveats:** OBBI is coastal → under-reads the interior. STUDYLIST S17–S18, S21.

## E07 — Diurnal bias curve            (2026-05-22)
- **Question:** is the cool-bias constant, or does it vary by hour of day?
- **Method:** `phase0/diurnal_bias.py`. 24-hour climatology at OBBI: OBBI vs ERA5 vs ERA5-Land.
- **Result:** ERA5 bias ~0 at dawn (+0.2 °C at 5h local) → −6.2 °C at 2 p.m.; 6.4 °C swing. ERA5 cell ~flat (33.8–34.4 °C) all day; station swings 34.6→40.6 °C.
- **Verdict:** the bias is a *missing diurnal cycle*, not an offset (sea heat capacity damps the day). A flat correction can't work. STUDYLIST S15–S16.
- **Reproduce:** `.venv/bin/python phase0/diurnal_bias.py`
- **Caveats:** single 8-day window; superseded as a *correction* by E08's trained version.

## E08 — Hour-of-day bias correction (train/test)            (2026-05-22)
- **Question:** can an hour-of-day correction beat raw + flat-offset out-of-sample?
- **Method:** `phase0/fetch_era5_summers.py` + `bias_correction_experiment.py`. Train JJA 2022, test JJA 2023, 2208 hrs each. ERA5 at OBBI cell vs OBBI obs.
- **Result:** test RMSE raw 3.15 → flat 2.10 → **hour-of-day 1.20 °C**; MAE 2.44 → 0.91; bias zeroed. 62% cut vs raw, 43% vs flat.
- **Verdict:** generalizes across years (no leakage). But per-station only; ~1.2 °C residual remains. STUDYLIST S24–S26.
- **Reproduce:** `.venv/bin/python phase0/fetch_era5_summers.py && .venv/bin/python phase0/bias_correction_experiment.py`
- **Caveats:** corrects ERA5 *at OBBI*, does not transfer to the island interior.

## E09 — Feature-based correction (does ERA5 explain its own residual?)            (2026-05-22)
- **Question:** can ERA5's own dewpoint/wind/season explain the ~1.2 °C residual from E08?
- **Method:** `phase0/fetch_era5_covars_summers.py` + `feature_bias_correction.py`. OLS (numpy), ERA5-derived predictors only (no station obs, to keep spatial transfer possible). Same 2022→2023 split.
- **Result:** hour-of-day 1.20 → feature model **1.15 °C RMSE (+5% only)**. Coeffs: dry clear afternoons grow the bias (+0.21), windy afternoons shrink it (−0.20) — small.
- **Verdict:** the residual is **external** — not in ERA5. Independent observations (the moat) are *required*, not optional, to go further. Decisive negative result. STUDYLIST S29.
- **Reproduce:** `.venv/bin/python phase0/fetch_era5_covars_summers.py && .venv/bin/python phase0/feature_bias_correction.py`
- **Caveats:** linear model; a nonlinear one (sklearn, not yet added) might gain a little, but headroom looks small.

---

## E10 — Bahrain Open Data station survey            (2026-05-23)
- **Question:** how many Bahraini sites log *temperature* (not just PM2.5), at what cadence/history? Enough spatial anchors for leave-one-station-out (S27)?
- **Method:** `phase0/survey_bahrain_opendata.py` (catalog scan, 493 datasets) + `phase0/survey_bahrain_weather_detail.py` (inspect weather/AQ datasets). Portal: data.gov.bh, OpenDataSoft Explore API v2.1.
- **Result:** Temperature/humidity/wind/rainfall exist but **national monthly aggregates only** (no station field; temp 2011–2025, rainfall 2005–2025). Per-station datasets are **air-quality only** (5 stations monthly / 7 yearly: Asker, Awali, Bahrain Fort, Gallali, Sitra, Central Store, Hidd) reporting pollutants (SO₂/NO₂/PM/O₃, µg/m³), annual/monthly means — **no temperature/met fields**.
- **Verdict:** open portal gives **no additional spatial temperature anchors**. Hourly air temp is still effectively OBBI-only → leave-one-station-out not yet possible from open data. Bahrain is **under-instrumented in *open* temperature data** (itself a finding / argument for BOWG).
- **Reproduce:** `.venv/bin/python phase0/survey_bahrain_opendata.py && .venv/bin/python phase0/survey_bahrain_weather_detail.py`
- **Leads opened:** (1) the 5–7 SCE air-quality stations are real located points and AQ monitors usually log met internally → a targeted SCE request could unlock spatial temperature; (2) check Iowa Mesonet for additional BH METAR stations (E10b); (3) raises priority of satellite thermal (E11). National monthly temp series = useful aggregate cross-check. *(Caveat: survey script's "SPATIAL" heuristic false-fired on the Arabic month field `shhr`.)*

## Planned (not yet run)

**E10b — Additional Bahraini METAR stations.** Question: does Iowa Mesonet carry more
than OBBI (e.g. Sakhir / other airfields)? Cheap query; each adds a free hourly anchor.

**E11 — Open satellite thermal over Bahrain.  ← NEXT SESSION.** Question: does open
EO thermal data resolve the island as distinct land, and how does satellite *skin*
temp relate to OBBI *air* temp? Approach (**decided route: Microsoft Planetary
Computer** — open STAC, no account, via `pystac-client` + `odc-stac`/`rioxarray`):
pull clear-sky Land Surface Temperature over Bahrain (start with Landsat ~100 m
and/or MODIS ~1 km), (1) confirm the island appears distinctly vs the 25 km smear,
(2) co-locate LST against OBBI air temp to characterize the skin↔air relationship
and its scatter. Caveats baked in (S30): skin ≠ air temp, clear-sky only, overpass
snapshots, resolution-vs-revisit tradeoff. Bahrain NSSA sovereign-satellite data +
licensing investigated separately. Dependency `pystac-client`+`odc-stac` pending a
decision. Prerequisite for E12.

**E12 — Three-way fusion (the cell, for real).** Question: can ERA5 (time) +
stations (true air temp) + satellite (spatial pattern) be fused into an
uncertainty-quantified estimate across the ungauged island? Approach: combine the
three, validate with leave-one-station-out + temporal holdout (no leakage). This is
the research core — see [[BOWG-Vision]]. Likely needs `sklearn` (decision pending).
