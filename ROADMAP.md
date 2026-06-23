# BOWG — Roadmap

Re-sequenced for the 2026-06-23 repositioning: **an open, reality-corrected
reanalysis data platform, API-first, keeping the open/citable DNA with a consumer
face on top.** See [[BOWG-Vision]] (why) and [[DECISIONS]] (the reposition entry +
locked choices). Phases beyond Phase 1 are **provisional** — direction, not
commitment; validate each before building.

**Through-line:** every phase must serve a reality-corrected number, honestly
labelled. The correction *is* the product; the rest is delivery.

---

## Phase 0 — Prove the gap (DONE ✓ 2026-05-22)

ERA5 pulled, validated, and the Bahrain blindspot *measured*, not guessed: the
0.25° cell reads 36 °C where the real airport reads 44 °C (+8 °C). Hour-of-day
correction gets OBBI to 1.2 °C RMSE out-of-sample (E08); ERA5's own fields can't
explain the residual (E09) → the missing signal is external. Spine reconstructed
2026-06-23 (`phase0/verify_arco_era5.py`, ARCO-ERA5 read verified).

## Phase 1 — Reality-corrected `/point` API (MVP) — DONE ✓ 2026-06-23

The smallest honest version of the entire pitch: one variable, one corrected
number, served openly. **Built and verified:**

- `phase1/api.py` — FastAPI `/point` reads 2m temperature for the queried
  point/time live from ARCO-ERA5 and returns **raw + corrected + honest scope**.
- `phase0/fetch_obbi_metar.py` — OBBI ground-truth fetcher rebuilt (E06 code was
  lost; method preserved). `phase1/train_correction.py` — hour-of-day bias model
  rebuilt (E08), **test RMSE 3.60 → 2.52 → 1.44 °C out-of-sample** (train JJA 2022
  / test JJA 2023); 24 offsets saved to `correction_obbi_hourofday.json`.
- Honest scope enforced: the correction fires only inside the OBBI calibration
  cell and **abstains** (`corrected_C: null`) elsewhere — no faked precision.
- Stack stayed within ceiling + the FastAPI runtime trio (uvicorn/httpx) and
  `requirements.txt` pinned for recovery. `phase1/smoke_test.py` passes.

**Exit met:** `GET /point?lat=..&lon=..&time=..` returns a corrected value with
its uncertainty stated — demonstrably more accurate than the uncorrected global
apps (the provable claim). *Known MVP limits:* one variable; calibrated/served at
the OBBI cell only; climatological correction misses day-specific synoptic
extremes (the ~1.4 °C residual is that miss, stated).

## Phase 2 — Durability + go public (provisional)

Make Phase 1 dependable and open it to the world.

- Freshness/cron ingestion (cron until cron breaks — no Airflow), freshness
  checks, deploy to one cheap VPS.
- Second variable: dewpoint/humidity (unlocks Heat Index later; also the
  marine-contamination signal is largest here).
- Public API docs + open licence. This is the "Open-Meteo democratization" layer.

## Phase 3 — The consumer face (provisional)

First sliver of the Earth Nullschool *experience* — but read-out before map.

- A minimal, Bahraini-friendly page: "the real temperature right now / today,"
  corrected, with the honesty stated plainly.
- First derived product: **Heat Index / WBGT** (matters here — wrong humidity
  from the sea-smear makes uncorrected "feels-like" badly wrong).
- Front-end deps deferred to here, each via a DECISIONS entry.

## Phase 4 — The moat: spatial ground truth (provisional)

Move correction beyond OBBI to the island interior — the actual research core and
the thing nobody else has.

- Spatial anchors: SCE met-data request (the warm channel), additional METAR
  (E10b), and satellite thermal (E11 → E12 fusion: ERA5 + stations + satellite).
- Enables leave-one-station-out validation and an uncertainty-quantified interior
  field — not just a single corrected point.
- New deps expected (`pystac-client`/`odc-stac` for E11; `sklearn`/XGBoost for
  E12) — each gated on its own decision.

## Phase 5 — Forecast layer (provisional)

Turn "accurate history" into "accurate tomorrow."

- Add a live forecast source (GFS/IFS) — the first non-reanalysis source.
- Apply the ERA5-learned correction to the forecast → **reality-corrected
  forecast**, the consumer-facing payoff.
- Richer visualisation (the fuller Earth Nullschool experience).

## Phase 6 — One real external user (the north star)

Someone in Bahrain who isn't the maintainer relies on it. Everything above is in
service of this.

---

*Honesty bounds (hard constraints, carried from [[DECISIONS]]):* "most accurate"
means *more accurate than the uncorrected global apps* — provable — and is
firmest at Muharraq, temporally, until Phase 4 brings spatial ground truth. The
interior is an uncertainty-quantified estimate, said out loud, never invented
precision.
