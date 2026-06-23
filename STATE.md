# STATE — BOWG

**Status:** Phase 0 complete → Phase 1 ready  
**Last active:** 2026-05-22 (wrap-up session)  
**Blocked on:** Nothing technical. Moat access = warm channel (maintainer's SCE relationship).  
**Next action:** Mirror Gulf subset from ARCO-ERA5 → local Zarr → FastAPI `/point`

---

## Phase 0 Deliverables (Complete ✓)

1. ERA5 pulled & validated — CDS NetCDF, xarray, triple-validated (±0.4°C)
2. Resolution ceiling proven — 0.25° cells 5-18% land over Bahrain
3. Ground truth found — OBBI METAR 44°C vs ERA5 36.1°C (8°C gap)
4. Moat accessible — 3/4 Bahrain sources open
5. Bias characterized — Missing diurnal cycle (−6.2°C at 2pm, +0.2°C at dawn)
6. Correction built — Hour-of-day 62% RMSE cut (3.15→1.20), out-of-sample
7. Residual proven external — ERA5's own variables explain only +5%
8. ARCO shortcut adopted — Public Zarr, 273 vars, 6.9s open
9. Vision crystallized — "Pearl in the satellite oyster" + three-source fusion
10. Strategy defined — Models-first + SCE warm channel

## Document Inventory

- [[BOWG-Vision]] — Why (pearl metaphor, three-source fusion)
- [[BOWG-Data-Strategy]] — How (models-first, SCE warm channel, satellite)
- [[BOWG-Phase0-Findings]] — Narrative (6 findings + 6 data layers)
- [[EXPERIMENTS]] — Lab notebook (E01–E11, reproducible)
- [[STUDYLIST]] — Living curriculum (30+ items)
- [[DECISIONS]] — Locked choices
- [[LOG]] — Session history
- [[README]] — Phase tracker + doc map

---

*Last updated: 2026-06-19 by Hermes -- generated graph reports retired from active context.*
