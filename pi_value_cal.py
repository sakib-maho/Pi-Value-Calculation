"""Backward-compatible entrypoint for PI CLI."""

from cli import main


if __name__ == "__main__":
    raise SystemExit(main())
