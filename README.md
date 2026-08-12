# 🧠 shesh-brain

Packaged SheshAOS kernel for desktop — routes tool calls through policy Guard. Brain layer.

- Part of [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)
- Layer: Brain (governance)
- Provides: task-router, scheduler, tool-broker
- Upstream: shesh-kernel / SheshAOS Rust workspace 12 crates, 981 tests

## Tools
- `route_tool_call` — check tool via Guard, emit Nexus event, forward to SheshAOS if available else stub
- `get_policy` — current policy rules
- `list_tasks` — queued tasks
- `schedule_task` — schedule with budget

## Dev
```bash
uv sync && uv run pytest
```
