# BOWG — Study List

*A living curriculum. Every concept, technique, and "aha" we hit while building
BOWG, with a one-line what-we-saw and a "dig deeper" pointer. Append as we go;
never delete. Reference items by their ID (e.g. "S12").*

This is the science-soak companion to the engineering log ([[LOG]]) and the
findings narrative ([[BOWG-Phase0-Findings]]). When something here clicks into a
real understanding, that's the point.

How to use it: skim the section that matches what we're doing, follow a "Dig
deeper" when you want to go down a rabbit hole, and tell me when you want a topic
expanded into its own note.

---

## A. Reanalysis & climate data products

**S1 — What "reanalysis" even is.** ERA5 isn't measurements; it's a physics model
(ECMWF's IFS) re-run over history, *nudged* toward every observation that existed
(satellites, balloons, stations, ships) via data assimilation. Output: a gap-free,
physically-consistent 4D field. *We used it as our base layer.*
Dig deeper: ECMWF "What is a reanalysis?"; the concept of **data assimilation**
(4D-Var). Why a model + obs beats either alone.

**S2 — ERA5 vs ERA5-Land vs ERA5T.** ERA5 = 0.25° global, atmosphere+surface.
ERA5-Land = 0.1°, land-surface only, re-run at higher resolution but *forced by
ERA5's coarse atmosphere* (this caveat is the heart of S15). ERA5T = the
preliminary near-real-time release (~5-day to 1-week lag) later replaced by the
final product. *We pulled ERA5 and ERA5-Land and watched them disagree.*
Dig deeper: Copernicus ERA5 vs ERA5-Land documentation; why "land-only, same
forcing" can't fully fix resolution.

**S3 — Reanalysis vs forecast vs observation.** Three different epistemic objects:
forecast (future, model only), reanalysis (past, model + assimilated obs),
observation (a real instrument, one point). BOWG uses all three for different jobs.
Dig deeper: why you validate a reanalysis *against* observations, not vice versa.

## B. Grid resolution & geometry

**S4 — Why 0.25° ≈ 25 km, and why it's not square.** A degree of latitude is ~111 km
everywhere; a degree of longitude shrinks by cos(latitude). At 26°N, 0.25° lon ≈
25 km but 0.25° lat ≈ 28 km. *We computed a cell ≈ 700 km² — nearly Bahrain's whole
land area.*
Dig deeper: map projections, the cosine-latitude factor, equirectangular grids.

**S5 — "Smaller than the pixel."** A feature narrower than the grid spacing cannot
get its own cell. Bahrain (~15–18 km E–W) never dominates a 25-km cell, so it never
appears as land. *The central finding of Phase 0.*
Dig deeper: the **representativeness** problem; sub-grid-scale heterogeneity.
**S6 — The land–sea mask.** Each cell carries a *fractional* land value (0–1), not a
binary. Bahrain's cells are 5–18% land. The model's surface energy balance is a
blend weighted by that fraction → a mostly-sea cell behaves like sea. *We mapped it
and saw temperature track land fraction almost exactly.*
Dig deeper: ERA5 land-sea mask + sub-grid surface tiling; how models blend surface types.

## C. Data formats & infrastructure

**S7 — NetCDF & the data model.** Self-describing N-dimensional arrays with named
dimensions, coordinates, units, and metadata (CF conventions). Climate data's lingua
franca. *Both our CDS pulls are NetCDF; xarray opened them.*
Dig deeper: CF conventions; `ncdump -h`; why named dims beat bare arrays.

**S8 — GRIB.** WMO's compact binary format for operational met data (what ECMWF/NOAA
emit natively). Denser than NetCDF, needs special readers. *ARCO converts GRIB→Zarr.*
Dig deeper: GRIB2 structure; why ops centers use it.

**S9 — Zarr & cloud-optimized data.** Chunked, compressed N-d arrays stored as many
small objects (great for cloud object storage + parallel/partial reads). You can open
a global dataset and read only the chunks you touch. *Our chosen storage format; the
basis of the ARCO shortcut.*
Dig deeper: chunking strategy, the "analysis-ready cloud-optimized" (ARCO) idea,
Zarr v3, why this killed our need for a bespoke ingestion pipeline.

**S10 — xarray.** Pandas-for-N-d-arrays: label-based selection (`.sel`), nearest-cell
lookup, `groupby` over time, lazy loading. *Every analysis script leans on it.*
Dig deeper: `.sel(method="nearest")`, `groupby("time.hour")`, dask integration.

**S11 — Anonymous public cloud datasets.** ARCO-ERA5 lives in a public GCS bucket;
`token="anon"` reads it with no account. Open *data* in an open *format* with public
*recipes* = reproducible even if the host vanishes. *Why we can depend on it without
betraying the "legacy-grade" goal.*
Dig deeper: requester-pays vs free public buckets; the Pangeo/cloud-native geoscience movement.

