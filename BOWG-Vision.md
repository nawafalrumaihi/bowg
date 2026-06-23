# BOWG — Vision

*Why this project exists, in one image and one number.*

> **Bahrain is a pearl hidden in the satellite oyster.**

The world's standard climate grid (ERA5, 0.25°, ~25 km) cannot see Bahrain. The
island is smaller than a single pixel — one grid cell (~700 km²) is nearly the
area of the whole country (~786 km²), and Bahrain is narrower E–W than the grid is
wide. So the cell that should be "Bahrain" is 82–95% Gulf water, and the data
takes on the sea's personality: cool, humid, flat across the day. The island's
real climate — hot, dry, with a fierce desert day/night swing — vanishes into the
shell.

We measured the gap, we didn't guess it: on a July afternoon the real airport
thermometer read **44 °C** where ERA5 said **36 °C**. An **8 °C hole**, sitting
unremarked in the data source most people trust, for an entire nation.

That is the closed oyster. BOWG is the diver.

## The pearl, and the tools that reveal it

No single instrument opens the shell. The pearl appears only when three sources
are fused, each covering the others' blindspot:

- **Reanalysis (ERA5)** gives us *when* — continuous in time, every variable —
  but is blind in space at this scale.
- **Ground stations** (the airport, and Bahrain's own observation network — the
  "moat") give us *the true air temperature* — but only at a handful of points.
- **Satellite thermal imagery** (Landsat, Sentinel-3, ECOSTRESS, MODIS/VIIRS, and
  Bahrain's own sovereign satellites) gives us *where* — the spatial pattern
  across the island at 70 m–1 km — but as surface skin temperature, in clear-sky
  snapshots.

ERA5 knows the clock. Stations know the truth. Satellites know the map. Braided
together — honestly, with uncertainty carried the whole way — they reconstruct
the climate of a place the global products structurally cannot resolve.

There is poetry in the means as well as the end: Bahrain's heritage is pearling
(UNESCO-listed — *Pearling, Testimony of an Island Economy*). The pearl was always
in the water. It just took the right diver, and the right tools, to bring it up.

## What BOWG is — and isn't

**Is:** an **open, reality-corrected weather-data platform for Bahrain and the
forkable Gulf** — the most accurate picture a Bahraini can get from global
sources, because the global numbers are corrected against local reality before
they're served. Open-source and citable underneath (the legacy-grade DNA), with
a friendly public face on top. Scientists can cite it, students can learn from
it, neighbours can fork it — *and* an ordinary person in Manama can just read it.

**Isn't:** a claim of magic. "Solving the cell" means *skillful, uncertainty-
quantified* estimates grounded in real observation — not invented precision. The
honesty is the point; it's what makes it both citable and trustworthy.

## The product, restated (2026-06-23 repositioning)

Three influences, three layers:

- **Open-Meteo → the access model.** Free, open, API-first, no gatekeeping. How
  the data reaches people. *This is the center of gravity:* BOWG is a data
  platform first; apps and visualisations are built on top.
- **Earth Nullschool → the experience.** The legible, beautiful Gulf weather map.
  The aspiration for the consumer face — but a *later* phase, not the starting
  point. The differentiator is in the data, not the pixels.
- **"Reality mixed in" → the moat.** Open-Meteo and Earth Nullschool both serve
  *raw global model data*. Neither corrects to local ground truth. BOWG does —
  we measured the 8 °C hole and we close it against real Bahraini observation.
  That correction is the only thing here nobody else is doing.

A note on honesty that the framing must carry: reanalysis (ERA5) is the
*calibration brain and historical climatology* — where the Bahrain correction is
learned — **not** a live forecast. "Most accurate" is provable as *more accurate
than the uncorrected global apps*, and today is firmest at the airport
(Muharraq), where we have ground truth; the island interior remains an
uncertainty-quantified estimate until more local observation exists. We say that
out loud. See [[DECISIONS]] (2026-06-23 reposition entry).

## The blindspot is not just Bahrain's

Every small island, coastal city, and wadi narrower than ~25 km is invisible to
the standard grid, worldwide. Bahrain is simply a whole country that falls
through — which makes it the cleanest possible demonstration of a global problem,
and a template anyone in the Gulf can fork.

---

*Grounded in measured results — see [[BOWG-Phase0-Findings]] and [[EXPERIMENTS]].
This doc is the "why"; those are the "how we know."*
