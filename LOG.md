# LOG

Chronological session log. Newest at top. Append-only.

---

## 2026-09-27 — Resume after 3 months; Phase 2 opened with a freshness/honesty fix

**Found by reading ARCO's own metadata:** the store is refreshed daily by Google (`last_updated` 2026-09-27) and carries `valid_time_stop` = 2026-06-30 (final ERA5) and `valid_time_stop_era5t` = 2026-09-21 (preliminary, **~6-day lag**). So the Phase 2 "cron/freshness ingestion" item likely shrinks to *reading these attrs* — Google already runs the ingestion.

**Bug (corrects the 2026-06-23 "Next" note):** a future `time` did *not* snap to the nearest available step. ARCO's time axis is **pre-allocated 1900–2050**; unwritten slots read as NaN, so `/point` returned **HTTP 200 with `raw_C: null`** while still labelling the correction "trustworthy here". Same for pre-1940. Recent ERA5T data was also served unlabelled as if final.

**Fix (`phase1/api.py`):** coverage parsed from the store attrs at startup (stop dates inclusive — boundary checked: 2026-09-21T23 has data, 09-22T00 is NaN). Times outside coverage (or any stray NaN) → **404 with an `availability` block**. Every response now carries `data_tier`: `final` or `preliminary (ERA5T) — may be revised`. `/` reports availability. Smoke test extended (future + pre-1940 must 404; 2023 must be `final`) — passes. No new deps.

**Open (not fixed, flagged):** the correction was trained on JJA only, but `/point` applies it in any month (e.g. a September query gets the summer offsets). Seasonal scope is the next honesty question — pending the external gap review started this session.

---

## 2026-06-23 — Phase 1 MVP built: reality-corrected /point API (the pitch, shipped small)

**Phase 1 done.** End-to-end reality-corrected `/point` works: ARCO-ERA5 raw → hour-of-day OBBI correction → JSON with raw + corrected + honest scope. New code: `phase0/fetch_obbi_metar.py` (E06 rebuilt), `phase1/train_correction.py` (E08 rebuilt), `phase1/api.py` (FastAPI), `phase1/smoke_test.py` (passes), `requirements.txt` (pinned recovery contract). Correction model committed as `phase1/correction_obbi_hourofday.json`.

- **Validation reproduced (E08):** train JJA 2022 / test JJA 2023, 2208 paired hrs each. Test RMSE **raw 3.60 → flat 2.52 → hour-of-day 1.44 °C** (60% cut, out-of-sample). Offsets +0.17 °C at night → −6.29 °C mid-afternoon — the missing diurnal cycle. Slightly higher than E08's 1.20 °C; explained by ARCO-vs-CDS source + my ob-snapping (nearest within 30 min). Structure and magnitude hold.
- **Live demo:** OBBI cell, 2023-07-19 13:00 UTC → raw 34.0 °C, corrected 38.9 °C (±1.44). Moves toward reality; falls short of that day's 44 °C because a *climatological* offset can't capture a single extreme afternoon — stated honestly, not hidden.
- **Honesty enforced in code:** the correction fires only inside the OBBI calibration cell; anywhere else (tested: Paris) it returns `corrected_C: null` with a scope note. No faked precision outside the validated domain.

**Methodological finding (matters): Open-Meteo's archive `temperature_2m` is NOT raw ERA5 0.25°.** Tried it as a fast training shortcut; it read **42.6 °C** where ARCO read **35.0 °C** for the same cell/week — it defaults to ERA5-Land (0.1°, land-aware), an already-partly-corrected, hotter product. Training against it would have used a baseline the API doesn't serve and laundered Open-Meteo's own correction (the "proxy for the thing we replace" failure DECISIONS warns of). So the correction is trained against ARCO (the served source) only; the slow ARCO point-series pull (chunk-1 store, ~9 min/summer, E03 caveat) was cached once to `phase1/cache/`. Reaffirms "Open-Meteo = reference, not source." See DECISIONS.

**Next (Phase 2):** durability + go public — cron/freshness, a second variable (dewpoint → Heat Index), cheap VPS deploy, open API docs. Also worth hardening: `/point` opens ARCO at startup (good) but a far-future `time` silently returns the nearest available step — add a freshness/staleness flag.

