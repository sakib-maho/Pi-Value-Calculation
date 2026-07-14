import csv
import math
from pathlib import Path
from subprocess import run

import pytest

from pi_calc.monte_carlo import (
    estimate_pi,
    estimate_pi_with_history,
    export_history_to_csv,
    multi_seed_stats,
)


def test_estimate_pi_is_reproducible() -> None:
    assert estimate_pi(2_000, seed=11) == estimate_pi(2_000, seed=11)


def test_estimate_pi_reasonably_close_to_pi() -> None:
    value = estimate_pi(20_000, seed=10)
    assert 3.0 < value < 3.3


def test_estimate_pi_rejects_invalid_samples() -> None:
    with pytest.raises(ValueError):
        estimate_pi(0)


def test_estimate_pi_with_history_returns_requested_checkpoints() -> None:
    estimate, history = estimate_pi_with_history(1_000, seed=5, checkpoints=[100, 500, 1_000])
    assert len(history) == 3
    assert history[0][0] == 100
    assert history[-1][0] == 1_000
    assert math.isclose(history[-1][1], estimate)
    assert history[-1][2] == pytest.approx(abs(estimate - math.pi))


def test_estimate_pi_with_history_clamps_large_checkpoint() -> None:
    estimate, history = estimate_pi_with_history(100, seed=3, checkpoints=[10, 500])
    assert history[-1][0] == 100
    assert history[-1][1] == pytest.approx(estimate)


def test_multi_seed_stats_summarizes_estimates() -> None:
    stats = multi_seed_stats(samples=2_000, seeds=[1, 2, 3])
    assert stats["seed_count"] == 3
    assert len(stats["estimates"]) == 3
    assert 3.0 < stats["mean"] < 3.3
    assert stats["std_dev"] >= 0.0


def test_multi_seed_stats_requires_seed_list() -> None:
    with pytest.raises(ValueError):
        multi_seed_stats(samples=100, seeds=[])


def test_export_history_to_csv_writes_rows(tmp_path: Path) -> None:
    history = [(100, 3.12, 0.02159), (500, 3.16, 0.01841)]
    output = export_history_to_csv(history, tmp_path / "history.csv")
    with output.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    assert rows[0] == ["samples", "estimate_pi", "abs_error_vs_math_pi"]
    assert rows[2][0] == "500"


def test_cli_basic_output() -> None:
    result = run(
        ["python3", "cli.py", "--samples", "5000", "--seed", "9"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "estimate=" in result.stdout
    assert "error_vs_math_pi=" in result.stdout


def test_cli_history_and_csv_output(tmp_path: Path) -> None:
    csv_path = tmp_path / "pi_history.csv"
    result = run(
        [
            "python3",
            "cli.py",
            "--samples",
            "1000",
            "--seed",
            "4",
            "--history",
            "100,500,1000",
            "--csv",
            str(csv_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "history[100]=" in result.stdout
    assert "history_csv=" in result.stdout
    assert csv_path.exists()


def test_cli_multi_seed_output() -> None:
    result = run(
        ["python3", "cli.py", "--samples", "2000", "--seeds", "1,2,3"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "mean=" in result.stdout
    assert "std_dev=" in result.stdout
