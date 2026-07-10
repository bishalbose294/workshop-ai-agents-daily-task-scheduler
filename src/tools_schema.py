"""
JSON Schema definitions describing each tool to LLM.
LLM uses 'description' fields to decide WHEN to call each tool.
"""

TOOLS = [
    {
        "name": "get_calendar_events",
        "description": "Fetch the user's scheduled meetings/events for a given date. Use this to know what fixed commitments exist before building a plan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                }
            },
            "required": ["date"]
        }
    },
    {
        "name": "get_weather",
        "description": "Fetch weather forecast for a given date and city. Use this to decide if outdoor tasks/commute should be adjusted.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "city": {"type": "string", "description": "City name, defaults to Mumbai"}
            },
            "required": ["date"]
        }
    },
    {
        "name": "get_pending_tasks",
        "description": "Fetch the user's pending to-do tasks with priority, estimated duration, and deadline for a given date. Use this to know what needs to be fit into free time slots.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
            },
            "required": ["date"]
        }
    }
]