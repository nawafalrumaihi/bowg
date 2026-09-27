"""Smoke test for the /point API. Confirms the reality correction actually fires
and pulls the sea-smeared ERA5 value toward the real Bahrain airport reading.

Run (after training):  .venv/bin/python phase1/smoke_test.py
"""

from fastapi.testclient import TestClient
from phase1.api import app

# 2023-07-19 13:00 UTC at the OBBI cell: E06 measured ERA5 ~36 C vs OBBI ~44 C.
HOT = {"lat": 26.0, "lon": 50.5, "time": "2023-07-19T13:00:00Z"}
FAR = {"lat": 48.0, "lon": 2.0, "time": "2023-07-19T13:00:00Z"}  # Paris: out of domain


def main() -> None:
    with TestClient(app) as c:
        r = c.get("/point", params=HOT).json()
        print("OBBI cell:", r)
        assert r["corrected_C"] is not None, "correction should apply at OBBI cell"
        assert r["corrected_C"] > r["raw_C"], "ERA5 is cool-biased; correction must warm it"
        assert 38 < r["corrected_C"] < 48, f"corrected {r['corrected_C']} not near reality"
        assert r["data_tier"] == "final", "2023 is final ERA5, not preliminary"

        f = c.get("/point", params=FAR).json()
        print("Out of domain:", f)
        assert f["corrected_C"] is None, "must not fake a correction outside calibration"

        bad = c.get("/point", params={**HOT, "time": "not-a-date"})
        assert bad.status_code == 422, "bad time should 422"

        # The ARCO time axis is pre-allocated to 2050; unwritten slots must 404,
        # never 200-with-nulls. Same for before ERA5 begins (1940).
        for t in ("2049-07-19T13:00:00Z", "1920-07-19T13:00:00Z"):
            hole = c.get("/point", params={**HOT, "time": t})
            assert hole.status_code == 404, f"{t} has no data; should 404"
            assert "availability" in hole.json()["detail"], "404 should say what exists"

    print("\nOK — correction fires at OBBI, abstains elsewhere, validates input, "
          "refuses times with no data.")


if __name__ == "__main__":
    main()
