#!/usr/bin/env python3
"""GitHub Actions entry point for the Daily Agentic Business Pulse."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from agentic_business_pulse import PulseConfig, PulseError, run_pulse


PROJECT_DIR = Path(__file__).resolve().parent.parent


def main() -> int:
    try:
        config = PulseConfig.from_env(PROJECT_DIR)
        result = run_pulse(config)
    except PulseError as error:
        print(f"[pulse:error] {error}", file=sys.stderr)
        return 1
    print("[pulse:result] " + json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