---

## 2026-06-23 — Repositioning: open reality-corrected platform, API-first + consumer face

**Strategic pivot (planning, no code).** Maintainer reframed BOWG from "open infrastructure / a diver's toolkit, *not* a weather app" toward a **public-facing, reality-corrected reanalysis data platform for Bahrainis** — "Earth Nullschool insights × Open-Meteo democratization × reality mixed in." The Phase 0 spine is kept as the backend.

**Two forks resolved (see DECISIONS 2026-06-23 reposition entry):**
- **Center of gravity = API-first data platform** (not consumer-app-first, not viz-first). Reanalysis-first is correct → **no forecast source added yet**; the current ARCO-ERA5 → correction → FastAPI `/point` spine is the right MVP.
- **Keep open/forkable/citable DNA + add a consumer face** (not a pivot to closed product).

**Framing locked:** Open-Meteo = access model (open, API-first); Earth Nullschool = experience/viz (later phase, *not* the start); "reality mixed in" = the moat (local ground-truth bias correction — the one thing neither competitor does). ERA5 = calibration brain + climatology, *not* live weather; a GFS/IFS forecast layer is a future phase that the ERA5-learned correction will be applied to.

**Honesty bounds carried as hard constraints:** (1) "most accurate" = *more accurate than uncorrected global apps* (provable), firmest at OBBI/Muharraq temporally; the interior stays an uncertainty-quantified estimate until spatial ground truth exists (E09/E10). (2) Viz is not the starting point.

**Docs updated:** BOWG-Vision.md ("What BOWG is/isn't" rewritten + new "product, restated" section), README tagline, DECISIONS.md (reposition entry, Accepted).

**Roadmap drafted:** re-sequenced into `ROADMAP.md` (6 phases; detail + exit criteria) and condensed into the README phase tracker. Phases beyond 1 are provisional. **Next concrete work = Phase 1:** reality-corrected `/point` API — rebuild the OBBI fetch + hour-of-day correction (lost with the old code) on top of the verified ARCO spine, served via FastAPI with raw + corrected + honest scope.

---

## 2026-06-23 — GitHub backup established + Phase 0 spine reconstructed

**Two things happened.** (1) Discovered the local git repo from the 2026-05-22 scaffolding was **gone** — Obsidian sync (primary backup) doesn't carry `.git`, so a vault resync left only the markdown. The entire `phase0/` code tree, `.venv`, `data/`, and old `.gitignore` did **not** survive. Findings are intact (this log, EXPERIMENTS, STUDYLIST); the code that produced them was lost. (2) Re-established git and pushed to a **private GitHub remote** as the durable second backup layer — closes the open question from the scaffolding session.

- **Backup:** `git init -b main` + new `.gitignore` (data/, *.nc, .venv/, graphify-out/, .cdsapirc); initial commit; `gh repo create bowg --private --source=. --push` → **github.com/nawafalrumaihi/bowg** (private). `origin/main` tracking, tree clean. See new DECISIONS entry.
- **Spine rebuilt (E03 reproduced):** recreated `.venv` (py3.11; 3.14 still lacks wheels) with `xarray 2026.4.0 / zarr 3.1.6 / gcsfs / cdsapi / netCDF4`. Reconstructed `phase0/verify_arco_era5.py` from EXPERIMENTS.md E03 and ran it: ARCO-ERA5 opened anonymously in 5.9 s (273 vars), Bahrain cell (26.00 N, 50.50 E) peak **36.06 °C** for 15–22 Jul 2023 — matches the recorded 36.1 °C. The chosen ingestion path is verified working again.

**Reality check for next session:** only `verify_arco_era5.py` has been reconstructed. The other phase0 scripts (E01–E10) are still missing and must be rebuilt from EXPERIMENTS.md before those results are reproducible. `~/.cdsapirc` is also gone — anything using `cdsapi` (E02, E05) needs the CDS token re-set + licences re-accepted; ARCO-based work (E03, E04) needs neither.

**Next action (unchanged target):** Phase 1 — extend `verify_arco_era5.py` from a single-cell read into a Gulf-subset mirror → local Zarr → FastAPI `/point`. E11 (satellite LST) still queued and still pending its dependency decision.

