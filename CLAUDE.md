# CLAUDE.md — BOWG project conventions

This file orients an AI assistant joining a BOWG session. Read it first.

## Where this lives

This folder is inside an **Obsidian vault** at `~/Documents/Ideas/`. The user runs an agent (**HermesBrain**) over the vault to link concepts across notes. Implications:

- Files moving, being renamed, or being reorganized between sessions is **expected** — it's the user curating the vault, not a hook misfire. Investigate before "fixing."
- Prefer plain markdown and Obsidian-compatible filenames (no slashes or odd characters). Wikilinks like `[[BOWG-Summary]]` are fine and often preferable for cross-vault linking.
- The vault is backed up via its own mechanism (Obsidian sync / cloud). Git in this folder is a **second** backup layer for version history, not the primary store. Do not assume git is the only source of truth.

## Project state

This is a **planning-stage** project. As of 2026-05-22, no code exists. Default to discussion, design, and writing in markdown — not to scaffolding code or installing dependencies. Only start coding when the user explicitly says "Phase 0" / "Phase 1" / "let's build X".

## Reading order when resuming

1. `LOG.md` — what was done last, what's next.
2. `DECISIONS.md` — locked-in design choices and why.
3. `README.md` — phase tracker and links.
4. `BOWG-Summary.md` — full project context.

## Stack minimalism (hard rule)

Phase 1 stack ceiling: `cdsapi`, `xarray`, `zarr`, `fastapi`. Nothing else without a written decision in `DECISIONS.md`.

Do **not** add the following before they're causing real pain:
- Airflow — use cron until cron breaks
- Kubernetes — Docker Compose, or a single VPS, is enough
- Redis, TimescaleDB, GraphQL, WebSocket — all premature
- Prometheus / Grafana stack
- ORMs, migration tools, complex deps

Before adding any dependency, library, service, or piece of infrastructure: **ask first**. Justify in `DECISIONS.md` if accepted.

## Honesty notes (do not let the user forget)

- **0.25° will not resolve Bahrain micro-climates.** ERA5 native is the floor; downscaling is a real research project, not a checkbox.
- **ERA5 lag** is ~5 days for ERA5T (preliminary) and 2–3 months for the final reanalysis. The summary doc says "monthly with 2-month lag" — that's a simplification worth correcting in conversation.
- **Bahrain-specific data sources are unverified.** Bahrain Met Service, air quality, university stations — none confirmed accessible. This is the project's actual moat and the biggest unknown.
- **"Legacy-grade" + solo project is a tension.** Whatever ships needs to still have value if untouched for 2 years.

## Tone

- Be direct. Push back when an idea is bad. Don't sycophantically agree.
- Short responses. No filler, no recap of what was just done.
- Terminal-friendly markdown. No emojis unless the user uses them first.
- When discussing tradeoffs, give a recommendation — don't just list options.

## What to ask before deciding

- Anything that touches `DECISIONS.md`.
- Anything that adds a dependency or external service.
- Anything that involves data volume / storage commitments.
- Anything that locks in API schema before real users exist.
