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

## Phase 1 — Reality-corrected `/point` API (MVP) ← NEXT

The smallest honest version of the entire pitch: one variable, one corrected
number, served openly.

- Read 2m temperature for the Bahrain cell from ARCO-ERA5 (spine — done).
- **Rebuild the OBBI correction** (lost with the old code): `fetch_obbi_metar`
  (Iowa Mesonet) + the hour-of-day bias model from E08.
- FastAPI `/point` endpoint returning **raw + corrected** temperature, with the
  correction method and its honest scope in the response (`corrected_at:
  "OBBI/Muharraq, temporal"`).
- Stack stays within the ceiling: `cdsapi`/`xarray`/`zarr`/`fastapi` + `gcsfs`.

**Exit:** `GET /point?lat=..&lon=..&time=..` returns a corrected value a human can
trust, with its uncertainty stated. This is shippable and demonstrably more
accurate than the uncorrected global apps — the provable claim.

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
