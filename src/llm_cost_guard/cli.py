"""Estimate prompt token cost and flag expensive LLM inputs locally."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, Sequence


def estimate_tokens(text: str) -> int:
    # Cheap local approximation used before provider-specific tokenizers.
    return max(1, math.ceil(len(text) / 4))


def analyze_cost(path: str, rate: float, budget: float = 0.01) -> Dict[str, float | int | str]:
    text = Path(path).read_text(encoding="utf-8")
    tokens = estimate_tokens(text)
    cost = tokens * rate
    return {
        "characters": len(text),
        "estimated_tokens": tokens,
        "estimated_cost": round(cost, 6),
        "budget": budget,
        "status": "over-budget" if cost > budget else "ok",
    }


def format_text(result: Dict[str, float | int | str]) -> str:
    return "\n".join(
        [
            f"Characters: {result['characters']}",
            f"Estimated tokens: {result['estimated_tokens']}",
            f"Estimated cost: ${result['estimated_cost']}",
            f"Budget: ${result['budget']}",
            f"Status: {result['status']}",
        ]
    )


def run(input_path: str, rate: float, budget: float = 0.01, output_format: str = "text") -> str:
    result = analyze_cost(input_path, rate, budget)
    if output_format == "json":
        return json.dumps(result, indent=2, sort_keys=True)
    return format_text(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Estimate prompt token cost and flag expensive LLM inputs locally.")
    parser.add_argument("input", help="Prompt text file")
    parser.add_argument("--rate", type=float, required=True, help="Cost per token")
    parser.add_argument("--budget", type=float, default=0.01)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.rate, args.budget, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
