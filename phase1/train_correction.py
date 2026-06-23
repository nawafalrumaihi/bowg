"""Train BOWG's hour-of-day bias correction for the OBBI cell (reproduces E08).

Pairs ARCO-ERA5 0.25 deg 2m temperature (sea-smeared) against OBBI station obs
(true air temp), learns a per-hour-of-day mean-bias correction on JJA 2022, and
validates out-of-sample on JJA 2023. Saves the 24 offsets + validation metrics to
correction_obbi_hourofday.json -- the small, committed model artifact the API loads.

Inputs (run these first):
  .venv/bin/python phase1/_pull_training_era5.py   # caches ERA5 (slow, one-time)
  .venv/bin/python phase0/fetch_obbi_metar.py      # caches OBBI obs

Run:  .venv/bin/python phase1/train_correction.py
Expected (E08): test RMSE raw ~3.15 -> flat ~2.10 -> hour-of-day ~1.20 C.
"""

import json
import pathlib
import numpy as np
import pandas as pd
import xarray as xr

CACHE = pathlib.Path("phase1/cache")
ERA5_NC = CACHE / "era5_obbi_cell_jja_2022_2023.nc"
OBBI_CSV = CACHE / "obbi_jja_2022_2023.csv"
OUT = pathlib.Path("phase1/correction_obbi_hourofday.json")


def _rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


def main() -> None:
    era5 = xr.open_dataarray(ERA5_NC)
    era5_c = pd.Series(era5.values - 273.15,
                       index=pd.to_datetime(era5["time"].values, utc=True))
    obbi = pd.read_csv(OBBI_CSV, index_col=0)
    obbi.index = pd.to_datetime(obbi.index, utc=True)
    obbi_c = obbi["t2m_obbi_C"]

    df = pd.DataFrame({"era5": era5_c, "obbi": obbi_c}).dropna()
    df["bias"] = df["era5"] - df["obbi"]      # negative: ERA5 reads too cool
    df["hour"] = df.index.hour

    train = df[df.index.year == 2022]
    test = df[df.index.year == 2023]

    # Models learned on TRAIN only (no leakage).
    flat_offset = float(train["bias"].mean())
    hour_offset = train.groupby("hour")["bias"].mean()       # 24 values

    # Evaluate on TEST.
    test_flat = test["era5"] - flat_offset
    test_hod = test["era5"] - test["hour"].map(hour_offset).values
    metrics = {
        "rmse_raw_C": round(_rmse(test["era5"].values, test["obbi"].values), 3),
        "rmse_flat_C": round(_rmse(test_flat.values, test["obbi"].values), 3),
        "rmse_hourofday_C": round(_rmse(test_hod.values, test["obbi"].values), 3),
        "mae_raw_C": round(float(np.mean(np.abs(test["era5"] - test["obbi"]))), 3),
        "mae_hourofday_C": round(float(np.mean(np.abs(test_hod - test["obbi"]))), 3),
    }

    model = {
        "model": "hour_of_day_mean_bias",
        "variable": "2m_temperature",
        "units": "C",
        "convention": "corrected = era5_raw - offset[hour_utc]  (offset = mean(era5 - obbi))",
        "grid_cell": {"lat": float(era5["latitude"]), "lon": float(era5["longitude"])},
        "calibrated_against": "OBBI / Bahrain International Airport (Muharraq), Iowa Mesonet",
        "trained_on": "JJA 2022", "validated_on": "JJA 2023",
        "n_train": int(len(train)), "n_test": int(len(test)),
        "flat_offset_C": round(flat_offset, 3),
        "hour_offsets_C": {int(h): round(float(v), 3) for h, v in hour_offset.items()},
        "validation": metrics,
        "uncertainty_rmse_C": metrics["rmse_hourofday_C"],
        "honesty_note": (
            "Corrects the sea-smeared ERA5 0.25 deg cell toward true Bahrain air "
            "temperature using a climatological hour-of-day offset learned at OBBI. "
            "Validated temporally AT OBBI only; the residual RMSE is the stated "
            "uncertainty. Does not transfer to the ungauged island interior (E09)."
        ),
    }
    OUT.write_text(json.dumps(model, indent=2))

    print(f"paired hours: train {len(train)}, test {len(test)}")
    print(f"test RMSE  raw {metrics['rmse_raw_C']} -> flat {metrics['rmse_flat_C']} "
          f"-> hour-of-day {metrics['rmse_hourofday_C']} C")
    print(f"offset range: {min(model['hour_offsets_C'].values()):.2f} .. "
          f"{max(model['hour_offsets_C'].values()):.2f} C")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
