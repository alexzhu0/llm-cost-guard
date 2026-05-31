# Llm Cost Guard

Estimate prompt token cost and flag expensive LLM inputs locally.

## Why

Prompt cost surprises are easy to miss before deployment.

This repository is intentionally small: it should be useful in one command, easy to inspect, and simple to fork.

## Install

```bash
git clone https://github.com/alexzhu0/llm-cost-guard.git
cd llm-cost-guard
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --rate 0.000005
```

## Examples

```bash
PYTHONPATH=src python3 -m llm_cost_guard examples/prompt.txt --rate 0.000005
```

## API

The first release is CLI-first. Public Python APIs can be added after real usage proves the right shape.

## FAQ

**Does this call external AI APIs?**

No. The generated starter uses the Python standard library only.

**Is this production-ready?**

Treat `v0.1.0` as a focused utility release. Pin versions and review output before adding it to CI.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

## License

MIT