---

## 2026-05-23 — SESSION CLOSE & resume pointer (read this first)

**Where we are:** Phase 0 done and richly explored. Experiments E01–E10 complete (see [[EXPERIMENTS]]); the science narrative is in [[BOWG-Phase0-Findings]], concepts in [[STUDYLIST]] (S1–S30), the why in [[BOWG-Vision]], and the data/SCE plan in [[BOWG-Data-Strategy]].

**The story in one line:** ERA5 0.25° can't see Bahrain (island < grid cell; cell is 82–95% sea). Measured the gap end-to-end — the real airport reads 44 °C where ERA5 says 36 (+8 °C). An hour-of-day correction gets OBBI to 1.2 °C RMSE out-of-sample, but ERA5's own fields can't explain the residual (E09) → the missing signal is **external**. Open Bahrain data has no spatial temperature (E10). So the path is **computational gap-filling** with new open signal.

**NEXT ACTION → E11 (agreed):** pull open satellite **LST** over Bahrain via **Microsoft Planetary Computer** (decided route). Goals: (1) confirm satellite resolves the island as distinct land vs the 25 km smear; (2) characterize how satellite *skin* temp relates to OBBI *air* temp at the one point we can check (mind S30: skin ≠ air, clear-sky, snapshots). Prereq for E12 (ML fusion: ERA5 + satellite + static physiography → air temp).

**Dependency to add next session (decision pending):** `pystac-client` + `odc-stac`/`rioxarray` for Planetary Computer (E11). Later: `scikit-learn`/XGBoost for E12 (start with numpy-linear rung first).

**Honesty anchor for E12:** with only OBBI we can validate *temporally*, not at the ungauged interior — interior output is uncertainty-quantified estimate, not verified truth. Aggregate cross-check available: predicted field averaged over Bahrain vs the national monthly mean (E10).

**Housekeeping:** working tree clean; `STATE.md`/`LINKAGES.md`/`graphify-out/` are stale HermesBrain auto-files, left for regeneration. Env: `.venv` (py3.11) with cdsapi/xarray/zarr/netCDF4/gcsfs; `~/.cdsapirc` set; ERA5 + ERA5-Land licences accepted.

---

## 2026-05-22 — Phase 0 COMPLETE: gridded ERA5 on disk, validated

- `phase0/fetch_era5_bahrain.py`: pulled gridded ERA5 `2m_temperature` for the Bahrain bbox (24–27 N, 49–52 E), July 15–22 2023, via `cdsapi`. 13×13 @ 0.25°, 192 hourly steps, 89 KB NetCDF. Opened in xarray, K→C. **Phase 0 deliverable met.**
- CDS setup: new-CDS Personal Access Token in `~/.cdsapirc` (`url: .../api`, no UID:key). Had to accept the ERA5 licence on the dataset page before requests cleared (403 until then). Request ran in ~35 s end to end.
- **Pipeline validated:** our CDS grid's Manama cell peak (36.1 C) agrees with the Open-Meteo ERA5 point (35.7 C) to **+0.4 C**. The source path BOWG owns is correct.
- **Resolution finding, quantified:** 16.1 C spread across the ~330 km box at the hottest step. Bahrain cell 36 C (mostly sea) vs inland desert 49.5 C. Caveat for the record: 49.5 C is mainland Saudi, NOT Bahrain — the real issue is that at 0.25° Bahrain has no land cell of its own (island < grid spacing). Missing information, not a correctable offset. Downscaling is a genuine workstream.
- **Architecture thread to pull:** CDS now serves a dedicated ERA5 catalogue pre-stored in ARCO **Zarr** for point/time-series retrieval (`reanalysis-era5-single-levels-timeseries`). We chose Zarr in DECISIONS.md — Copernicus already serves it. Could change ingestion: consume their ARCO Zarr vs. NetCDF→re-Zarr ourselves. Evaluate before Phase 1 storage work.
- Env: `.venv` on python3.11 (3.14 lacked binary wheels). Installed `cdsapi`, `xarray`, `zarr`, `netCDF4`. Data gitignored (`data/`, `*.nc`).

