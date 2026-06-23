# BOWG — Data Access & Partnership Strategy

*How BOWG gets the ground-truth it needs when the holder gatekeeps it — realistically,
for a solo builder — and how the project itself becomes worth collaborating with.*

Context: Bahrain's local observation data (the "moat") is the project's biggest
asset and its hardest dependency. The Supreme Council for Environment (SCE) — a
semi-government scientific-reporting body the maintainer has worked with — holds
spatially-resolved station data ([[EXPERIMENTS]] E10: 5–7 located air-quality
stations likely logging temperature/RH/wind internally) but gatekeeps it. This doc
is the realistic plan for not being blocked by that.

---

## The realistic path: models first

BOWG advances **computationally**, on data we can already get: open reanalysis
(ERA5 / ERA5-Land), open airport observations (OBBI via Iowa Mesonet), and open
satellite thermal. The work is bias correction, downscaling, and multi-source
fusion — all solo-feasible, all shippable without anyone's permission. This is the
spine; everything else is upside.

Why models-first wins for a solo project:
- **It ships regardless.** No dependency on institutions or hardware.
- **It's where the momentum is.** E01–E10 already built a credible, honest evidence
  chain (measured 8 °C gap, validated corrections, a decisive negative result).
- **It's the credibility that earns collaboration.** A working, rigorous product is
  a far better argument to SCE than any request — see "warm channel" below.

---

## Satellite thermal — and explaining the variance (a core BOWG value)

Open thermal Earth-observation (Landsat ~100 m, ECOSTRESS ~70 m, Sentinel-3 / MODIS
/ VIIRS ~1 km) resolves Bahrain as distinct land and needs no permission — the
spatial pattern the 0.25° grid can't see ([[EXPERIMENTS]] E11). But its real value
to BOWG is paired with **honest communication of what it is and isn't**, because
satellite data is widely misunderstood (STUDYLIST S30):

- It's **skin** temperature (radiating surface), not 2 m air temp — can differ
  10–25 °C at midday.
- It's **clear-sky only** — clouds block thermal IR, silently biasing the record
  toward cloud-free days.
- It's **overpass snapshots**, not continuous — the diurnal cycle is undersampled.
- Hard **resolution-vs-revisit tradeoff** — fine *or* frequent, rarely both.

BOWG's differentiator is not just a number but the **variance around it** and a
correct account of what each source measures. Communicating uncertainty well is a
public good and the project's identity — the same discipline as the diurnal-swing
and residual work ([[EXPERIMENTS]] E07–E09).

---

## SCE: the warm channel (the realistic route to the moat)

The maintainer has worked with SCE and can talk to people there directly. That
personal, collaborative relationship — not a cold data request or a leverage play —
is the realistic path to the station data. When that conversation happens, make it
easy and prestigious to say yes:

- **Credit loudly** — their logo, attribution, "in partnership with SCE."
- **Offer reciprocity** — give something back: a QC / anomaly-detection tool for
  their air-quality network, or a public dashboard they get credit for.
- **Align with national framing** — Bahrain Economic Vision 2030, climate goals, the
  UNESCO pearling-heritage angle ([[BOWG-Vision]]). Make yes look like national good.
- **Keep the ask narrow** — not "your data" but "the temperature/RH already logged at
  your monitoring stations, for research." Specific is easy to grant.
- **Lead with honesty** — for a scientific body, BOWG's uncertainty-quantified,
  reproducible, no-overclaim ethos *is* the credibility. The honesty is the pitch.

The product comes first; the relationship makes it definitive.

---

## Routes around the front door

- **Academic channel** — University of Bahrain (the maintainer as alum, or partners)
  often gets data-sharing access the public can't; doubles as credibility.
- **WMO / GTS** — Bahrain Met is a WMO member; some obs already flow internationally
  (that's how OBBI reaches Iowa Mesonet). Map what's already escaping the gate.
- **Published aggregates** — Met Directorate monthly climate PDFs are public; a free
  national cross-check without asking anyone. Plus the open national monthly series
  ([[EXPERIMENTS]] E10, 2011–2025).

---

## Parked (not now): own sensor network

A citizen-style network of low-cost automated stations was considered and **shelved
as currently unrealistic**: instrumentation near the airport is a security
non-starter, co-location calibration against OBBI isn't feasible, and a solo
deployment + maintenance burden isn't justified yet. Kept on record only as a
*someday-with-partners* idea — there is precedent for citizen sensors feeding
official systems (CWOP → NOAA, PurpleAir → US EPA) — but it is **not** part of the
current plan. Models first.

---

## The play, in one line

Build the open-data + satellite fusion to a credible, honest, uncertainty-quantified
state — models first, no permission needed — and let that working product, plus the
maintainer's direct SCE relationship, be what opens the door to the moat.

---

*Companion to [[BOWG-Vision]] (the why) and [[DECISIONS]] (locked choices). Revisit
before any institutional outreach.*
