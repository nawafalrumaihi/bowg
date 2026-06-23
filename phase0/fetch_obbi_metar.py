"""OBBI (Bahrain International Airport, Muharraq) hourly air temperature from the
Iowa Environmental Mesonet ASOS archive. Key-free URL API, decades of hourly data.

OBBI is BOWG's adopted ground-truth / calibration reference (DECISIONS 2026-05-22):
a real Bahraini thermometer reading true island air temperature, against which the
sea-smeared ERA5 0.25 deg cell is corrected. Reconstructed 2026-06-23 (E06 code
was lost with the drive; method preserved in EXPERIMENTS.md E06).

Used as a library by phase1/train_correction.py; runnable standalone to cache obs.
"""

import io
import pathlib
import requests
import pandas as pd

MESONET_URL = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
STATION = "OBBI"


def fetch_obbi(start_date: str, end_date: str) -> pd.Series:
    """Hourly-ish OBBI air temperature (deg C), indexed by UTC timestamp.

    start_date / end_date are 'YYYY-MM-DD' (end exclusive at Mesonet's boundary;
    pass the day after your last wanted day). Returns the raw observation series
    (sub-hourly METAR cadence); use to_hourly() to align onto ERA5's hourly grid.
    """
    sy, sm, sd = start_date.split("-")
    ey, em, ed = end_date.split("-")
    params = {
        "station": STATION, "data": "tmpc",
        "year1": sy, "month1": sm, "day1": sd,
        "year2": ey, "month2": em, "day2": ed,
        "tz": "Etc/UTC", "format": "onlycomma",
        "latlon": "no", "missing": "M", "trace": "T", "direct": "no",
    }
    r = requests.get(MESONET_URL, params=params, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), na_values=["M", "T"])
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    s = df.set_index("valid")["tmpc"].dropna()
    s.name = "t2m_obbi_C"
    return s


def to_hourly(obs: pd.Series, tolerance_min: int = 30) -> pd.Series:
    """Snap sub-hourly obs onto the top-of-hour grid (nearest ob within tolerance).

    Matches ERA5's hourly, on-the-hour UTC stamps so the two can be paired for
    bias correction without interpolation artefacts.
    """
    hours = pd.date_range(obs.index.min().ceil("h"), obs.index.max().floor("h"),
                          freq="h", tz="UTC")
    snapped = obs.reindex(hours, method="nearest",
                          tolerance=pd.Timedelta(minutes=tolerance_min))
    return snapped.dropna()


def main() -> None:
    out = pathlib.Path("phase1/cache/obbi_jja_2022_2023.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = []
    for yr in (2022, 2023):
        raw = fetch_obbi(f"{yr}-06-01", f"{yr}-09-01")
        hourly = to_hourly(raw)
        print(f"OBBI JJA {yr}: {len(raw)} raw obs -> {len(hourly)} hourly; "
              f"peak {hourly.max():.1f}C")
        frames.append(hourly)
    series = pd.concat(frames)
    series.to_csv(out)
    print(f"cached -> {out} ({len(series)} hourly obs)")


if __name__ == "__main__":
    main()
