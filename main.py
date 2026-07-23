from src.agent import DailyPlannerAgent
from colorama import Fore

if __name__ == "__main__":
    agent = DailyPlannerAgent()
    
    # All 3 tools (calendar + weather + tasks)
    prompt = "Plan my full day for 2026-07-15 — I have outdoor errands to run between meetings and a few pending tasks I want to fit in."
    # prompt = "Build me a realistic schedule for 2026-07-22. I'll be commuting across the city for some tasks, so factor in the weather."
    # prompt = "Give me a time-blocked plan for 2026-08-03 that fits my meetings, my to-dos, and accounts for whether I'll get rained on."

    # Calendar + Weather only (explicitly no tasks)
    # prompt = "I have no pending tasks today. Just tell me my meeting schedule for 2026-07-18 and whether the weather will disrupt my commute."
    # prompt = "Ignore my to-do list for 2026-07-27 — I just want my meetings laid out with a note on outdoor/commute risk from the weather."

    # Calendar + Tasks only (explicitly staying home / no weather)
    # prompt = "I'm staying home all day on 2026-07-16, so skip weather. Just schedule my meetings and pending tasks around each other."
    # prompt = "Plan 2026-08-05 for me — I'm not leaving the house today, so no need to check weather. Just fit my tasks around my meetings."

    # Weather + Tasks only (no fixed meetings expected / testing calendar still gets checked)
    # prompt = "I don't think I have any meetings on 2026-07-30, but I have several pending tasks — some outdoors. Check the weather and build my day around my to-dos."

    # Single-tool edge cases (to test the agent resists over-calling)
    # prompt = "What's the weather forecast for 2026-08-10? I'm just deciding whether to walk or drive, no need to look at my calendar or tasks."
    # prompt = "List out my pending tasks for 2026-07-25 only — don't worry about meetings or weather, I just want to see what's on my plate."

    result = agent.run(
        prompt
    )

    print(Fore.YELLOW + "\n=========== FINAL DAILY PLAN ===========")
    print(result)