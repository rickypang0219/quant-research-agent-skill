"""Binance USD-M perpetual 1h OHLC collection and audit helpers.

This module deliberately stays at the research-data layer. It uses Binance's
current USD-M futures REST endpoints to select USDT perpetual contracts whose
``onboardDate`` is on or before the cutoff date, then paginates 1h klines.

Research caveat: the current exchangeInfo endpoint is not a complete historical
listing/delisting database. For a production-grade point-in-time universe, keep
daily exchangeInfo snapshots or source a historical instrument master.
"""

from __future__ import annotations

import argparse
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl

BINANCE_FAPI_BASE_URL = "https://fapi.binance.com"
KLINE_INTERVAL_MS = 60 * 60 * 1000


@dataclass(frozen=True)
class SymbolInfo:
    symbol: str
    onboard_ms: int
    quote_volume: float | None = None


def parse_utc_ms(value: str | None) -> int | None:
    """Parse an ISO date/datetime string to UTC epoch milliseconds."""
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    if len(raw) == 10:
        dt = datetime.fromisoformat(raw).replace(tzinfo=UTC)
    else:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        else:
            dt = dt.astimezone(UTC)
    return int(dt.timestamp() * 1000)


def _request_json(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    base_url: str = BINANCE_FAPI_BASE_URL,
    timeout_seconds: float = 30.0,
    max_retries: int = 6,
    retry_sleep_seconds: float = 5.0,
) -> Any:
    query = urllib.parse.urlencode(params or {})
    url = f"{base_url}{path}"
    if query:
        url = f"{url}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "quant-research-agent/0.1"})
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code not in {418, 429} or attempt >= max_retries:
                raise
            retry_after = error.headers.get("Retry-After")
            if retry_after is not None:
                sleep_seconds = float(retry_after)
            else:
                sleep_seconds = retry_sleep_seconds * (2**attempt)
            time.sleep(sleep_seconds)
        except (ConnectionResetError, TimeoutError, socket.timeout, urllib.error.URLError) as error:
            if attempt >= max_retries:
                raise
            sleep_seconds = retry_sleep_seconds * (2**attempt)
            print(f"Transient request failure for {path}: {error}. Retrying in {sleep_seconds:.1f}s.")
            time.sleep(sleep_seconds)
    raise RuntimeError("unreachable retry loop state")


def fetch_exchange_info(*, base_url: str = BINANCE_FAPI_BASE_URL) -> dict[str, Any]:
    return _request_json("/fapi/v1/exchangeInfo", base_url=base_url)


def fetch_24h_tickers(*, base_url: str = BINANCE_FAPI_BASE_URL) -> list[dict[str, Any]]:
    return _request_json("/fapi/v1/ticker/24hr", base_url=base_url)


def select_usdt_perp_universe(
    *,
    onboard_cutoff: str = "2023-01-01",
    max_symbols: int | None = None,
    min_quote_volume: float | None = None,
    sort_by_quote_volume: bool = True,
    base_url: str = BINANCE_FAPI_BASE_URL,
) -> list[SymbolInfo]:
    """Select current USDT perpetual symbols onboarded by the cutoff date.

    Binance returns ``onboardDate`` in milliseconds for USD-M futures symbols.
    The filter is intentionally strict: USDT quote, PERPETUAL contract, current
    TRADING status, and onboarded no later than the cutoff.
    """
    cutoff_ms = parse_utc_ms(onboard_cutoff)
    if cutoff_ms is None:
        raise ValueError("onboard_cutoff must be a date or datetime")

    exchange_info = fetch_exchange_info(base_url=base_url)
    quote_volume_by_symbol: dict[str, float] = {}
    if sort_by_quote_volume or min_quote_volume is not None:
        for ticker in fetch_24h_tickers(base_url=base_url):
            symbol = str(ticker.get("symbol", ""))
            try:
                quote_volume_by_symbol[symbol] = float(ticker.get("quoteVolume", 0.0))
            except (TypeError, ValueError):
                quote_volume_by_symbol[symbol] = 0.0

    symbols: list[SymbolInfo] = []
    for item in exchange_info.get("symbols", []):
        symbol = str(item.get("symbol", ""))
        onboard_ms = int(item.get("onboardDate", 0))
        if item.get("quoteAsset") != "USDT":
            continue
        if item.get("contractType") != "PERPETUAL":
            continue
        if item.get("status") != "TRADING":
            continue
        if onboard_ms > cutoff_ms:
            continue

        quote_volume = quote_volume_by_symbol.get(symbol)
        if min_quote_volume is not None and (quote_volume is None or quote_volume < min_quote_volume):
            continue
        symbols.append(SymbolInfo(symbol=symbol, onboard_ms=onboard_ms, quote_volume=quote_volume))

    if sort_by_quote_volume:
        symbols.sort(key=lambda item: item.quote_volume or 0.0, reverse=True)
    else:
        symbols.sort(key=lambda item: item.symbol)
    if max_symbols is not None:
        symbols = symbols[:max_symbols]
    return symbols


