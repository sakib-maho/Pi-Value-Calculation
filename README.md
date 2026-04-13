# PI Value Calculation Showcase

This repository is upgraded into a reproducible Monte Carlo PI estimation project.
The notebook is preserved, and the codebase now includes package modules, CLI, and tests.

## Features

- Monte Carlo PI estimation with configurable sample count
- Deterministic seeding support for repeatable runs
- CLI entrypoint for quick experiments
- Unit tests for estimator and CLI

## Usage

```bash
python3 cli.py --samples 10000
```

## Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## License

MIT License. See `LICENSE`.
