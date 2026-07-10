from src.agent import DailyPlannerAgent
from colorama import Fore

if __name__ == "__main__":
    agent = DailyPlannerAgent()
    result = agent.run(
        "Plan my day for 2026-07-25. Fit in my pending tasks around my meetings, and account for the weather and tell me if I should carry an umbrella or not."
    )
    print(Fore.YELLOW + "\n=========== FINAL DAILY PLAN ===========")
    print(result)