**Next:** Phase 1 — decide ingestion source (raw NetCDF vs CDS ARCO Zarr), then one source/one variable/one region → Zarr → FastAPI `/point`. Before storage code: resolve the ARCO-Zarr question in DECISIONS.md.

---

## 2026-05-22 — ARCO-Zarr question resolved (verified)

- Investigated the ARCO thread. Found Google's public ARCO-ERA5 Zarr: full 0.25° ERA5, anonymous read, 273 vars, ERA5T ~1-week lag. `phase0/verify_arco_era5.py` opened it in 6.9 s and pulled the Bahrain cell for the same July 2023 window.
- **Result: 36.1 C, matching our own CDS pull to -0.04 C.** Same grid point (26.00 N, 50.50 E). The public-Zarr shortcut is proven, not assumed.
- **Decision logged (Accepted):** consume ARCO-ERA5, mirror only the Gulf subset for independence, drop the bespoke NetCDF→Zarr ingestion pipeline, keep `cdsapi` as fallback. See DECISIONS.md.
- Added `gcsfs` to the venv (needed to read GCS Zarr).
- Three ARCO/Zarr sources distinguished: Google ARCO (gridded archive — chosen), CDS `…-timeseries` (point extraction — possible Open-Meteo replacement), DestinE Earth Data Hub (EU mirror — backup).

**Next:** Phase 1 — mirror a Gulf-region subset (bbox + first variables) from ARCO-ERA5 into a local Zarr, then a FastAPI `/point` endpoint over it. Open question still untouched: Bahrain-specific source accessibility (the moat).

---

## 2026-05-22 — Resolution probes: land-sea mask + ERA5-Land 0.1deg

- `phase0/land_sea_mask_grid.py`: ERA5 land fraction over the Gulf box. Bahrain cells are **5–18% land**, read 34–36 C (== open sea); 100%-land Saudi/Qatar cells read 47–49 C. Temperature is a direct readout of land fraction. Widening the box captures Saudi/Qatari land, never Bahraini — no aggregation isolates Bahrain because it never dominates a 0.25 deg cell.
- `phase0/fetch_era5land_bahrain.py`: ERA5-Land at 0.1 deg (land-only). Bahrain footprint yields **only 6 land cells**; LAND peak **38.5 C** = **+2.4 C** vs the 0.25 deg sea-smeared cell, but still ~11 C below mainland and ~4–6 C below a real Manama station extreme.
- **Key physics finding:** ERA5-Land refines the land *surface* but is forced by ERA5's coarse 0.25 deg *atmosphere* — the marine-moderated air mass is inherited. Land-surface downscaling != atmospheric downscaling. So ERA5-Land is the best free baseline but cannot reach true Bahrain land climate alone.
- **Implication for strategy:** closing the last gap needs dynamical downscaling (WRF-style) OR statistical correction against local station obs. This makes the "moat" (Bahrain Met / university stations) a *physical necessity*, not optional polish. Strengthens the DECISIONS.md call to pull moat investigation into Phase 1.

**Next:** unchanged (Phase 1 ARCO subset → Zarr → FastAPI), now with ERA5-Land as the candidate Bahrain-land baseline and a sharpened reason to verify local-station access early.

---

## 2026-05-22 — Moat verified accessible + ground-truth gap measured

- Source recon (the DECISIONS.md "confirm Bahrain source accessibility" task): **three of four sources openly reachable.** OBBI airport METAR via Iowa Mesonet (URL API, no key, decades hourly); AERONET Bahrain (1998–2024, free); SCE air quality via Bahrain Open Data Portal `data.gov.bh` (open API). Bahrain Met Directorate `bahrainweather.gov.bh` = partial (real-time + monthly PDF summaries; deep archive to 1902 likely on request).
- `phase0/fetch_obbi_metar.py`: pulled OBBI hourly temp for the same July 2023 window. **Peak 44.0 C** (2023-07-19 13:30 UTC) vs ERA5 36.1 C (**+7.9 C**) and ERA5-Land 38.5 C (**+5.5 C**). The 8 C gap = the project thesis, measured.
- Secondary finding: at noon OBBI = 42 C / 17 C dewpoint = **~24% RH** (hot, dry). Sea-smeared ERA5 showed 55–75% RH. Marine contamination ~tripled apparent humidity — wrong air mass, not just wrong temperature. Matters for Heat Index / WBGT.
- Caveat logged: OBBI is coastal (Muharraq), so it under-reads the island interior — true gap is likely larger.

