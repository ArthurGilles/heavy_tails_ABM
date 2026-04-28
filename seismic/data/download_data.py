# Download earthquake data from USGS

import io
import logging
from urllib.parse import urlencode

import pandas as pd
import requests

logger = logging.getLogger(__name__)

_USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def download_usgs_catalog(
    min_magnitude=2.0,
    start="2000-01-01",
    end="2024-01-01"):
    # Download USGS earthquake catalog, cache result to CSV
    import os

    cache_path = os.path.join(os.path.dirname(__file__), "usgs_catalog.csv")
    if os.path.exists(cache_path):
        logger.info("Loading USGS catalog from cache: %s", cache_path)
        df = pd.read_csv(cache_path, parse_dates=["time"])
        return df

    logger.info(
        "Downloading USGS catalog: M>=%.1f from %s to %s",
        min_magnitude, start, end)

    # Split into quarterly chunks to stay under the USGS 20 000-event limit.
    # Do NOT include orderby — it triggers HTTP 400 on large result sets.
    start_dt = pd.Timestamp(start)
    end_dt = pd.Timestamp(end)
    chunks = []

    n_chunks = int((end_dt - start_dt).days / 91) + 1
    current = start_dt
    i_chunk = 0
    while current < end_dt:
        next_chunk = min(current + pd.DateOffset(months=3), end_dt)
        i_chunk += 1
        print(f"  Downloading chunk {i_chunk}/{n_chunks}: {current.date()} → {next_chunk.date()}", flush=True)
        params = {
            "format": "csv",
            "starttime": current.strftime("%Y-%m-%d"),
            "endtime": next_chunk.strftime("%Y-%m-%d"),
            "minmagnitude": min_magnitude}
        url = _USGS_BASE_URL + "?" + urlencode(params)
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            chunk = pd.read_csv(io.StringIO(resp.text))
            if not chunk.empty:
                chunks.append(chunk)
        except Exception as exc:
            logger.warning("  Failed to fetch chunk: %s", exc)
        current = next_chunk

    if not chunks:
        raise RuntimeError("No data downloaded from USGS.")

    df_raw = pd.concat(chunks, ignore_index=True)

    # keep only needed columns, rename for consistency
    col_map = {}
    for col in df_raw.columns:
        cl = col.lower()
        if cl == "time":
            col_map[col] = "time"
        elif cl in ("lat", "latitude"):
            col_map[col] = "latitude"
        elif cl in ("lon", "longitude"):
            col_map[col] = "longitude"
        elif cl in ("mag", "magnitude"):
            col_map[col] = "magnitude"

    df = df_raw.rename(columns=col_map)[["time", "latitude", "longitude", "magnitude"]]
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df = df.dropna(subset=["magnitude"]).reset_index(drop=True)

    # save to cache
    df.to_csv(cache_path, index=False)
    logger.info("Saved USGS catalog to %s (%d events)", cache_path, len(df))

    return df
