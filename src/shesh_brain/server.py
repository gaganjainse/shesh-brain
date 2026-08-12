"""MCP server — packaged Shesh kernel for desktop: policy routing + kernel event bridge.

Task/session management is owned by the shesh-orchestrator MCP server
(execute / start_session / get_session / list_sessions / cancel_session);
brain deliberately does not duplicate it.
"""

from __future__ import annotations

from shesh_audit.gate import Guard
from shesh_audit.kernel_bridge import KernelBridge
from shesh_audit.mcp_guard import GuardedMCP as FastMCP

mcp = FastMCP("shesh-brain")

_bridge = KernelBridge()
_guard = Guard(bridge=_bridge)


@mcp.tool()
def route_tool_call(actor: str, tool: str, args: dict | None = None) -> dict:
    """Check a proposed tool call against Shesh policy and record the decision.

    The Guard audit-logs every decision and mirrors it to the kernel event
    store. The caller executes the tool only when this returns allowed=True
    (or after human confirmation when requires_confirmation=True).
    """
    args = args or {}
    decision = _guard.check(tool, args, actor=actor)
    return {
        "allowed": decision.allowed,
        "requires_confirmation": decision.requires_confirmation,
        "verdict": decision.verdict,
        "reason": decision.reason,
    }


@mcp.tool()
def get_policy() -> dict:
    """Return a view of the active policy (rule count and rules)."""
    try:
        rules = [
            {"tool": r.tool, "verdict": r.verdict.value, "reason": r.reason}
            for r in _guard.policy.rules
        ]
        return {"guard": True, "rule_count": len(rules), "rules": rules}
    except Exception as e:  # noqa: BLE001 — MCP tool boundary returns error dicts
        return {"guard": True, "error": str(e)}


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