**Next:** Phase 1. Candidate calibration design: correct ERA5/ERA5-Land against OBBI METAR (and later more stations) to recover real Bahrain land climate. Still to assess: AERONET + SCE data shapes/cadence for the dust and air-quality products.

---

## 2026-05-22 — Diurnal bias curve + STUDYLIST.md established

- `phase0/diurnal_bias.py`: 24-hour bias climatology at OBBI. ERA5 cool-bias swings from ~0 at dawn (+0.2 C at 5h local — actually *warmer*) to **−6.2 C at 2 p.m.**, a **6.4 C diurnal swing**. ERA5's cell sits ~flat at 33.8–34.4 C all day (ocean-like, no diurnal cycle) while the station swings 34.6→40.6 C. **The bias is missing diurnal amplitude, not an offset** → correction must be time-of-day aware. Confirms the QGIS-spotted dawn flip.
- New living doc: `STUDYLIST.md` — numbered curriculum (S1–S23) of concepts hit so far, with "dig deeper" pointers. User wants to learn the science deeply; we append every session and reference items by ID. Linked from README.
- Findings doc gained "Finding 5"; README doc-map updated.

**Next:** Phase 1 build, or continue exploration (AERONET dust thread / first real bias-correction experiment). Maintain STUDYLIST.md going forward.

---

## 2026-05-22 — First bias-correction experiment (out-of-sample, it works)

- `phase0/fetch_era5_summers.py` + `phase0/bias_correction_experiment.py`. Pulled ERA5 0.25° JJA 2022+2023 (1.5 MB). Trained hour-of-day mean-bias correction on **2022**, tested on **2023** (2208 paired hrs each, no leakage).
- **Result (test/2023): RMSE 3.15 → 2.10 (flat) → 1.20 C (hour-of-day).** Bias zeroed; MAE 2.44 → 0.91. Hour-of-day cuts RMSE 62% vs raw, 43% vs flat — generalizes across years. Learned offsets reproduce the diurnal curve (−0.5 night → −5.2 noon). Flat offset leaves a 3.1 C midday residual; hour-of-day removes it.
- **Limits (honest):** per-station only (calibrates ERA5 *at OBBI*, not the island interior); ~1.2 C residual = day-to-day synoptic variability a climatological lookup can't capture.
- STUDYLIST gained section J (S24–S28): leakage, baselines, this result, spatial generalization (leave-one-station-out), feature-based downscaling.

**Direction (user steer):** move toward feature-based correction that learns *patterns* from covariates (dewpoint, wind, season, distance-to-coast) to capture the synoptic residual, and pull Bahrain Open Data station obs for *spatial* ground truth — the real path to "solving the Bahraini cell." Validate via temporal + leave-one-station-out holdout (no leakage).

---

## 2026-05-22 — Feature-based correction: residual is external (decisive negative result)

- `phase0/fetch_era5_covars_summers.py` + `phase0/feature_bias_correction.py`. Added ERA5's OWN dewpoint, 10m wind, season + day/night interactions as predictors (deliberately NOT station obs, so the correction could transfer to ungauged points). OLS, same 2022→2023 holdout.
- **Result: hour-of-day 1.20 → feature model 1.15 C RMSE (+5% only).** ERA5's own fields barely explain the residual. Verdict: **the missing signal is not in ERA5** — closing the gap *requires* independent observations. Hard evidence that the moat is mandatory, not optional.
- Physics found (small but sensible): `depression×daytime +0.21` (dry clear afternoons grow the bias), `wind×daytime −0.20` (windy afternoons shrink it).
- Balanced read: 1.15 C RMSE is a genuinely good *per-station* product at OBBI; limits are (a) no spatial transfer, (b) ERA5-alone ceiling ~1.2 C. A nonlinear model might gain a little; structural conclusion holds.
- STUDYLIST S29 added (useful negative result / irreducible-from-features).

