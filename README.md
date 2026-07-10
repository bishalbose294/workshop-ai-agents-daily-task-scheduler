# Daily Task Scheduler Agent

Workshop project: an AI agent that builds a time-blocked daily plan using the **ReAct** pattern (Reason → Act → Observe → Repeat).

It pulls calendar events, weather, and pending tasks via tools, then schedules work around fixed meetings (9:00–21:00).

## How it works

```
User request
    ↓
DailyPlannerAgent (OpenRouter LLM)
    ↓
Tool calls → get_calendar_events / get_weather / get_pending_tasks
    ↓
Mock data layer (JSON files)
    ↓
Final time-blocked schedule
```

**Tools**

| Tool | Purpose |
|------|---------|
| `get_calendar_events` | Fixed meetings for a date |
| `get_weather` | Forecast (outdoor/commute risk) |
| `get_pending_tasks` | Todos with priority, duration, deadline |

## Project structure

```
├── main.py                 # Entry point
├── test_setup.py           # Quick OpenRouter connectivity check
├── requirements.txt
├── data/
│   ├── mock_calendar.json
│   ├── mock_weather.json
│   └── mock_tasks.json
└── src/
    ├── agent.py            # ReAct agent loop
    ├── tools_schema.py     # Tool definitions for the LLM
    ├── tool_executor.py    # Dispatches tool calls
    └── data_layer.py       # Reads mock JSON data
```

## Setup

1. **Clone & create a virtualenv**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

Create a `.env` in the project root:

```env
OPENROUTER_API_KEY=your_key_here
MODEL=your_model_id_here
```

4. **Verify API access** (optional)

```bash
python test_setup.py
```

## Run

From the project root (so `./data` resolves correctly):

```bash
# Ensure src is on PYTHONPATH, or run from src-aware setup
set PYTHONPATH=src
python main.py
```

On macOS/Linux:

```bash
PYTHONPATH=src python main.py
```

The agent plans for the date in `main.py` (default: `2026-07-09`) using mock data for that day.

## Customize

- **Change the request/date** — edit the string in `main.py`
- **Add mock data** — extend the JSON files under `data/` (keys are `YYYY-MM-DD`)
- **Add tools** — update `tools_schema.py`, `data_layer.py`, and `TOOL_MAP` in `tool_executor.py`

## Requirements

- Python 3.10+
- OpenRouter API key
