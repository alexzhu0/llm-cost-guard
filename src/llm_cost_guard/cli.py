"""Estimate prompt token cost and flag expensive LLM inputs locally."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, Sequence


MODEL_PRESETS = {
    # Approximate input-token rates for quick local triage. Override with --rate for billing-critical use.
    "gpt-4o-mini": 0.00000015,
    "gpt-4.1-mini": 0.0000004,
    "claude-haiku": 0.00000025,
    "generic": 0.000005,
}


def estimate_tokens(text: str) -> int:
    # Cheap local approximation used before provider-specific tokenizers.
    return max(1, math.ceil(len(text) / 4))


def resolve_rate(rate: float | None, model: str) -> float:
    if rate is not None:
        return rate
    return MODEL_PRESETS.get(model, MODEL_PRESETS["generic"])


def analyze_cost(
    path: str,
    rate: float | None = None,
    budget: float = 0.01,
    model: str = "gpt-4o-mini",
) -> Dict[str, float | int | str]:
    text = Path(path).read_text(encoding="utf-8")
    tokens = estimate_tokens(text)
    resolved_rate = resolve_rate(rate, model)
    cost = tokens * resolved_rate
    return {
        "model": model,
        "rate": resolved_rate,
        "characters": len(text),
        "estimated_tokens": tokens,
        "estimated_cost": round(cost, 6),
        "budget": budget,
        "status": "over-budget" if cost > budget else "ok",
    }


def format_text(result: Dict[str, float | int | str]) -> str:
    return "\n".join(
        [
            f"Model: {result['model']}",
            f"Rate: ${result['rate']} per token",
            f"Characters: {result['characters']}",
            f"Estimated tokens: {result['estimated_tokens']}",
            f"Estimated cost: ${result['estimated_cost']}",
            f"Budget: ${result['budget']}",
            f"Status: {result['status']}",
        ]
    )


def run(
    input_path: str,
    rate: float | None = None,
    budget: float = 0.01,
    output_format: str = "text",
    model: str = "gpt-4o-mini",
) -> str:
    result = analyze_cost(input_path, rate, budget, model)
    if output_format == "json":
        return json.dumps(result, indent=2, sort_keys=True)
    return format_text(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Estimate prompt token cost and flag expensive LLM inputs locally.")
    parser.add_argument("input", help="Prompt text file")
    parser.add_argument("--rate", type=float, default=None, help="Cost per token; overrides --model preset")
    parser.add_argument("--model", choices=sorted(MODEL_PRESETS), default="gpt-4o-mini")
    parser.add_argument("--budget", type=float, default=0.01)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.rate, args.budget, args.format, args.model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