**Next (now clearly the move):** the spatial track — survey Bahrain Open Data Portal for additional stations *with temperature*, enabling leave-one-station-out and the real attempt at the ungauged cell. Stack note: feature model used `numpy` OLS only (no `sklearn` yet — would need a decision to add).

---

## 2026-05-23 — E10: Bahrain Open Data survey (no open spatial temperature)

- `phase0/survey_bahrain_opendata.py` + `phase0/survey_bahrain_weather_detail.py`. Scanned 493 datasets on data.gov.bh (OpenDataSoft API).
- **Result:** temperature/humidity/wind/rainfall are **national monthly aggregates only** (no station field; temp 2011–2025). Per-station data is **air-quality only** — 5–7 located SCE stations (Asker, Awali, Bahrain Fort, Gallali, Sitra, Central Store, Hidd) reporting pollutants, annual/monthly means, **no temperature**.
- **Verdict:** open portal adds **no spatial temperature anchors**; hourly air temp still effectively OBBI-only. Bahrain is under-instrumented in *open* temperature data — itself a finding.
- **Leads:** (1) SCE AQ stations likely log met internally → targeted request could unlock spatial temp at 5–7 points (the moat relationship, now specific); (2) E10b: check Iowa Mesonet for more BH METAR stations; (3) satellite thermal (E11) priority up. National monthly temp = aggregate cross-check.

**Next:** E10b (extra METAR stations, cheap) → E11 (satellite thermal) → E12 (fusion). Or open the SCE met-data request (institutional, slower). See [[EXPERIMENTS]].

## 2026-05-22 — Phase 0 started: Open-Meteo sanity check (first code)

- First code in the repo: `phase0/sanity_check_openmeteo.py`. Pulls ERA5-via-Open-Meteo for Manama over a hot July 2023 week, key-free. `requests` only (already installed).
- **Finding:** peak 2m temp came back **35.7 C** — too cool for mid-July Manama (land stations hit 38–42 C). RH 55–75%, "feels like" 42.9 C, reported elevation 53 m. Signature of **marine contamination**: the ERA5 grid cell over Bahrain is dominated by Gulf sea surface, which moderates dry-bulb temp. Concrete confirmation of the 0.25-degree resolution caveat (CLAUDE.md honesty note #1) on day one.
- Logged decision: Open-Meteo is a validation reference, not a source (see DECISIONS.md).
- Env note: system Python 3.14, `requests` in user site-packages with a urllib3 version mismatch (noisy warning, harmless for GET).

**Next:** Set up Copernicus CDS account + `~/.cdsapirc` key, then the real Phase 0 deliverable — pull the gridded ERA5 NetCDF via `cdsapi`, open in xarray, and compare the land-cell value against this 35.7 C reference to quantify the marine smear.

## 2026-05-22 — Scaffolded project folder

- Canonical location: `~/Documents/Ideas/Projects/BOWG/` (inside the Obsidian vault).
- During scaffolding, the user reorganized the vault — lowercase `projects/` was deprecated in favor of capitalized `Projects/`, and the original blueprint (`Bahrain-Open-Weather-Gateway.md`) was relocated into this folder. New docs were briefly trashed and then restored into the right path.
- Added: `README.md`, `CLAUDE.md`, `DECISIONS.md`, `LOG.md`, `.gitignore`. Moved `BOWG-Summary.md` from `~/Desktop/`.
- Pre-existing in folder: `Bahrain-Open-Weather-Gateway.md`, `BOWG.md`, `BOWG-Study-Roadmap.md`, `research/earth-nullschool-reference.md`. All preserved.
- `git init` + initial commit. Git is a **secondary** backup layer; the Obsidian vault has its own sync as the primary.
- No code, no dependencies, no Phase 0 work yet.

**Next:** Phase 0 — pull one ERA5 file end-to-end via `cdsapi`, open in xarray, sanity-check values for Bahrain on a known hot day. Not started.

**Open questions for next session:**
- Copernicus CDS account: exists already, or need to create?
- First variable: 2m temperature is the safe default — confirm.
- Bahrain-specific sources: has anyone contacted Bahrain Met Service yet, or start cold?
- Second backup layer beyond git: GitHub remote, or relying on Obsidian sync + git locally?
