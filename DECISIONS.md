# Decisions

ADR-lite log of architectural and product decisions. Newest at top.

**Format:**
```
## YYYY-MM-DD — <short title>

**Context:** What forced the decision.
**Decision:** What we chose.
**Status:** Proposed | Accepted | Superseded
**Consequences:** Tradeoffs accepted.
```

Until Phase 0 produces real data, treat decisions marked **Proposed** as pending validation. Architecture freeze is premature.

---

## 2026-06-23 — Reposition: open reality-corrected reanalysis platform, API-first, with a consumer face

**Context:** Original framing was "legacy-grade open infrastructure / a diver's toolkit, *not* another weather app" (BOWG-Vision). The maintainer is repositioning toward a public-facing product for Bahrainis: the most accurate weather data they can get from global sources, scientifically sound. Framed as "Earth Nullschool insights × Open-Meteo democratization × reality mixed in." Phase 0 + spine are kept as the backend.
**Decision:** BOWG becomes an **open, reality-corrected reanalysis data platform for Bahrain/the Gulf**, with these locked choices:
- **Center of gravity = API-first data platform** (Open-Meteo's access model): a clean open API serving reality-corrected Bahrain data; apps/viz are built on top. **Reanalysis-first is correct; no live forecast source is added yet.** The current spine (ARCO-ERA5 → correction → FastAPI `/point`) is the right MVP.
- **Keep the open/forkable/citable DNA, add a consumer face** on top — not a pivot to closed consumer product.
- **The three influences map to three layers:** Open-Meteo = the *access model* (open, API-first); Earth Nullschool = the *experience/viz* (later phase, not the starting point); "reality mixed in" = the *differentiator* — local ground-truth bias correction, which neither of those does for Bahrain. This is the moat.
- **Role of reanalysis clarified:** ERA5 is the *calibration brain + historical climatology* (where the Bahrain bias-correction is learned), NOT a live-weather source. A live **forecast** layer (GFS/IFS) is a *future* phase; when it lands, the ERA5-learned correction is applied to forecast = "reality-corrected forecast." Until then the product serves corrected reanalysis/near-real-time, honestly labelled.
**Status:** Accepted (product direction). Roadmap re-sequencing (where viz/forecast/consumer-face land as phases) is Proposed — to draft next.
**Consequences:** Vision doc updated (below supersedes "not another weather app"). Two honesty bounds carried forward as hard constraints: (1) **"most accurate" is defensible only at OBBI/Muharraq, temporally** — the island interior remains an uncertainty-quantified estimate until spatial ground truth exists (E09/E10); claim "more accurate than uncorrected global apps," provable, never "accurate everywhere." (2) **Viz is not the starting point** — the differentiator is the data layer; the map is the later showcase. Stack ceiling unchanged for now (cdsapi/xarray/zarr/fastapi + gcsfs); a public API + consumer face will need new deps later, each via its own decision.

## 2026-06-23 — GitHub private remote as the second backup layer

**Context:** The 2026-05-22 scaffolding `git init` did not persist — Obsidian sync (primary backup) doesn't carry `.git`, and a vault resync left only markdown, losing all `phase0/` code and the `.venv`. The "GitHub remote vs Obsidian-sync-only" question left open at scaffolding is now forced by data loss.
**Decision:** Push BOWG to a **private** GitHub repo (`nawafalrumaihi/bowg`) as the durable second backup layer. Private for now (planning-stage); flip to public when there's a shippable artifact, matching the long-term open-source goal. Obsidian sync remains primary; git/GitHub is for version history and loss protection. Code, scripts, and `.md` are committed; data, `.venv`, caches, and secrets are gitignored.
**Status:** Accepted.
**Consequences:** Code now survives vault reorgs. Two backup layers can diverge — `git push` is a deliberate step, not automatic, so commit after meaningful work. `.cdsapirc` stays out of the repo (lives in `~`); CDS access must be re-established separately if lost.

## 2026-05-23 — Satellite thermal access via Microsoft Planetary Computer

**Context:** E09 proved the ERA5 residual is external; spatial signal must come from new open data. Satellite LST is the un-gatekeepable spatial source (E11), but access tooling varies (Planetary Computer vs Google Earth Engine vs NASA AppEEARS).
**Decision:** Use **Microsoft Planetary Computer** as the satellite-access route — open STAC catalog, no account required, fits the xarray/Zarr stack. Pull via `pystac-client` + `odc-stac`/`rioxarray`.
**Status:** Proposed (to validate in E11 next session; dependency not yet added — confirm before installing).
**Consequences:** Adds `pystac-client` + `odc-stac` (or `rioxarray`) when E11 runs. Keeps everything in the Python geospatial stack. GEE remains a fallback if PC coverage/latency disappoints. Honesty caveat carried: satellite LST is skin temp, not air temp (STUDYLIST S30).

## 2026-05-22 — Consume ARCO-ERA5 (public Zarr); do not build a NetCDF→Zarr ingestion pipeline

**Context:** Google publishes all of ERA5, regridded to uniform 0.25°, as a public Zarr store (`gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`), anonymous read, 273 variables, ERA5T at ~1-week lag. Verified in Phase 0: ARCO's Bahrain cell = 36.1 C, matching our own `cdsapi` pull to -0.04 C (`phase0/verify_arco_era5.py`). The original architecture's GFS/ERA5 buckets + cron + GRIB→Zarr conversion would re-implement, worse, what ARCO already provides.
**Decision:** Read gridded reanalysis directly from ARCO-ERA5. For independence/legacy, **mirror the Gulf-region subset** (bbox + chosen variables) into BOWG's own Zarr — small, VPS-sized, reproducible if the bucket ever disappears (recipes are open). Do **not** build a bespoke NetCDF→Zarr ingestion pipeline. Keep `cdsapi` only as a fallback for the latest ERA5T window and any variable absent from ARCO.
**Status:** Accepted (verified end-to-end). Supersedes the "separate forecast/reanalysis ingestion buckets" framing for reanalysis; revisit for GFS forecast separately.
**Consequences:** Adds `gcsfs` (required to read GCS Zarr; accepted). Production-scale reads cross-region from GCS — watch egress if we ever pull large volumes rather than the Gulf subset. Strengthens the prior "Zarr for gridded" decision: the whole ecosystem (Google, Copernicus, DestinE) converged on Zarr.

## 2026-05-22 — Open-Meteo as validation reference, not a source

**Context:** Phase 0 needs real Bahrain numbers fast, without waiting on a Copernicus CDS account + queue. Open-Meteo's Historical API serves ERA5 at a point as JSON, key-free.
**Decision:** Use Open-Meteo as a **validation reference** (the "known point" to sanity-check the gridded ERA5 we ingest), never as BOWG's data source. BOWG owns the gridded `cdsapi` -> Zarr pipeline. Building on Open-Meteo would make BOWG a proxy for the thing it exists to replace.
**Status:** Accepted.
**Consequences:** `requests` is used (already present; `cdsapi` depends on it anyway — no net stack growth). Phase 0 smoke test lives in `phase0/sanity_check_openmeteo.py`.

## 2026-05-22 — Moat sources verified accessible; adopt OBBI METAR as ground-truth/calibration source

**Context:** Resolves the source-investigation decision below. Phase 0 measured the bias to fix: OBBI airport reads 44.0 C where ERA5 says 36.1 C (+7.9 C) and ERA5-Land says 38.5 C (+5.5 C), same July 2023 window. We then confirmed the data to correct it is reachable.
**Decision:** Three of four moat sources are openly accessible (OBBI METAR via Iowa Mesonet, AERONET Bahrain, SCE air quality via Bahrain Open Data Portal). Adopt **OBBI METAR (Iowa Mesonet)** as the primary ground-truth / calibration reference for reanalysis bias correction. AERONET → future Dust Storm Index; SCE → air-quality products. Bahrain Met Directorate deep archive deferred (likely requires a request/relationship).
**Status:** Accepted (sources verified). Calibration *method* (statistical correction vs dynamical downscaling) is **Proposed**, to design in Phase 1.
**Consequences:** Adds `requests`-based point-source fetchers (already in stack). The moat shifts from Phase 4 unknown to Phase 1 asset. Marketing/accuracy claims can now be grounded against a real station.

## 2026-05-22 — Pull Bahrain-specific source investigation into Phase 1

**Context:** Bahrain Met Service, air quality, university stations are the project's actual moat. Original plan deferred them to Phase 4.
**Decision:** Spend ~1 hour in Phase 1 confirming whether these sources are accessible (web-scrapeable / FOI / closed). The answer reshapes the project if they're inaccessible.
**Status:** Accepted — **done 2026-05-22, positive result** (see entry above).
**Consequences:** Slightly later first ERA5 win, much earlier strategic clarity.

## 2026-05-22 — Phase 1 stack ceiling

**Context:** Stack bloat is the most likely failure mode for a solo open-source project. The original summary lists Airflow, K8s, Redis, TimescaleDB, GraphQL, WebSocket, Prometheus + Grafana before a single byte has flowed.
**Decision:** Phase 1 uses only `cdsapi`, `xarray`, `zarr`, `fastapi`. Add nothing else without a new decision entry here.
**Status:** Accepted (hard rule).
**Consequences:** Some manual ops work in early phases. Forces real pain to justify each new dependency.

## 2026-05-22 — Zarr for gridded, Parquet for tabular

**Context:** Gridded multi-dimensional climate data vs. point time-series obs have different access patterns.
**Decision:** Zarr for gridded ERA5 / MERRA-2 / IMERG. Parquet for AERONET and similar point sources. Defer TimescaleDB until point-query latency proves it's needed.
**Status:** Proposed.
**Consequences:** Two formats to learn. No SQL for point obs until justified.

## 2026-05-22 — Separate forecast and reanalysis pipelines

**Context:** GFS is real-time forecast; ERA5 is historical reanalysis. Different cadences, different validation strategies.
**Decision:** Two pipelines — `forecast/` bucket for GFS, `archive/` bucket for ERA5.
**Status:** Proposed.
**Consequences:** Some code duplication, clearer mental model.

## 2026-05-22 — Start at 0.25° global resolution; defer downscaling

**Context:** ERA5 native is 0.25° (~25km). Bahrain is ~50km across. 0.25° does not resolve micro-climates.
**Decision:** Phase 1 uses 0.25° as-is. Document the resolution limit honestly. Downscaling (statistical or dynamical) is its own future workstream, not a Phase-1 checkbox.
**Status:** Proposed.
**Consequences:** Marketing claims must match technical reality. Real micro-climate work deferred until there's a reason to do it.
