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

**Is:** open-source, legacy-grade infrastructure that makes Bahrain (and the
forkable Gulf) *visible* in climate data — citable by scientists, learnable by
students, reusable by neighbours. A diver's toolkit, not another weather app.

**Isn't:** a claim of magic. "Solving the cell" means *skillful, uncertainty-
quantified* estimates grounded in real observation — not invented precision. The
honesty is the point; it's what makes it citable.

## The blindspot is not just Bahrain's

Every small island, coastal city, and wadi narrower than ~25 km is invisible to
the standard grid, worldwide. Bahrain is simply a whole country that falls
through — which makes it the cleanest possible demonstration of a global problem,
and a template anyone in the Gulf can fork.

---

*Grounded in measured results — see [[BOWG-Phase0-Findings]] and [[EXPERIMENTS]].
This doc is the "why"; those are the "how we know."*
