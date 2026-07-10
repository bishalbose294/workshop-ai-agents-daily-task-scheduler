from datetime import datetime
import simplejson as json


MOCK_CALENDAR = json.load(open("./data/mock_calendar.json"))
MOCK_WEATHER = json.load(open("./data/mock_weather.json"))
MOCK_TASKS = json.load(open("./data/mock_tasks.json"))


def fetch_calendar_events(date: str) -> dict:
    events = MOCK_CALENDAR.get(date, [])
    return {"date": date, "event_count": len(events), "events": events}


def fetch_weather(date: str, city: str = "Mumbai") -> dict:
    weather = MOCK_WEATHER.get(date)
    if not weather:
        return {"error": f"No weather data for {date}"}
    return weather


def fetch_pending_tasks(date: str) -> dict:
    tasks = MOCK_TASKS.get(date, [])
    return {"date": date, "task_count": len(tasks), "tasks": tasks}


if __name__ == "__main__":
    # Example usage
    date_str = "2026-07-23"
    print(fetch_calendar_events(date_str))
    print(fetch_weather(date_str))
    print(fetch_pending_tasks(date_str))