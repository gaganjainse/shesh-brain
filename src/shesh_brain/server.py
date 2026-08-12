"""MCP server — packaged Shesh kernel for desktop, routes tool calls through policy."""

from __future__ import annotations

import sys

try:
    from shesh_audit.gate import Guard
    from shesh_audit.mcp_guard import GuardedMCP as FastMCP  # type: ignore
    HAS_GUARD = True
except ImportError:
    from fastmcp import FastMCP
    HAS_GUARD = False
    Guard = None  # type: ignore

mcp = FastMCP("shesh-brain")

try:
    from shesh_audit.nexus_bridge import NexusBridge
    _bridge = NexusBridge()
    HAS_BRIDGE = True
except ImportError:
    _bridge = None
    HAS_BRIDGE = False

@mcp.tool()
def route_tool_call(actor: str, tool: str, args: dict | None = None) -> dict:
    args = args or {}
    if HAS_GUARD:
        guard = Guard()
        decision = guard.check(tool, args)
        verdict = decision.verdict
        if verdict == "deny":
            return {"allowed": False, "verdict": "deny", "reason": decision.reason, "routed_to": "blocked"}
    else:
        verdict = "allow"
    if HAS_BRIDGE and _bridge:
        try:
            _bridge.emit(actor, tool, verdict, args)
        except Exception as exc:  # noqa: BLE001 — telemetry must never break a routed call
            print(f"nexus bridge emit failed: {exc}", file=sys.stderr)
    return {
        "allowed": True,
        "verdict": verdict if isinstance(verdict, str) else getattr(verdict, 'value', 'allow'),
        "routed_to": "shesh-kernel" if HAS_BRIDGE else "local",
        "has_guard": HAS_GUARD,
        "has_bridge": HAS_BRIDGE,
    }

@mcp.tool()
def get_policy() -> dict:
    if HAS_GUARD:
        try:
            guard = Guard()
            return {"rules": len(guard.policy.rules), "guard": True}
        except Exception as e:  # noqa: BLE001 — MCP tool boundary returns error dicts
            return {"error": str(e), "guard": True}
    return {"rules": 0, "guard": False, "stub": True}

@mcp.tool()
def list_tasks() -> list[dict]:
    """Real view into shesh-orchestrator sessions when available, else empty.

    Brain routes policy/audit; orchestrator owns scheduling — this bridges the
    two so MCP clients always get a truthful answer.
    """
    try:
        from shesh_orchestrator.sessions import SessionManager  # type: ignore

        return SessionManager().list_sessions()
    except ImportError:
        return []
    except Exception as exc:  # noqa: BLE001 — degrade gracefully, never raise in a tool
        return [{"error": f"orchestrator unavailable: {exc}"}]

@mcp.tool()
def schedule_task(goal: str, priority: str = "P1") -> dict:
    return {"scheduled": True, "goal": goal, "priority": priority, "routed_to": "stub"}

def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
