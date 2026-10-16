"""Binance USD-M perpetual funding rate collection and loading.

Funding settles on the position held at the funding timestamp. The backtest
layer is responsible for assigning each funding event to the holding interval
that contains it; this module only collects and loads raw events.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import polars as pl

from research.crypto_stat_arb.binance_ohlc import (
    BINANCE_FAPI_BASE_URL,
    _request_json,
    parse_utc_ms,
)

FUNDING_SCHEMA = {
    "timestamp": pl.Datetime(time_unit="ms", time_zone="UTC"),
    "symbol": pl.String,
    "funding_rate": pl.Float64,
}


def fetch_funding_history(
    symbol: str,
    *,
    start: str = "2023-01-01",
    end: str | None = None,
    base_url: str = BINANCE_FAPI_BASE_URL,
    request_sleep_seconds: float = 0.15,
) -> list[dict[str, Any]]:
    """Fetch all funding rate events for one USD-M futures symbol."""
    start_ms = parse_utc_ms(start)
    end_ms = parse_utc_ms(end)
    if start_ms is None:
        raise ValueError("start must be a date or datetime")

    rows: list[dict[str, Any]] = []
    cursor = start_ms
    while True:
        params: dict[str, Any] = {
            "symbol": symbol,
            "limit": 1000,
            "startTime": cursor,
        }
        if end_ms is not None:
            params["endTime"] = end_ms
        batch = _request_json("/fapi/v1/fundingRate", params=params, base_url=base_url)
        if not batch:
            break
        rows.extend(batch)
        last_funding_ms = int(batch[-1]["fundingTime"])
        next_cursor = last_funding_ms + 1
        if next_cursor <= cursor:
            raise RuntimeError(f"Binance funding pagination did not advance for {symbol}")
        if end_ms is not None and next_cursor >= end_ms:
            break
        if len(batch) < 1000:
            break
        cursor = next_cursor
        if request_sleep_seconds > 0:
            time.sleep(request_sleep_seconds)
    return rows


def funding_to_frame(symbol: str, rows: list[dict[str, Any]]) -> pl.DataFrame:
    """Convert raw funding events to the module funding schema."""
    if not rows:
        return pl.DataFrame(schema=FUNDING_SCHEMA)
    frame = pl.DataFrame(
        {
            "funding_time_ms": [int(row["fundingTime"]) for row in rows],
            "funding_rate": [float(row["fundingRate"]) for row in rows],
        }
    )
    return (
        frame.with_columns(
            pl.lit(symbol).alias("symbol"),
            pl.from_epoch(pl.col("funding_time_ms"), time_unit="ms")
            .dt.replace_time_zone("UTC")
            .alias("timestamp"),
        )
        .select(["timestamp", "symbol", "funding_rate"])
        .unique(subset=["timestamp", "symbol"], keep="last")
        .sort("timestamp")
    )


def collect_funding(
    *,
    output_dir: Path,
    symbols: list[str],
    start: str = "2023-01-01",
    end: str | None = None,
    base_url: str = BINANCE_FAPI_BASE_URL,
    skip_existing: bool = True,
    request_sleep_seconds: float = 0.15,
) -> list[Path]:
    """Collect one funding parquet file per symbol."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for symbol in symbols:
        path = output_dir / f"{symbol}.parquet"
        if skip_existing and path.exists():
            paths.append(path)
            continue
        rows = fetch_funding_history(
            symbol,
            start=start,
            end=end,
            base_url=base_url,
            request_sleep_seconds=request_sleep_seconds,
        )
        funding_to_frame(symbol, rows).write_parquet(path)
        paths.append(path)
        if request_sleep_seconds > 0:
            time.sleep(request_sleep_seconds)
    return paths


def load_funding_dir(data_dir: Path) -> pl.DataFrame:
    files = sorted(data_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No funding parquet files found in {data_dir}")
    return pl.concat([pl.read_parquet(path) for path in files], how="vertical_relaxed")


def symbols_from_ohlc_dir(data_dir: Path) -> list[str]:
    return sorted(path.stem for path in data_dir.glob("*.parquet"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect Binance USD-M funding rate history.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser("collect")
    collect_parser.add_argument("--output-dir", type=Path, default=Path("data/raw/binance_um_funding"))
    collect_parser.add_argument(
        "--ohlc-dir",
        type=Path,
        default=Path("data/raw/binance_um_1h_onboard_20230101_all"),
        help="Use the OHLC parquet filenames as the symbol universe.",
    )
    collect_parser.add_argument("--start", default="2023-01-01")
    collect_parser.add_argument("--end")
    collect_parser.add_argument("--request-sleep-seconds", type=float, default=0.15)
    collect_parser.add_argument("--overwrite-existing", action="store_true")

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--data-dir", type=Path, default=Path("data/raw/binance_um_funding"))

    args = parser.parse_args()
    if args.command == "collect":
        symbols = symbols_from_ohlc_dir(args.ohlc_dir)
        paths = collect_funding(
            output_dir=args.output_dir,
            symbols=symbols,
            start=args.start,
            end=args.end,
            skip_existing=not args.overwrite_existing,
            request_sleep_seconds=args.request_sleep_seconds,
        )
        print(json.dumps([str(path) for path in paths], indent=2))
    elif args.command == "audit":
        frame = load_funding_dir(args.data_dir)
        report = {
            "row_count": frame.height,
            "symbol_count": frame.get_column("symbol").n_unique(),
            "duplicate_rows": int(frame.select(["timestamp", "symbol"]).is_duplicated().sum()),
            "null_rates": int(frame.get_column("funding_rate").null_count()),
            "start": str(frame.get_column("timestamp").min()),
            "end": str(frame.get_column("timestamp").max()),
            "abs_rate_p99": float(frame.get_column("funding_rate").abs().quantile(0.99)),
        }
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