## D. Downscaling (the core research problem)

**S12 — Statistical vs dynamical downscaling.** Statistical = learn a correction from
local observations and apply it (cheap, needs ground-truth data = the moat). Dynamical
= run a high-resolution physics model (e.g. WRF) nested in the global one (expensive,
physically grounded). *BOWG will likely need both eventually.*
Dig deeper: WRF; quantile mapping / bias correction; pros/cons of each.

**S13 — Land-surface vs atmospheric downscaling.** ERA5-Land refines the *ground* but
inherits ERA5's coarse *air*. Refining the surface under a sea-moderated air mass only
gets you part way. *Why ERA5-Land closed only ~2.4 of the ~8°C gap.*
Dig deeper: land–atmosphere coupling; boundary forcing; why the air mass matters more
than the surface for 2m temperature near coasts.

**S14 — The atmospheric boundary layer.** The lowest ~1–2 km of air that "feels" the
surface within hours. Over hot land it grows deep and well-mixed; over sea it stays
shallow and cool. A coarse model advecting marine boundary-layer air over a tiny island
keeps the island cool. *The mechanism behind our whole bias.*
Dig deeper: convective boundary layer, sea-breeze circulation, land/sea thermal contrast.

## E. The diurnal cycle & thermal inertia

**S15 — Heat capacity & why the sea has no "day."** Water stores ~4× the heat of air
and mixes, so its temperature barely moves day-to-night; land heats and cools fast.
*We saw ERA5's sea-dominated cell stay ~flat at 34°C all 24h while the real station
swung 35→41°C.*
Dig deeper: specific heat capacity, thermal inertia, diurnal temperature range (DTR).

**S16 — The bias is a missing diurnal cycle, not an offset.** (`diurnal_bias.py`) The
ERA5 cool-bias ran ~0 at dawn (even +0.2°C — *warmer*) and −6.2°C at 2 p.m., a 6.4°C
swing. So the error isn't a constant to subtract — it's the island's day/night
amplitude that the ocean-like cell never produced. *This reframes correction as
restoring physics, not patching a number.*
Dig deeper: why time-of-day-aware bias correction is mandatory; diurnal-cycle metrics.

## F. Ground truth & observations