def fetch_1h_klines(
    symbol: str,
    *,
    start: str = "2023-01-01",
    end: str | None = None,
    base_url: str = BINANCE_FAPI_BASE_URL,
    request_sleep_seconds: float = 0.2,
) -> list[list[Any]]:
    """Fetch all 1h klines for one USD-M futures symbol."""
    start_ms = parse_utc_ms(start)
    end_ms = parse_utc_ms(end)
    if start_ms is None:
        raise ValueError("start must be a date or datetime")
    rows: list[list[Any]] = []
    cursor = start_ms

    while True:
        params: dict[str, Any] = {
            "symbol": symbol,
            "interval": "1h",
            "limit": 1500,
            "startTime": cursor,
        }
        if end_ms is not None:
            params["endTime"] = end_ms

        batch = _request_json("/fapi/v1/klines", params=params, base_url=base_url)
        if not batch:
            break
        rows.extend(batch)
        last_open_ms = int(batch[-1][0])
        next_cursor = last_open_ms + KLINE_INTERVAL_MS
        if next_cursor <= cursor:
            raise RuntimeError(f"Binance kline pagination did not advance for {symbol}")
        if end_ms is not None and next_cursor >= end_ms:
            break
        if len(batch) < 1500:
            break
        cursor = next_cursor
        if request_sleep_seconds > 0:
            time.sleep(request_sleep_seconds)

    return rows


def klines_to_frame(symbol: str, rows: list[list[Any]]) -> pl.DataFrame:
    """Convert Binance kline rows to the module OHLC schema."""
    if not rows:
        return pl.DataFrame(
            schema={
                "timestamp": pl.Datetime(time_unit="ms", time_zone="UTC"),
                "symbol": pl.String,
                "open": pl.Float64,
                "high": pl.Float64,
                "low": pl.Float64,
                "close": pl.Float64,
                "volume": pl.Float64,
                "quote_volume": pl.Float64,
                "open_time_ms": pl.Int64,
                "close_time_ms": pl.Int64,
            }
        )

    frame = pl.DataFrame(
        rows,
        schema=[
            "open_time_ms",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time_ms",
            "quote_volume",
            "trade_count",
            "taker_buy_base_volume",
            "taker_buy_quote_volume",
            "ignore",
        ],
        orient="row",
    )
    frame = (
        frame.with_columns(
            pl.lit(symbol).alias("symbol"),
            pl.from_epoch(pl.col("open_time_ms").cast(pl.Int64), time_unit="ms")
            .dt.replace_time_zone("UTC")
            .alias("timestamp"),
            pl.col("close_time_ms").cast(pl.Int64),
            pl.col("open").cast(pl.Float64),
            pl.col("high").cast(pl.Float64),
            pl.col("low").cast(pl.Float64),
            pl.col("close").cast(pl.Float64),
            pl.col("volume").cast(pl.Float64),
            pl.col("quote_volume").cast(pl.Float64),
        )
        .select(
            [
                "timestamp",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "quote_volume",
                "open_time_ms",
                "close_time_ms",
            ]
        )
        .sort(["symbol", "timestamp"])
    )
    return repair_ohlc_invariants(frame)


def repair_ohlc_invariants(frame: pl.DataFrame) -> pl.DataFrame:
    """Conservatively repair vendor OHLC rows that violate candle bounds.

    Binance occasionally returns a high below the close or a low above the
    close. For research candles, preserve open/close and widen the candle range.
    """
    required = {"open", "high", "low", "close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Cannot repair OHLC invariants; missing columns: {sorted(missing)}")
    return frame.with_columns(
        pl.max_horizontal("open", "high", "low", "close").alias("high"),
        pl.min_horizontal("open", "high", "low", "close").alias("low"),
    )


def collect_1h_ohlc(
    *,
    output_dir: Path,
    start: str = "2023-01-01",
    end: str | None = None,
    onboard_cutoff: str = "2023-01-01",
    max_symbols: int | None = None,
    min_quote_volume: float | None = None,
    base_url: str = BINANCE_FAPI_BASE_URL,
    skip_existing: bool = True,
    request_sleep_seconds: float = 0.2,
) -> list[Path]:
    """Collect one parquet file per selected symbol."""
    output_dir.mkdir(parents=True, exist_ok=True)
    universe = select_usdt_perp_universe(
        onboard_cutoff=onboard_cutoff,
        max_symbols=max_symbols,
        min_quote_volume=min_quote_volume,
        base_url=base_url,
    )
    paths: list[Path] = []
    for info in universe:
        path = output_dir / f"{info.symbol}.parquet"
        if skip_existing and path.exists():
            paths.append(path)
            continue
        rows = fetch_1h_klines(
            info.symbol,
            start=start,
            end=end,
            base_url=base_url,
            request_sleep_seconds=request_sleep_seconds,
        )
        frame = klines_to_frame(info.symbol, rows)
        frame.write_parquet(path)
        paths.append(path)
        if request_sleep_seconds > 0:
            time.sleep(request_sleep_seconds)
    return paths


