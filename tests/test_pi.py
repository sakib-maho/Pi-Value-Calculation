from subprocess import run
import unittest

from pi_calc.monte_carlo import estimate_pi


class PiEstimationTests(unittest.TestCase):
    def test_estimate_close_to_pi(self) -> None:
        value = estimate_pi(20000, seed=10)
        self.assertGreater(value, 3.0)
        self.assertLess(value, 3.3)

    def test_cli(self) -> None:
        result = run(
            ["python3", "cli.py", "--samples", "5000"],
            check=True,
            text=True,
            capture_output=True,
        )
        value = float(result.stdout.strip())
        self.assertGreater(value, 2.5)
        self.assertLess(value, 3.6)


if __name__ == "__main__":
    unittest.main()
