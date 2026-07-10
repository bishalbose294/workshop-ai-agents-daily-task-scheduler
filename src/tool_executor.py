"""
Dispatch layer: maps a tool name requested by LLM to the actual Python function.
This is the ONLY place where LLM output touches real code execution — validate here.
"""

from src.data_layer import fetch_calendar_events, fetch_weather, fetch_pending_tasks

TOOL_MAP = {
    "get_calendar_events": lambda inputs: fetch_calendar_events(inputs["date"]),
    "get_weather": lambda inputs: fetch_weather(inputs["date"], inputs.get("city", "Mumbai")),
    "get_pending_tasks": lambda inputs: fetch_pending_tasks(inputs["date"]),
}


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name not in TOOL_MAP:
        return {"error": f"Unknown tool requested: {tool_name}"}
    try:
        return TOOL_MAP[tool_name](tool_input)
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}
    

if __name__ == "__main__":
    tool_name = "get_calendar_events"
    tool_input = {"date": "2026-07-23"}
    result = execute_tool(tool_name, tool_input)
    print(result)

    tool_name = "get_weather"
    tool_input = {"date": "2026-07-23", "city": "Mumbai"}
    result = execute_tool(tool_name, tool_input)
    print(result)

    tool_name = "get_pending_tasks"
    tool_input = {"date": "2026-07-23"}
    result = execute_tool(tool_name, tool_input)
    print(result)