def load_ohlc_dir(data_dir: Path) -> pl.DataFrame:
    files = sorted(data_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {data_dir}")
    return pl.concat([pl.read_parquet(path) for path in files], how="vertical_relaxed")


def audit_ohlc_frame(frame: pl.DataFrame, *, expected_interval_ms: int = KLINE_INTERVAL_MS) -> dict[str, Any]:
    """Return a compact OHLC audit report for the research data contract."""
    required = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
    missing_columns = sorted(required.difference(frame.columns))
    if missing_columns:
        return {"ok": False, "missing_columns": missing_columns}

    issues: dict[str, Any] = {
        "row_count": frame.height,
        "symbol_count": frame.get_column("symbol").n_unique(),
        "duplicate_rows": frame.select(["timestamp", "symbol"]).is_duplicated().sum(),
        "bad_ohlc_rows": frame.filter(
            (pl.col("open") <= 0)
            | (pl.col("high") <= 0)
            | (pl.col("low") <= 0)
            | (pl.col("close") <= 0)
            | (pl.col("low") > pl.min_horizontal("open", "close"))
            | (pl.col("high") < pl.max_horizontal("open", "close"))
            | (pl.col("high") < pl.col("low"))
        ).height,
        "negative_volume_rows": frame.filter(pl.col("volume") < 0).height,
        "missing_intervals": 0,
        "symbols_with_gaps": [],
    }

    for symbol, symbol_frame in frame.sort(["symbol", "timestamp"]).group_by("symbol"):
        timestamps = symbol_frame.get_column("timestamp").to_list()
        gap_count = 0
        for left, right in zip(timestamps, timestamps[1:], strict=False):
            delta_ms = int((right - left).total_seconds() * 1000)
            if delta_ms > expected_interval_ms:
                gap_count += max(1, (delta_ms // expected_interval_ms) - 1)
            elif delta_ms <= 0:
                gap_count += 1
        if gap_count:
            symbol_name = symbol[0] if isinstance(symbol, tuple) else symbol
            issues["symbols_with_gaps"].append(symbol_name)
            issues["missing_intervals"] += gap_count

    issues["ok"] = (
        issues["duplicate_rows"] == 0
        and issues["bad_ohlc_rows"] == 0
        and issues["negative_volume_rows"] == 0
        and issues["missing_intervals"] == 0
    )
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect or audit Binance USD-M 1h OHLC data.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    universe_parser = subparsers.add_parser("universe")
    universe_parser.add_argument("--onboard-cutoff", default="2023-01-01")
    universe_parser.add_argument("--max-symbols", type=int)
    universe_parser.add_argument("--min-quote-volume", type=float)

    collect_parser = subparsers.add_parser("collect")
    collect_parser.add_argument("--output-dir", type=Path, default=Path("data/raw/binance_um_1h"))
    collect_parser.add_argument("--start", default="2023-01-01")
    collect_parser.add_argument("--end")
    collect_parser.add_argument("--onboard-cutoff", default="2023-01-01")
    collect_parser.add_argument("--max-symbols", type=int)
    collect_parser.add_argument("--min-quote-volume", type=float)
    collect_parser.add_argument("--request-sleep-seconds", type=float, default=0.2)
    collect_parser.add_argument("--overwrite-existing", action="store_true")

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--data-dir", type=Path, default=Path("data/raw/binance_um_1h"))

    args = parser.parse_args()
    if args.command == "universe":
        universe = select_usdt_perp_universe(
            onboard_cutoff=args.onboard_cutoff,
            max_symbols=args.max_symbols,
            min_quote_volume=args.min_quote_volume,
        )
        print(json.dumps([info.__dict__ for info in universe], indent=2))
    elif args.command == "collect":
        paths = collect_1h_ohlc(
            output_dir=args.output_dir,
            start=args.start,
            end=args.end,
            onboard_cutoff=args.onboard_cutoff,
            max_symbols=args.max_symbols,
            min_quote_volume=args.min_quote_volume,
            skip_existing=not args.overwrite_existing,
            request_sleep_seconds=args.request_sleep_seconds,
        )
        print(json.dumps([str(path) for path in paths], indent=2))
    elif args.command == "audit":
        frame = load_ohlc_dir(args.data_dir)
        print(json.dumps(audit_ohlc_frame(frame), indent=2, default=str))


if __name__ == "__main__":
    main()
