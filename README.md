# PI Value Calculation Showcase

<!-- BrandCloud:readme-standard -->
[![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Showcase](https://img.shields.io/badge/Portfolio-Showcase-blue.svg)](#)

_Part of the `sakib-maho` project showcase series with consistent documentation and quality standards._

This repository is upgraded into a reproducible Monte Carlo PI estimation project.
The notebook is preserved, and the codebase now includes package modules, CLI, and tests.

## Features

- Monte Carlo PI estimation with configurable sample count
- Deterministic seeding support for repeatable runs
- CLI entrypoint for quick experiments
- Unit tests for estimator and CLI

## Quick Start

```bash
python3 cli.py --samples 10000
```

## Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## License

MIT License. See `LICENSE`.
