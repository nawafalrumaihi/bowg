"""BOWG Phase 1 — reality-corrected /point API (MVP).

Serves ERA5 0.25 deg 2m temperature for a point/time, read live from public
ARCO-ERA5, and corrected toward true Bahrain air temperature using the
hour-of-day model trained at OBBI (phase1/train_correction.py). Every response
carries both the raw and corrected value plus the honest scope of the correction
-- the smallest faithful version of the whole BOWG pitch.

Run:  .venv/bin/uvicorn phase1.api:app --reload
Then: GET /point?lat=26.0&lon=50.5&time=2023-07-19T13:00:00Z
"""

import json
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
from fastapi import FastAPI, HTTPException, Query

ARCO_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
MODEL_PATH = pathlib.Path(__file__).with_name("correction_obbi_hourofday.json")
GRID_RES = 0.25  # ERA5 cell size; within half a cell == same cell

app = FastAPI(
    title="BOWG — Bahrain Open Weather Gateway",
    description="Open, reality-corrected reanalysis temperature for Bahrain/the Gulf.",
    version="0.1.0",
)
_state: dict = {}


def _coverage(attrs: dict) -> dict:
    """Data availability from the store's own metadata.

    The ARCO time axis is pre-allocated (1900-2050) and unwritten slots read as
    NaN, so the axis alone says nothing about what exists. The `valid_time_*`
    attrs do; each stop date is inclusive (data runs through its 23:00).
    Read once at startup, so a long-running server under-claims newer data --
    the safe direction.
    """
    day = pd.Timedelta(days=1)
    return {
        "start": pd.Timestamp(attrs["valid_time_start"], tz="UTC"),
        "final_end": pd.Timestamp(attrs["valid_time_stop"], tz="UTC") + day,
        "era5t_end": pd.Timestamp(attrs["valid_time_stop_era5t"], tz="UTC") + day,
        "store_last_updated": attrs.get("last_updated"),
    }


@app.on_event("startup")
def _load() -> None:
    _state["ds"] = xr.open_zarr(ARCO_URL, storage_options={"token": "anon"}, chunks=None)
    _state["cov"] = _coverage(_state["ds"].attrs)
    _state["model"] = json.loads(MODEL_PATH.read_text())


def _availability() -> dict:
    cov = _state["cov"]
    last = pd.Timedelta(hours=1)
    return {
        "first_time": cov["start"].isoformat(),
        "last_final_time": (cov["final_end"] - last).isoformat(),
        "last_preliminary_time": (cov["era5t_end"] - last).isoformat(),
        "store_last_updated": cov["store_last_updated"],
    }


@app.get("/")
def root() -> dict:
    m = _state["model"]
    return {
        "service": "BOWG /point — reality-corrected ERA5 for Bahrain",
        "data_source": "ARCO-ERA5 (ECMWF reanalysis, 0.25 deg)",
        "correction": f"{m['model']} calibrated at {m['calibrated_against']}",
        "uncertainty_rmse_C": m["uncertainty_rmse_C"],
        "availability": _availability(),
        "try": "/point?lat=26.0&lon=50.5&time=2023-07-19T13:00:00Z",
    }


@app.get("/point")
def point(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=360),
    time: str = Query(..., description="ISO 8601 UTC, e.g. 2023-07-19T13:00:00Z"),
) -> dict:
    ds, model = _state["ds"], _state["model"]
    try:
        ts = pd.Timestamp(time)
        ts = ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
    except (ValueError, TypeError):
        raise HTTPException(422, f"could not parse time: {time!r}")

    cell = ds["2m_temperature"].sel(
        latitude=lat, longitude=lon % 360, time=ts.tz_localize(None), method="nearest")
    raw_c = round(float(cell.values) - 273.15, 2)
    g_lat, g_lon = float(cell["latitude"]), float(cell["longitude"]) % 360
    used_time = pd.Timestamp(cell["time"].values, tz="UTC")

    # Never serve a hole: outside the written range (or any stray NaN) is a 404
    # that says what does exist, not a 200 with nulls.
    cov = _state["cov"]
    if not (cov["start"] <= used_time < cov["era5t_end"]) or np.isnan(cell.values):
        raise HTTPException(404, {"error": f"no ERA5 data for {used_time.isoformat()}",
                                  "availability": _availability()})
    tier = ("final" if used_time < cov["final_end"] else
            "preliminary (ERA5T) — may be revised when final ERA5 is released")

    # The correction is calibrated at the OBBI cell only; apply it solely there.
    cal = model["grid_cell"]
    in_domain = abs(g_lat - cal["lat"]) < GRID_RES / 2 and \
        abs(((g_lon - cal["lon"] + 180) % 360) - 180) < GRID_RES / 2

    result = {
        "query": {"lat": lat, "lon": lon, "time": ts.isoformat()},
        "grid_cell": {"lat": round(g_lat, 2), "lon": round(g_lon, 2),
                      "time_used": used_time.isoformat()},
        "raw_C": raw_c,
        "data_tier": tier,
        "source": "ARCO-ERA5 0.25 deg (raw reanalysis — sea-smeared over Bahrain)",
    }
    if in_domain:
        offset = model["hour_offsets_C"][str(used_time.hour)]
        result["corrected_C"] = round(raw_c - offset, 2)
        result["correction"] = {
            "applied_offset_C": offset, "hour_utc": used_time.hour,
            "model": model["model"], "uncertainty_rmse_C": model["uncertainty_rmse_C"],
            "scope": "validated at OBBI/Muharraq, temporally — trustworthy here",
        }
    else:
        result["corrected_C"] = None
        result["correction"] = {
            "applied_offset_C": None,
            "scope": ("outside the OBBI calibration cell — no validated correction "
                      "for this location yet (see ROADMAP Phase 4)."),
        }
    return result
