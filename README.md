# 🧠 shesh-brain

Packaged SheshAOS kernel for desktop — routes tool calls through the policy Guard and mirrors every decision to the kernel event store. Brain layer.

- Part of [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)
- Layer: Brain (governance)
- Provides: policy-router, kernel event bridge, tool-broker governance
- Upstream: shesh-kernel / SheshAOS Rust workspace (crates/shesh-kernel)

## Tools
- `route_tool_call` — check a proposed tool call via the Guard; the decision is audit-logged and mirrored to the kernel event store; the caller executes only when allowed
- `get_policy` — current policy rules

Task/session management (`execute`, `start_session`, `list_sessions`, …) is owned by
[shesh-orchestrator](https://github.com/gaganjainse/shesh-orchestrator) — brain does not duplicate it.

## Dev
```bash
uv sync && uv run pytest
```

## Security

Security posture and vulnerability reporting: [canonical ecosystem security
policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).
