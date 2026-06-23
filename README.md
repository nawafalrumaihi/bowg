# BOWG — Bahrain Open Weather Gateway

An open, **reality-corrected** weather-data platform for Bahrain and the Gulf: the most accurate picture you can get from global sources, because the global numbers are corrected against local ground truth before they're served. API-first and citable underneath (forkable by other Gulf states, citable by scientists), with a public Bahraini-facing layer on top. See [`BOWG-Vision.md`](BOWG-Vision.md) for the repositioning.

**Status:** Phase 1 MVP working — reality-corrected `/point` API serves raw + corrected ERA5 from ARCO, with the hour-of-day OBBI correction (test RMSE 3.60 → 1.44 °C, out-of-sample) and honest scope. ✓ 2026-06-23
**Phase:** 2 (next) — durability + go public: cron/freshness, second variable, cheap VPS, open API docs.

**Run it:** `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt`, then `.venv/bin/uvicorn phase1.api:app` → `GET /point?lat=26.0&lon=50.5&time=2023-07-19T13:00:00Z`. (First train the model: see [`ROADMAP.md`](ROADMAP.md) Phase 1.)

## Why this exists

The Gulf is data-poor in global climate models: GFS at 0.25° (~25km) cannot see Bahrain's micro-climates (the island is ~50km across), no open portal exists for historical Gulf weather, and the region is warming faster than the global average. Commercial APIs gate access. BOWG is the open alternative.

## Map of docs in this folder

- [`BOWG-Vision.md`](BOWG-Vision.md) — why this exists, in one image and one number ("a pearl hidden in the satellite oyster").
- [`BOWG-Data-Strategy.md`](BOWG-Data-Strategy.md) — getting gatekept ground-truth realistically: models first (open data + satellite + honest variance), SCE via the maintainer's direct relationship.
- [`BOWG-Phase0-Findings.md`](BOWG-Phase0-Findings.md) — Phase 0 story: the six data layers and what they taught (start here for the ERA5 findings).
- [`STUDYLIST.md`](STUDYLIST.md) — living curriculum: every concept we hit, with "dig deeper" pointers. The science-soak companion.
- [`EXPERIMENTS.md`](EXPERIMENTS.md) — lab notebook: one entry per experiment (question → method → result → verdict), reproducible. The evidence trail.
- [`ROADMAP.md`](ROADMAP.md) — re-sequenced phase plan (post-repositioning) with exit criteria.
- [`BOWG-Summary.md`](BOWG-Summary.md) — current planning summary.
- [`Bahrain-Open-Weather-Gateway.md`](Bahrain-Open-Weather-Gateway.md) — original blueprint (full).
- [`BOWG.md`](BOWG.md) — earlier project doc.
- [`BOWG-Study-Roadmap.md`](BOWG-Study-Roadmap.md) — study roadmap.
- [`research/`](research/) — exploratory notes (e.g. Earth Nullschool reference).
- [`CLAUDE.md`](CLAUDE.md) — AI-session conventions.
- [`DECISIONS.md`](DECISIONS.md) — ADR-lite design log.
- [`LOG.md`](LOG.md) — chronological session log.

This folder is part of an Obsidian vault, so Obsidian wikilinks (e.g. `[[BOWG-Summary]]`) also resolve.

## Phase tracker

Re-sequenced for the 2026-06-23 repositioning (open reality-corrected data platform, API-first). Full detail + exit criteria in [`ROADMAP.md`](ROADMAP.md).

- [x] **Phase 0** — Prove the gap: ERA5 pulled, validated, +8 °C blindspot measured. ✓ 2026-05-22 (spine rebuilt 2026-06-23)
- [x] **Phase 1** — Reality-corrected `/point` API (MVP): ARCO-ERA5 + OBBI hour-of-day correction → FastAPI, raw + corrected + honest scope. ✓ 2026-06-23 (RMSE 3.60→1.44 °C OOS)
- [ ] **Phase 2** — Durability + go public: cron/freshness, second variable, cheap VPS, open API docs. ← next
- [ ] **Phase 3** — Consumer face: minimal Bahraini-friendly read-out + Heat Index.
- [ ] **Phase 4** — The moat: spatial ground truth (SCE / extra METAR / satellite fusion) → interior correction.
- [ ] **Phase 5** — Forecast layer: add GFS/IFS, apply the correction → reality-corrected forecast + richer viz.
- [ ] **Phase 6** — One real external user (the north star).

## How to resume with Claude

1. Read `CLAUDE.md` (project conventions for AI sessions).
2. Read `LOG.md` (what was done last, what's next).
3. Read `DECISIONS.md` before proposing architecture changes.
4. Ask before adding any dependency or service.

To start a session: tell Claude "BOWG Phase N" and point at this directory.
