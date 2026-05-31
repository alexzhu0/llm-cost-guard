# LLM Cost Guard

Estimate prompt token cost and flag expensive LLM inputs locally.

## Why

Prompt cost surprises are easy to miss before deployment, especially with long agent context.

This is a baseline HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/llm-cost-guard.git
cd llm-cost-guard
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --model generic --budget 0.001
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --model generic --budget 0.001
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --model generic --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m llm_cost_guard --help`
- Main demo: `PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --model generic --budget 0.001`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Local token approximation
- Model rate presets
- Manual rate override
- Budget threshold status
- Text and JSON output

## API

The public Python surface is intentionally small:

```python
from llm_cost_guard.cli import analyze_cost
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It is a fast local cost sanity check before prompts reach production.

## Used With

- Run as a CI budget guard for long prompts and coding-agent context files.
- Pair with `repo-to-ai-brief` to keep generated briefs inside a practical token budget.
- Keep this as a supporting utility; the stronger public story is budget discipline for agent workflows.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
