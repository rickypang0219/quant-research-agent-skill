from __future__ import annotations

from datetime import UTC, datetime, timedelta

import polars as pl

from research.crypto_stat_arb.train_forward_validation import (
    ParameterGrid,
    _split_timestamp_by_ratio,
)


def test_parameter_grid_optimizes_only_two_parameters() -> None:
    grid = ParameterGrid(pca_window_days=(90, 180), entry_scores=(1.25, 1.5, 1.75))

    assert grid.optimized_parameter_count == 2
    assert grid.search_count == 6


def test_split_timestamp_by_ratio_is_chronological() -> None:
    start = datetime(2023, 1, 1, tzinfo=UTC)
    frame = pl.DataFrame(
        {
            "timestamp": [start + timedelta(hours=4 * index) for index in range(10)],
            "symbol": ["BTCUSDT"] * 10,
            "close": [100.0 + index for index in range(10)],
        }
    )

    split_timestamp, split_index, timestamps = _split_timestamp_by_ratio(frame, 0.8)

    assert split_index == 8
    assert split_timestamp == timestamps[8]
