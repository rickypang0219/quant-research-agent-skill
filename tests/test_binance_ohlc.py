from __future__ import annotations

import polars as pl

from research.crypto_stat_arb.binance_ohlc import repair_ohlc_invariants


def test_repair_ohlc_invariants_widens_bad_vendor_candle() -> None:
    frame = pl.DataFrame(
        {
            "open": [0.8131],
            "high": [0.8239],
            "low": [0.8113],
            "close": [0.8251],
        }
    )

    repaired = repair_ohlc_invariants(frame)

    assert repaired.item(0, "high") == 0.8251
    assert repaired.item(0, "low") == 0.8113