**S17 — METAR & airport observations.** Standardized hourly (often half-hourly) aviation
weather reports: temp, dewpoint, wind, pressure, visibility. Globally archived (Iowa
Mesonet). *Our ground truth: OBBI peaked at 44°C.*
Dig deeper: METAR decoding; ASOS/AWOS; WMO station siting standards (Stevenson screen,
2 m height, grass — why airport readings aren't just hot tarmac).

**S18 — Point vs grid; representativeness again.** A station is one spot; a grid cell is
an area-average. Comparing them fairly means knowing what each represents. OBBI itself
sits on the coast → even our "ground truth" under-reads the island interior.
Dig deeper: spatial representativeness error; how to compare point obs to gridded fields.

## G. Bias, calibration & validation

**S19 — Validation by independent agreement.** We trusted the pipeline because three
independent ERA5 paths (Open-Meteo, our CDS pull, ARCO) agreed to ±0.4°C. Agreement of
independent methods → confidence the *plumbing* is right (separate from whether the
*data* resolves Bahrain).
Dig deeper: verification vs validation; the difference between "code correct" and
"physically adequate."

**S20 — Why a flat offset fails.** Follows from S16: a single correction constant
applied to a curve is wrong everywhere except where it crosses. Real calibration is a
function of (at least) hour-of-day, and probably season and synoptic regime.
Dig deeper: regression-based MOS (model output statistics); conditioning on covariates.

## H. Humidity & heat stress

**S21 — Dewpoint vs relative humidity.** Dewpoint = absolute moisture (temperature at
which air saturates); RH = moisture relative to capacity at the current temp. *OBBI noon:
42°C / 17°C dewpoint ≈ 24% RH — hot and dry. The sea-smeared ERA5 cell implied 55–75%
RH — wrong air mass entirely.*
Dig deeper: Clausius–Clapeyron; why RH is misleading without temperature; mixing ratio.

**S22 — Heat-stress indices (future products).** Heat Index and WBGT combine temperature
+ humidity (+ wind/radiation for WBGT) into a felt-stress number. Getting the *air mass*
right (S21) is a prerequisite — a cool-humid bias and a hot-dry reality give very
different stress. *Motivates why the humidity bias matters as much as temperature.*
Dig deeper: WBGT definition; Heat Index formula; wet-bulb temperature and survivability
thresholds (the Gulf is a hotspot in this literature).

## I. Data source catalogue (where the bytes live)

**S23 — The six layers we used.** Open-Meteo (point, key-free reference) · ERA5 0.25°
(CDS / ARCO) · ERA5-Land 0.1° (CDS) · ERA5 land-sea mask · OBBI METAR (Iowa Mesonet) ·
Bahrain moat sources (AERONET aerosols, SCE/Bahrain Open Data air quality). *See
[[BOWG-Phase0-Findings]] for the full ladder and numbers.*
Dig deeper: each source's licence, cadence, and lag; the Copernicus CDS API; the Iowa
Environmental Mesonet; NASA AERONET; the Bahrain Open Data Portal.

## J. Bias correction & learning from data

**S24 — Data leakage & out-of-sample evaluation.** If you train and test on the
same data, any method looks great — you're measuring memorization, not skill. The
fix: hold out data the model never sees. *We trained the correction on summer 2022
and tested on 2023; the 62% RMSE cut is trustworthy because 2023 was unseen.*
Dig deeper: train/validation/test splits, temporal vs random holdout, k-fold CV.

**S25 — Beat the dumb baseline.** A complex method only earns its keep if it beats a
trivial one on held-out data. *Hour-of-day (RMSE 1.20) had to beat flat-offset
(2.10) and raw (3.15) — it did.* Always carry baselines.
Dig deeper: skill scores; the principle of the simplest model that works.

**S26 — Our first correction: result & limits.** (`bias_correction_experiment.py`)
Hour-of-day mean-bias correction cut out-of-sample RMSE 3.15→1.20 C and removed the
midday diurnal residual a flat offset leaves behind. BUT: (a) it's **per-station** —
calibrates ERA5 *at OBBI*, not across the island; (b) a **~1.2 C residual remains** =
day-to-day synoptic variability a climatological lookup can't capture. That residual
is the real signal-from-noise frontier.
Dig deeper: model output statistics (MOS); climatological vs conditional correction.

**S27 — Solving "the cell" = spatial generalization.** Per-station correction fixes
points we have stations for. Predicting the *ungauged* island interior is spatial
downscaling, and the binding constraint is **spatial ground truth (number of
stations)**, not method cleverness. Test it honestly with **leave-one-station-out
CV**: hide a whole station, predict it, see if the model transfers in space.
Dig deeper: leave-one-group-out CV; geostatistics/kriging; the ungauged-basin problem.

**S28 — Feature-based (covariate) downscaling.** To shrink the synoptic residual
(S26), condition the correction on predictors that carry the day's signal: dewpoint,
wind speed/direction, day-of-year, and physiographic terms (distance-to-coast, land
fraction, elevation). A regression or ML model learns patterns instead of a fixed
lookup — *if* validated without leakage (S24, S27).
Dig deeper: random forests / gradient boosting for downscaling; physics-informed
features; why distance-to-coast matters for an island.

**S29 — When the residual is *external* (a useful negative result).**
(`feature_bias_correction.py`) Adding ERA5's own dewpoint/wind/season to the
hour-of-day correction cut test RMSE only 1.20→1.15 C (+5%). Interpretation: the
leftover error is **not** recoverable from the reanalysis — the missing signal
isn't in ERA5 at all, so closing the gap *requires independent observations*. A
small-gain experiment that decisively redirects strategy is worth as much as a
big-gain one. (Physics it did find: dry clear afternoons → bias grows; windy
afternoons → bias shrinks. Real but tiny.)
Dig deeper: irreducible error / aleatoric vs epistemic uncertainty; knowing when
more *features* won't help and you need more *data*.

## K. Satellite thermal & honest uncertainty

**S30 — What satellite "temperature" actually is (and isn't).** Thermal EO does not
measure air temperature. Four caveats everyone should carry: (a) it's **skin/land-
surface temperature** (radiating surface), not 2 m air temp — can differ 10–25 °C at
midday; (b) **clear-sky only** — clouds block thermal IR, silently biasing the record
toward cloud-free days; (c) **overpass snapshots**, not continuous — the diurnal cycle
is undersampled; (d) a hard **resolution-vs-revisit tradeoff** (Landsat 100 m / 16-day
vs MODIS 1 km / daily). *Most users misread satellite maps as continuous air temp;
correcting that — communicating the variance — is a core BOWG value, not a footnote.*
Dig deeper: land surface temperature (LST) retrieval, emissivity & atmospheric
correction, skin-vs-air-temperature relationship; sun-synchronous overpass sampling.

---

*Next topics likely to land here: leave-one-station-out validation, FastAPI `/point`,
AERONET dust, ERA5↔satellite↔station fusion.*
