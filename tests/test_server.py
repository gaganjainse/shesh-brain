from shesh_brain.server import route_tool_call, get_policy

def test_route():
    res = route_tool_call("test", "get_system_status", {})
    assert "allowed" in res

def test_policy():
    res = get_policy()
    assert isinstance(res, dict)
