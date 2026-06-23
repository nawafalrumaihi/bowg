"""E03 — ARCO-ERA5 public-Zarr verification (reconstructed 2026-06-23).

Opens Google's public ARCO-ERA5 Zarr anonymously and pulls the Bahrain grid
cell's 2m temperature for 15-22 Jul 2023. Phase 0 (E03) recorded 36.1 C here,
matching the bespoke CDS pull to -0.04 C. This script is the reproducible spine
of BOWG's chosen ingestion path (see DECISIONS.md: consume ARCO, don't build a
NetCDF->Zarr pipeline). No GCP account required.

Reproduce:  .venv/bin/python phase0/verify_arco_era5.py
Expected:   Bahrain cell peak ~36.1 C, grid point ~26.00 N / 50.50 E.
"""

import xarray as xr

# Public ARCO-ERA5 store: full ERA5, regridded to uniform 0.25 deg, anonymous read.
ARCO_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

# Bahrain cell + the canonical Phase 0 validation window (a hot July week).
BAHRAIN_LAT = 26.0          # ERA5 0.25 deg grid node nearest Manama
BAHRAIN_LON = 50.5          # ERA5 longitudes run 0-360, so 50.5 is as-is
WINDOW = slice("2023-07-15", "2023-07-22")


def main() -> None:
    import time

    t0 = time.time()
    ds = xr.open_zarr(ARCO_URL, storage_options={"token": "anon"}, chunks=None)
    print(f"opened ARCO-ERA5 in {time.time() - t0:.1f}s ({len(ds.data_vars)} variables)")

    t2m = ds["2m_temperature"].sel(time=WINDOW)
    cell = t2m.sel(latitude=BAHRAIN_LAT, longitude=BAHRAIN_LON, method="nearest")
    cell_c = cell.values - 273.15  # K -> C

    print(f"grid point: {float(cell.latitude):.2f} N, {float(cell.longitude):.2f} E")
    print(f"window:     {WINDOW.start} .. {WINDOW.stop}  ({cell_c.size} hourly steps)")
    print(f"peak 2m T:  {cell_c.max():.2f} C")
    print(f"min  2m T:  {cell_c.min():.2f} C")
    print(f"mean 2m T:  {cell_c.mean():.2f} C")


if __name__ == "__main__":
    main()
