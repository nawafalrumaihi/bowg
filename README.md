# BOWG — Bahrain Open Weather Gateway

An open, **reality-corrected** weather-data platform for Bahrain and the Gulf: the most accurate picture you can get from global sources, because the global numbers are corrected against local ground truth before they're served. API-first and citable underneath (forkable by other Gulf states, citable by scientists), with a public Bahraini-facing layer on top. See [`BOWG-Vision.md`](BOWG-Vision.md) for the repositioning.

**Status:** Phase 0 done — gridded ERA5 pulled, opened in xarray, validated against an independent ERA5 point (+0.4°C).
**Phase:** 1 (not started) — one source/one variable/one region → Zarr → FastAPI `/point`.

## Why this exists

The Gulf is data-poor in global climate models: GFS at 0.25° (~25km) cannot see Bahrain's micro-climates (the island is ~50km across), no open portal exists for historical Gulf weather, and the region is warming faster than the global average. Commercial APIs gate access. BOWG is the open alternative.

## Map of docs in this folder

- [`BOWG-Vision.md`](BOWG-Vision.md) — why this exists, in one image and one number ("a pearl hidden in the satellite oyster").
- [`BOWG-Data-Strategy.md`](BOWG-Data-Strategy.md) — getting gatekept ground-truth realistically: models first (open data + satellite + honest variance), SCE via the maintainer's direct relationship.
- [`BOWG-Phase0-Findings.md`](BOWG-Phase0-Findings.md) — Phase 0 story: the six data layers and what they taught (start here for the ERA5 findings).
- [`STUDYLIST.md`](STUDYLIST.md) — living curriculum: every concept we hit, with "dig deeper" pointers. The science-soak companion.
- [`EXPERIMENTS.md`](EXPERIMENTS.md) — lab notebook: one entry per experiment (question → method → result → verdict), reproducible. The evidence trail.
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

- [x] **Phase 0** — One ERA5 file on disk, opened in xarray, values sanity-checked. ✓ 2026-05-22
- [ ] **Phase 1** — End-to-end MVP: one source, one variable, one region, Zarr → FastAPI `/point` endpoint. ← next
- [ ] **Phase 2** — Durability: second variable, cron, freshness checks, deploy to one cheap VPS.
- [ ] **Phase 3** — Second source (MERRA-2 aerosols) + first derived product (Heat Index) + minimal viz.
- [ ] **Phase 4** — Bahrain-specific data sources (the actual moat).
- [ ] **Phase 5** — One real external user.

## How to resume with Claude

1. Read `CLAUDE.md` (project conventions for AI sessions).
2. Read `LOG.md` (what was done last, what's next).
3. Read `DECISIONS.md` before proposing architecture changes.
4. Ask before adding any dependency or service.

To start a session: tell Claude "BOWG Phase N" and point at this directory.
