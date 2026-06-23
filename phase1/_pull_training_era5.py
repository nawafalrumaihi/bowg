"""One-time: cache ARCO-ERA5 2m temperature at the OBBI cell for JJA 2022+2023.

ARCO's chunk-1 store is slow for long point series (E03 caveat) but reliable
eager. We pull once and cache to NetCDF so training/validation read locally.
The API serves single-time queries from ARCO directly (cheap), so this slow path
is training-only. Output is gitignored (*.nc).

Run:  .venv/bin/python phase1/_pull_training_era5.py
"""

import time
import pathlib
import xarray as xr

ARCO_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
LAT, LON = 26.0, 50.5  # the verified Bahrain ERA5 0.25 deg cell (sea-dominated)
OUT = pathlib.Path("phase1/cache/era5_obbi_cell_jja_2022_2023.nc")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ds = xr.open_zarr(ARCO_URL, storage_options={"token": "anon"}, chunks=None)
    pt = ds["2m_temperature"].sel(latitude=LAT, longitude=LON, method="nearest")
    pieces = []
    for yr in (2022, 2023):
        t0 = time.time()
        s = pt.sel(time=slice(f"{yr}-06-01", f"{yr}-08-31")).load()
        print(f"JJA {yr}: {s.size} hrs in {time.time()-t0:.0f}s", flush=True)
        pieces.append(s)
    out = xr.concat(pieces, dim="time").rename("t2m_era5_K")
    out.to_netcdf(OUT)
    print(f"cached -> {OUT} ({out.size} hourly steps, "
          f"grid {float(out.latitude):.2f}N/{float(out.longitude):.2f}E)", flush=True)


if __name__ == "__main__":
    main()
